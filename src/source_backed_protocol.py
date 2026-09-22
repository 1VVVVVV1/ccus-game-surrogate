"""Source-backed execution, exact boundary V2, provenance and verified resume."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd

from .config import ROOT, CONFIG_PATH, FEATURES, DOMAIN, MODES, BASELINE, TARGETS
from .dataset import baseline, build_dataset, validate_rows
from .scenario_solver import solve_scenario
from .surrogate import fit_surrogates
from .sobol_design import design, scenario_split
from .boundary_v2 import BOUNDARY_TARGETS, exact_grid_search
from .investment_synchronization_diagnostics import summarize_mode, check_identical_target_hashes
from .reproducibility import (identity, sha256, canonical_hash, read_json, write_json,
                              write_csv, write_text, append_progress, source_manifest)

FORMAL = ROOT / 'results/source_backed_formal'


def git(*args):
    return subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', *args],
                                   cwd=ROOT, text=True).strip()


def provenance():
    return dict(identity(), git_commit=git('rev-parse', 'HEAD'),
                parameter_registry_sha256=sha256(ROOT/'config/parameter_registry.source_backed.csv'),
                source_catalog_sha256=sha256(ROOT/'docs/SOURCE_CATALOG.md'),
                official_carbon_csv_sha256=sha256(FORMAL/'calibration/carbon_price_series.csv'),
                sobol_design_sha256=canonical_hash(design().to_dict('list')),
                scenario_split_sha256=canonical_hash(scenario_split().to_dict('list')))


def save_json(path, value, resume):
    if path.exists():
        if not resume or canonical_hash(read_json(path)) != canonical_hash(value):
            raise RuntimeError(f'RESUME_MISMATCH: {path}')
    else:
        write_json(path, value)


def save_csv(path, frame, resume):
    if path.exists():
        if not resume:
            raise RuntimeError(f'EXISTING_ARTIFACT: {path}')
        expected = pd.read_csv(__import__('io').StringIO(frame.to_csv(index=False, float_format='%.17g')),
                               float_precision='round_trip')
        pd.testing.assert_frame_equal(pd.read_csv(path, float_precision='round_trip'), expected)
    else:
        write_csv(path, frame)


def gate(name, evidence, resume):
    save_json(FORMAL/'gates'/f'{name}.json', dict(status='PASS', identity=identity(), evidence=evidence), resume)
    print(f'{name}: PASS', flush=True)


def tests():
    env = os.environ.copy()
    env.pop('CCUS_CONFIG_PATH', None)
    outputs = []
    commands = [(['-m', 'compileall', '-q', 'src', 'tests', 'run_source_backed_protocol.py'], env),
                (['-m', 'pytest', '-q'], env),
                (['-m', 'pytest', '-q', 'tests/test_dynamic_solver.py', 'tests/test_commit_now.py',
                  'tests/test_synchronization.py', 'tests/test_boundary_v2.py',
                  'tests/test_static_accounting_roundoff.py', 'tests/test_accounting_validation.py'], os.environ.copy())]
    for args, environment in commands:
        result = subprocess.run([sys.executable, *args], cwd=ROOT, env=environment,
                                capture_output=True, text=True)
        outputs.append(dict(command=args, exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr))
        print(result.stdout, flush=True)
        if result.returncode:
            raise RuntimeError('PREFLIGHT_TEST_FAILURE: '+result.stdout+result.stderr)
    return outputs


def validate_source():
    audit = read_json(FORMAL/'gates/GATE_SOURCE_AUDIT.json')
    if audit['status'] != 'PASS' or audit['config_sha256'] != sha256(CONFIG_PATH):
        raise RuntimeError('SOURCE_AUDIT_CONFIG_MISMATCH')
    if audit['parameter_registry_sha256'] != sha256(ROOT/'config/parameter_registry.source_backed.csv'):
        raise RuntimeError('SOURCE_REGISTRY_MISMATCH')
    calibration = read_json(FORMAL/'calibration/carbon_gbm_calibration.json')
    if calibration['official_input_sha256'] != sha256(FORMAL/'calibration/carbon_price_series.csv'):
        raise RuntimeError('OFFICIAL_CARBON_HASH_MISMATCH')
    from .carbon_calibration import fit_official_gbm
    prices = pd.read_csv(FORMAL/'calibration/carbon_price_series.csv')
    measured, _ = fit_official_gbm(prices.date.tolist(), prices.close.tolist())
    if any(measured[k] != calibration[k] for k in ('P0', 'mu', 'sigma', 'n_observations')):
        raise RuntimeError('CARBON_CALIBRATION_RECOMPUTATION_MISMATCH')
    frozen = read_json(ROOT/'results/resume_before_1d8388dd.json')
    if any(sha256(ROOT/'results/formal'/p) != h for p, h in frozen['artifacts'].items()):
        raise RuntimeError('METHOD_VALIDATION_ARTIFACT_CHANGED')
    if sha256(ROOT/'config/model_config.game.json') != frozen['identity']['config_sha256']:
        raise RuntimeError('METHOD_VALIDATION_CONFIG_CHANGED')
    return calibration


def synchronization(frame, prefix, resume):
    fields = ['mode', 'invest_prob_C', 'invest_prob_U', 'expected_tau_C_conditional',
              'expected_tau_U_conditional'] + [c for c in frame if c.startswith('mass_action_')]
    fields += ['mass_asymmetric_invest_action', 'mean_annual_asymmetric_built_state_probability',
               'expected_asymmetric_built_years', 'max_year_asymmetric_probability']
    if 'scenario_id' in frame:
        fields.insert(0, 'scenario_id')
    if not np.allclose(frame[[c for c in frame if c.startswith('mass_action_')]].sum(axis=1),
                       30, atol=1e-12, rtol=0):
        raise RuntimeError('SYNCHRONIZATION_ACTION_MASS_FAILURE')
    if not np.allclose(frame.expected_asymmetric_built_years,
                       30*frame.mean_annual_asymmetric_built_state_probability, atol=1e-12, rtol=0):
        raise RuntimeError('SYNCHRONIZATION_YEAR_IDENTITY_FAILURE')
    summary = {mode: summarize_mode(group) for mode, group in frame.groupby('mode')}
    save_csv(FORMAL/'diagnostics'/f'{prefix}.csv', frame[fields], resume)
    save_json(FORMAL/'diagnostics'/f'{prefix}_summary.json', summary, resume)
    return summary


def validate_additional_outputs(frame):
    for mode, group in frame.groupby('mode'):
        for target in TARGETS[mode]:
            if target.startswith('commit_now_') and not np.isfinite(group[target]).all():
                raise RuntimeError('NONFINITE_COMMIT_NOW_VALUE')


def boundary_job(job):
    mode, variable, z = job
    return solve_scenario(dict(BASELINE, **{variable: z}), mode)


def boundaries(resume):
    folder = FORMAL/'boundaries_v2'
    rows = []
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 1)) as executor:
        for variable, (lower, upper) in zip(FEATURES, DOMAIN):
            grid = lower + np.arange(1001)*(upper-lower)/1000
            for mode in MODES:
                label = f'{variable}__{mode}'
                path = folder/'exact_grid'/f'{label}.csv'
                meta_path = path.with_suffix('.json')
                if path.exists():
                    meta = read_json(meta_path)
                    if not resume or meta['identity'] != identity() or sha256(path) != meta['sha256']:
                        raise RuntimeError('BOUNDARY_GRID_RESUME_MISMATCH')
                    frame = pd.read_csv(path, float_precision='round_trip')
                else:
                    results = list(executor.map(boundary_job, [(mode, variable, float(z)) for z in grid], chunksize=1))
                    frame = pd.DataFrame(results)
                    validate_additional_outputs(frame)
                    write_csv(path, frame)
                    write_json(meta_path, dict(identity=identity(), sha256=sha256(path), points=1001))
                if len(frame) != 1001 or not np.array_equal(frame[variable].to_numpy(), grid):
                    raise RuntimeError('BOUNDARY_GRID_DEFINITION_MISMATCH')
                cache = {float(z): row for z, row in zip(grid, frame.to_dict('records'))}
                applicable = list(BOUNDARY_TARGETS) if mode == 'TRANSFER' else (
                    [k for k in BOUNDARY_TARGETS if k != 'STORAGE_FEE_ZERO'] if mode == 'JOINT_VENTURE'
                    else ['COMMIT_NOW_SYSTEM_NPV_ZERO', 'C_INVEST_PROB_50', 'U_INVEST_PROB_50'])
                targets = applicable if variable == 'carbon_scale' else ['COMMIT_NOW_SYSTEM_NPV_ZERO', 'C_INVEST_PROB_50', 'U_INVEST_PROB_50']
                for boundary_type in targets:
                    target, level = BOUNDARY_TARGETS[boundary_type]
                    record_path = folder/'verification'/f'{label}__{boundary_type}.json'
                    if record_path.exists():
                        record = read_json(record_path)
                        if not resume or record['identity'] != identity() or record['grid_hash'] != sha256(path):
                            raise RuntimeError('BOUNDARY_RECORD_RESUME_MISMATCH')
                    else:
                        def exact(z):
                            if z not in cache:
                                cache[z] = solve_scenario(dict(BASELINE, **{variable: z}), mode)
                            return cache[z][target]
                        found = exact_grid_search(exact, lower, upper, level, target.startswith('invest_prob_'))
                        y = np.asarray(found['responses'])
                        finite = np.flatnonzero(np.isfinite(y))
                        closest = int(finite[np.argmin(abs(y[finite]-level))]) if len(finite) else None
                        diagnostic = dict(min_response=float(y[finite].min()) if len(finite) else None,
                                          max_response=float(y[finite].max()) if len(finite) else None,
                                          closest_point=float(grid[closest]) if closest is not None else None,
                                          closest_response=float(y[closest]) if closest is not None else None,
                                          left_endpoint_response=float(y[0]), right_endpoint_response=float(y[-1]))
                        result_rows = found['roots'] or [dict(found=False, root_count=0, root_index=None,
                                                            explanation=found['explanation'])]
                        for row in result_rows:
                            row.update(mode=mode, variable=variable, boundary_type=boundary_type, **diagnostic)
                        record = dict(identity=identity(), grid_hash=sha256(path), rows=result_rows,
                                      refinement_evaluations=found['refinement_evaluations'])
                        write_json(record_path, record)
                    rows.extend(record['rows'])
                print('BOUNDARY_V2 '+label, flush=True)
    result = pd.DataFrame(rows)
    if result.groupby(['variable', 'mode', 'boundary_type']).ngroups != 61:
        raise RuntimeError('BOUNDARY_SEARCH_COUNT_MISMATCH')
    save_csv(folder/'boundary_results.csv', result, resume)
    return result


def artifact_hashes():
    excluded = {'reproducibility_manifest.json', 'completion.json', 'resume_validation.json'}
    return {str(p.relative_to(FORMAL)).replace('\\', '/'): sha256(p)
            for p in sorted(FORMAL.rglob('*')) if p.is_file() and p.name not in excluded}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', action='store_true')
    resume = parser.parse_args().resume
    current = 'PREFLIGHT'
    try:
        frozen = provenance()
        lock = FORMAL/'source_run_lock.json'
        if lock.exists():
            if not resume or read_json(lock) != frozen:
                raise RuntimeError('SOURCE_RUN_IDENTITY_MISMATCH')
        else:
            if resume or git('status', '--porcelain'):
                raise RuntimeError('SOURCE_CODE_NOT_CLEAN_AND_FROZEN')
            write_json(lock, frozen)
        if resume and (FORMAL/'reproducibility_manifest.json').exists():
            saved_manifest = read_json(FORMAL/'reproducibility_manifest.json')
            completion = read_json(FORMAL/'completion.json')
            if (sha256(FORMAL/'reproducibility_manifest.json') != completion['manifest_sha256']
                    or saved_manifest['artifacts_sha256'] != artifact_hashes()):
                raise RuntimeError('PRE_RESUME_ARTIFACT_HASH_MISMATCH')
        preflight = tests()
        if not (FORMAL/'source_preflight.json').exists():
            write_json(FORMAL/'source_preflight.json', preflight)
        current = 'SOURCE_AUDIT'
        calibration = validate_source()
        gate('SOURCE_AUDIT_GATE', dict(unresolved=0), resume)
        gate('CARBON_CALIBRATION_GATE', calibration, resume)
        gate('CONFIG_FREEZE', frozen, resume)
        current = 'BASELINE'
        base = baseline(FORMAL, resume)
        validate_additional_outputs(base)
        save_csv(FORMAL/'baseline/source_backed_baseline_summary.csv', base, resume)
        gate('BASELINE_GATE', dict(mode_count=3), resume)
        current = 'SYNCHRONIZATION_DIAGNOSIS'
        synchronization(base, 'baseline_synchronization', resume)
        gate('SYNCHRONIZATION_DIAGNOSTIC_GATE', dict(baseline_modes=3), resume)
        current = 'EXACT_DATASET'
        exact = build_dataset(FORMAL, resume)
        validate_rows(exact, range(4096))
        validate_additional_outputs(exact)
        gate('EXACT_DATASET_GATE', dict(rows=len(exact), scenarios=4096), resume)
        gate('EXACT_INTEGRITY_GATE', dict(solver_OK=12288), resume)
        sync = synchronization(exact, 'investment_synchronization', resume)
        current = 'SURROGATE'
        measured, failures = fit_surrogates(FORMAL, exact, resume)
        collisions = []
        for mode in MODES:
            subset = exact[exact['mode'] == mode].sort_values('scenario_id')
            for a, b in [('invest_prob_C', 'invest_prob_U'), ('expected_tau_C_conditional', 'expected_tau_U_conditional')]:
                directory = FORMAL/'surrogate/models'
                status = check_identical_target_hashes(subset[a], subset[b], sha256(directory/f'{mode}__{a}.joblib'), sha256(directory/f'{mode}__{b}.joblib'))
                collisions.append(dict(mode=mode, targets=[a, b], status=status))
        save_json(FORMAL/'diagnostics/identical_target_hashes.json', collisions, resume)
        if failures:
            raise RuntimeError('GATE_SURROGATE_FAIL: '+str(failures))
        gate('SURROGATE_GATE', dict(targets=33, passed=33), resume)
        current = 'BOUNDARY_V2'
        boundary = boundaries(resume)
        gate('BOUNDARY_V2_GATE', dict(searches=61, exact_grid_points=1001), resume)
        current = 'FINAL_TESTS'
        tests()
        if provenance() != frozen:
            raise RuntimeError('FINAL_PROVENANCE_MISMATCH')
        current = 'FINAL_REPORT'
        report = FORMAL/'FINAL_EXECUTION_REPORT.md'
        if not report.exists():
            registry = pd.read_csv(ROOT/'config/parameter_registry.source_backed.csv').fillna('')
            parts = ['# Source-backed formal results', '## Empirical Source Audit',
                     registry.to_csv(index=False),
                     'The method-validation run verifies numerical correctness.\nThe source-backed run is the paper-facing empirical calibration.',
                     (ROOT/'docs/SOURCE_BACKED_SCALAR_SUMMARY.md').read_text(encoding='utf-8'),
                     '## Official carbon calibration', json.dumps(calibration, indent=2),
                     '## Baseline', base.to_string(index=False), '## Synchronization', json.dumps(sync, indent=2),
                     '## Exact dataset', '4096 scenarios;12288 rows; all solver checks pass.',
                     '## Surrogate metrics', measured[measured.split == 'test'].to_string(index=False),
                     '## Boundary V2', boundary.to_string(index=False),
                     'No crossing on the prescribed grid is not proof of global absence. Jump brackets are not exact roots.',
                     'Static accounting tolerance is100CNY by explicit user decision; other gates retain their original tolerances.',
                     '## Provenance', json.dumps(frozen, indent=2)]
            write_text(report, '\n\n'.join(parts))
        gate('FINAL_REPRODUCIBILITY_GATE', dict(identity_verified=True), resume)
        snapshot = artifact_hashes()
        manifest_path = FORMAL/'reproducibility_manifest.json'
        if manifest_path.exists():
            previous = read_json(manifest_path)
            if previous['provenance'] != frozen or previous['artifacts_sha256'] != snapshot:
                raise RuntimeError('FINAL_ARTIFACT_RESUME_HASH_MISMATCH')
            if not (FORMAL/'resume_validation.json').exists():
                write_json(FORMAL/'resume_validation.json', dict(status='PASS', unchanged_files=len(snapshot)))
            (FORMAL/'completion.json').write_text(json.dumps(dict(status='ALL_STAGES_COMPLETED',
                manifest_sha256=sha256(manifest_path), resume_unchanged_files=len(snapshot)), indent=2), encoding='utf-8')
        else:
            write_json(manifest_path, dict(provenance=frozen, source_files_sha256=source_manifest(), artifacts_sha256=snapshot))
            write_json(FORMAL/'completion.json', dict(status='FORMAL_RUN_COMPLETE_RESUME_PENDING', manifest_sha256=sha256(manifest_path)))
        print('SOURCE_BACKED_RUN_PASS', flush=True)
        return 0
    except Exception as exc:
        message = f'{current}: {type(exc).__name__}: {exc}'
        print(message, flush=True)
        path = FORMAL/'SOURCE_BACKED_EXECUTION_STOP.json'
        if not path.exists():
            write_json(path, dict(stage=current, error=str(exc), identity=provenance()))
        append_progress('## Source-backed execution stopped\n\n'+message+'\nNo downstream stage executed.')
        return 1
