from pathlib import Path
import hashlib, json, math, subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / 'results' / 'source_backed_formal'
OUT = Path(__file__).resolve().parent
TABLE = OUT / 'tables'; FIG = OUT / 'figures'; AUDIT = OUT / 'audit'
for d in (TABLE, FIG, AUDIT): d.mkdir(parents=True, exist_ok=True)

def sha(path):
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def snapshot():
    return {str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in FORMAL.rglob('*') if p.is_file()}

before=snapshot()
frozen=json.loads((FORMAL/'reproducibility_manifest.json').read_text(encoding='utf-8'))
for section in ['source_files_sha256','artifacts_sha256']:
    for rel, expected in frozen[section].items():
        p=ROOT/rel
        if not p.exists(): p=FORMAL/rel
        assert sha(p)==expected, (section,rel)
assert subprocess.check_output(['git','-c','safe.directory='+ROOT.as_posix(),'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==frozen['provenance']['git_commit']
assert sha(ROOT/'config/model_config.source_backed.json')==frozen['provenance']['config_sha256']
(AUDIT/'formal_before.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
config=json.loads((ROOT/'config/model_config.source_backed.json').read_text(encoding='utf-8'))

baseline = pd.read_csv(FORMAL/'baseline'/'source_backed_baseline_summary.csv')
exact = pd.read_csv(FORMAL/'exact_dataset'/'exact_equilibrium_outputs.csv')
scen = pd.read_csv(FORMAL/'exact_dataset'/'exact_scenarios.csv')
bound = pd.read_csv(FORMAL/'boundaries_v2'/'boundary_results.csv')
sync = pd.read_csv(FORMAL/'diagnostics'/'baseline_synchronization.csv')
assert len(exact)==12288 and len(scen)==4096 and len(bound)==61
assert not exact.duplicated(['scenario_id','mode']).any()
assert exact.solver_status.eq('OK').all() and not bound.found.any()
features=list(config['scenario_domain'])
grids={(p.stem.split('__')[1],p.stem.split('__')[0]):pd.read_csv(p) for p in (FORMAL/'boundaries_v2/exact_grid').glob('*.csv')}
assert len(grids)==18 and all(len(g)==1001 for g in grids.values())
option_stats=[]; quartiles=[]

baseline['option_value'] = baseline.system_npv - baseline.commit_now_system_npv
baseline['option_value_pct_commit'] = 100*baseline.option_value/baseline.commit_now_system_npv
baseline.to_csv(TABLE/'baseline_comparison.csv', index=False)
cols=['mode','system_npv','commit_now_system_npv','option_value','option_value_pct_commit','invest_prob_C','invest_prob_U','expected_tau_C_conditional','expected_tau_U_conditional','expected_active_years']
baseline[cols].to_csv(TABLE/'dynamic_commit_option_value.csv', index=False)
sync.to_csv(TABLE/'synchronization_diagnostic.csv', index=False)

# Exact-scenario signed timing increment and parameter associations.
for mode, g in exact.groupby('mode'):
    g=g.copy(); g['option_value']=g.system_npv-g.commit_now_system_npv
    g['prob_gap']=g.invest_prob_U-g.invest_prob_C
    g['tau_gap']=g.expected_tau_U_conditional-g.expected_tau_C_conditional
    g['asym_mass']=g.mass_asymmetric_invest_action
    rows=[]
    for p in ['transport_market_price','effective_abatement_fraction','storage_subsidy','capex_C_multiplier','capex_U_multiplier','carbon_scale']:
        for y in ['option_value','prob_gap','tau_gap','asym_mass']:
            varying=g[y].nunique()>1
            rows.append({'mode':mode,'parameter':p,'response':y,'spearman':g[p].corr(g[y],method='spearman') if varying else np.nan,'pearson':g[p].corr(g[y]) if varying else np.nan})
    pd.DataFrame(rows).to_csv(TABLE/f'{mode.lower()}_parameter_associations.csv',index=False)
    if mode=='JOINT_VENTURE':
        for p in features:
            for q,h in g.groupby(pd.qcut(g[p],4,labels=False),observed=True):
                quartiles.append(dict(parameter=p,quartile=int(q)+1,n=len(h),parameter_min=h[p].min(),parameter_max=h[p].max(),mean_prob_gap=h.prob_gap.mean(),mean_tau_gap=h.tau_gap.mean(),mean_asym_mass=h.asym_mass.mean(),share_asym=(h.asym_mass>1e-12).mean()))
        g['capex_C_bin']=pd.qcut(g.capex_C_multiplier,4,labels=False,duplicates='drop')
        g['capex_U_bin']=pd.qcut(g.capex_U_multiplier,4,labels=False,duplicates='drop')
        g['carbon_bin']=pd.qcut(g.carbon_scale,4,labels=False,duplicates='drop')
        g['eta_bin']=pd.qcut(g.effective_abatement_fraction,4,labels=False,duplicates='drop')
        for a,b in [('capex_C_bin','capex_U_bin'),('carbon_bin','eta_bin')]:
            g.groupby([a,b],observed=True).agg(n=('scenario_id','size'),mean_prob_gap=('prob_gap','mean'),mean_asym_mass=('asym_mass','mean'),share_asym=('asym_mass',lambda x:(x>1e-12).mean())).reset_index().to_csv(TABLE/f'JV_{a}_{b}_regions.csv',index=False)
        g.sort_values('asym_mass',ascending=False).head(20).to_csv(TABLE/'JV_high_asymmetry_scenarios.csv',index=False)
    option_stats.append(dict(mode=mode,n=len(g),min_option=g.option_value.min(),max_option=g.option_value.max(),mean_option=g.option_value.mean(),negative_beyond_1e_8=int((g.option_value < -1e-8).sum()),positive_beyond_1e_8=int((g.option_value > 1e-8).sum()),max_prob_gap_abs=g.prob_gap.abs().max(),max_tau_gap_abs=g.tau_gap.abs().max(),max_asym_mass=g.asym_mass.max()))
pd.DataFrame(option_stats).to_csv(TABLE/'exact_option_and_sync_summary.csv',index=False)
pd.DataFrame(quartiles).to_csv(TABLE/'JV_parameter_quartiles.csv',index=False)

# Baseline JV annual built/action diagnostic from the persisted audit JSON.
jv=json.loads((FORMAL/'baseline'/'JOINT_VENTURE.json').read_text(encoding='utf-8'))
audit=jv.get('audit',{})
pd.DataFrame(audit.get('investment_time_probabilities',[])).to_csv(TABLE/'JV_baseline_investment_time_probabilities.csv',index=False)
annual=np.asarray(audit.get('investment_time_probabilities',[]),dtype=float)
if annual.shape==(30,2):
    pd.DataFrame({'year':np.arange(30),'C_action_mass':annual[:,0],'U_action_mass':annual[:,1],'asymmetric_action_mass':np.abs(annual[:,0]-annual[:,1])}).to_csv(TABLE/'JV_baseline_annual_actions.csv',index=False)
reachable=pd.DataFrame(audit.get('reachable_policy',[]))
policy=pd.DataFrame(audit.get('policy',[]))
if not reachable.empty:
    reachable.to_csv(TABLE/'JV_baseline_reachable_policy.csv',index=False)
if not policy.empty:
    policy.to_csv(TABLE/'JV_baseline_policy.csv',index=False)

# Boundary proximity: never compare unlike units in one rank. Thresholds are part of target names.
def threshold(target):
    if target.endswith('_50'): return .5
    if target.endswith('_ZERO'): return 0.0
    return 0.0
bound['threshold']=bound.boundary_type.map(threshold)
bound['min_abs_distance']=np.minimum(abs(bound.min_response-bound.threshold),abs(bound.max_response-bound.threshold))
bound['min_signed_distance']=np.where(abs(bound.min_response-bound.threshold)<=abs(bound.max_response-bound.threshold),bound.min_response-bound.threshold,bound.max_response-bound.threshold)
bound['threshold_side']=np.where((bound.min_response-bound.threshold)*(bound.max_response-bound.threshold)>0,np.where(bound.min_response>bound.threshold,'above','below'),'touch_or_bracket')
bound['direction']=np.where(bound.right_endpoint_response>bound.left_endpoint_response,'increasing',np.where(bound.right_endpoint_response<bound.left_endpoint_response,'decreasing','flat_endpoints'))
bound['metric_family']=np.where(bound.boundary_type.str.contains('PROB'), 'probability',np.where(bound.boundary_type.str.contains('PRICE|FEE'),'price_CNY_per_t','NPV_million_CNY'))
target_cols={'COMMIT_NOW_SYSTEM_NPV_ZERO':'commit_now_system_npv','COMMIT_NOW_C_VALUE_ZERO':'commit_now_value_C','COMMIT_NOW_U_VALUE_ZERO':'commit_now_value_U','C_INVEST_PROB_50':'invest_prob_C','U_INVEST_PROB_50':'invest_prob_U','CO2_PRICE_ZERO':'mean_co2_price_conditional','STORAGE_FEE_ZERO':'mean_storage_fee_conditional'}
for i,r in bound.iterrows():
    grid=grids[(r['mode'],r.variable)]; y=grid[target_cols[r.boundary_type]].to_numpy(); d=np.diff(y)
    assert np.isfinite(y).all()
    tol=64*np.finfo(float).eps*max(1.,np.max(abs(y)))
    up=int((d>tol).sum()); down=int((d < -tol).sum()); closest=int(np.argmin(abs(y-r.threshold)))
    bound.loc[i,'min_abs_distance']=abs(y[closest]-r.threshold)
    bound.loc[i,'closest_point']=grid.iloc[closest][r.variable]
    bound.loc[i,'closest_response']=y[closest]
    bound.loc[i,'increasing_steps']=up; bound.loc[i,'decreasing_steps']=down
    bound.loc[i,'descriptive_flat_tolerance']=tol
    bound.loc[i,'monotonicity']='nonmonotonic' if up and down else 'nondecreasing' if up else 'nonincreasing' if down else 'numerically_flat'
    assert np.isclose(y.min(),r.min_response,atol=1e-8,rtol=0) and np.isclose(y.max(),r.max_response,atol=1e-8,rtol=0)
bound.sort_values(['metric_family','min_abs_distance']).to_csv(TABLE/'boundary_proximity_all61.csv',index=False)
bound['rank_within_unit']=bound.groupby('metric_family').min_abs_distance.rank(method='min').astype(int)
bound.sort_values(['metric_family','rank_within_unit']).to_csv(TABLE/'boundary_proximity_ranked_by_unit.csv',index=False)

# Source/input audit manifest. Formal hash list is captured without altering formal files.
inputs=[FORMAL/'FINAL_EXECUTION_REPORT.md',ROOT/'PROJECT_PROGRESS.md',FORMAL/'baseline'/'source_backed_baseline_summary.csv',FORMAL/'exact_dataset'/'exact_scenarios.csv',FORMAL/'exact_dataset'/'exact_equilibrium_outputs.csv',FORMAL/'boundaries_v2'/'boundary_results.csv',FORMAL/'diagnostics'/'baseline_synchronization.csv']
manifest={'git_commit':'bc0d0fe4d2fff35a32caae1e74f87e1ea74f0786','config_sha256':'8c7501f0ee4a27fa8f13c561a9b2205888b7c6660cbef88f83df256b3583ac5c','source_sha256':'a4af0372bad0729fd178cc2f1107ba683b6eb6406e6d7b790475058b4afe6e3d','registry_sha256':'43b07f4c82a0485f6e4502385c99919eef704643623211ccc756d0b353f8834f','official_carbon_csv_sha256':'a5e60f21e0c065a4c3ef361274c7dfbc8a8d1664ee133cad979286462494000e','input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in inputs},'exact_rows':len(exact),'scenario_rows':len(scen),'boundary_rows':len(bound)}
(AUDIT/'analysis_input_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# Figures (deterministic, no inferential error bars).
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':9,'axes.labelsize':8})
colors={'TRANSFER':'#2166ac','JOINT_VENTURE':'#b2182b','STATE_OWNED':'#4d9221'}
fig,ax=plt.subplots(1,3,figsize=(10,3.1),constrained_layout=True)
x=np.arange(3); modes=baseline['mode'].tolist()
for i,m in enumerate(modes):
    r=baseline[baseline['mode']==m].iloc[0]; c=colors[m]
    ax[0].bar(i-.16,r.invest_prob_C,.32,color=c,label=m.replace('_',' ')); ax[0].bar(i+.16,r.invest_prob_U,.32,color=c,alpha=.45)
    ax[1].bar(i,r.option_value,color=c); ax[2].bar(i,r.expected_tau_C_conditional,color=c); ax[2].bar(i,r.expected_tau_U_conditional,color=c,alpha=.45)
for a in ax: a.set_xticks(x,modes); a.tick_params(axis='x',rotation=25); a.grid(axis='y',alpha=.25)
ax[0].set_ylim(0,1.05); ax[0].set_ylabel('Investment probability'); ax[0].set_title('C solid, U translucent')
ax[1].set_ylabel('Dynamic − commit-now NPV (million CNY)'); ax[1].set_title('Signed timing increment')
ax[2].set_ylabel('Conditional investment year'); ax[2].set_title('Investment timing')
fig.savefig(FIG/'fig1_baseline_timing_option.png',dpi=400); fig.savefig(FIG/'fig1_baseline_timing_option.svg'); plt.close(fig)

fig,ax=plt.subplots(1,2,figsize=(8,3.1),constrained_layout=True)
jvtime=pd.DataFrame(audit.get('investment_time_probabilities',[]))
if not jvtime.empty:
    # accept either long or wide persisted schema
    if 'year' in jvtime.columns:
        for c in [c for c in jvtime.columns if c!='year']: ax[0].plot(jvtime.year,jvtime[c],label={'0':'C action','1':'U action'}.get(c,c))
    else:
        for c in jvtime.columns:
            if c not in ('t','year'): ax[0].plot(jvtime.index,jvtime[c],label={'0':'C action','1':'U action'}.get(c,c))
ax[0].set_title('JV baseline annual investment mass'); ax[0].set_xlabel('Decision year'); ax[0].set_ylabel('Probability mass'); ax[0].legend(fontsize=7); ax[0].grid(alpha=.25)
jv_exact=exact[exact['mode']=='JOINT_VENTURE']
ax[1].scatter(jv_exact.carbon_scale,jv_exact.mass_asymmetric_invest_action,s=5,c=jv_exact.effective_abatement_fraction,cmap='viridis'); ax[1].set_xlabel('Carbon-price scale'); ax[1].set_ylabel('Cumulative asymmetric action mass'); ax[1].set_title('JV exact scenarios'); ax[1].grid(alpha=.25)
fig.savefig(FIG/'fig2_jv_asynchrony.png',dpi=400); fig.savefig(FIG/'fig2_jv_asynchrony.svg'); plt.close(fig)

fig,ax=plt.subplots(2,2,figsize=(7.2,5.1),constrained_layout=True)
for col,var in enumerate(['carbon_scale','capex_U_multiplier']):
    for m in modes:
        g=grids[(m,var)]
        ax[0,col].plot(g[var],g.system_npv,color=colors[m],label=m.replace('_',' '))
        ax[1,col].plot(g[var],g.invest_prob_C,color=colors[m])
        ax[1,col].plot(g[var],g.invest_prob_U,color=colors[m],ls='--')
    for row in range(2):
        ax[row,col].set_xlabel(var); ax[row,col].grid(alpha=.2)
    ax[0,col].set_ylabel('System NPV (million CNY)'); ax[0,col].legend(fontsize=6)
    ax[1,col].set_ylabel('Investment probability'); ax[1,col].set_title('C solid; U dashed')
fig.savefig(FIG/'fig3_key_response_curves.png',dpi=400); fig.savefig(FIG/'fig3_key_response_curves.svg'); plt.close(fig)

after=snapshot()
changed=[k for k in before if before[k]!=after.get(k)]
assert not changed, changed
(AUDIT/'formal_after.json').write_text(json.dumps(after,indent=2),encoding='utf-8')

print(json.dumps({'baseline':baseline[cols].to_dict('records'),'boundary_metric_counts':bound.metric_family.value_counts().to_dict(),'output':str(OUT)},ensure_ascii=False,indent=2))
