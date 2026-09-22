"""Require complete official weekday responses before exporting GBM calibration."""
from datetime import date, timedelta
from pathlib import Path
import csv
import hashlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.carbon_calibration import fit_official_gbm


def main():
    audit = ROOT / 'results/source_backed_formal/source_audit'
    raw = audit / 'official_carbon_api'
    holidays_path = audit / 'scalar_followup/holidays.json'
    holidays = set(json.loads(holidays_path.read_text(encoding='utf-8')))
    fallback_path = raw / 'official_article_fallbacks.json'
    fallbacks = json.loads(fallback_path.read_text(encoding='utf-8')) if fallback_path.exists() else {}
    start, end = date(2021, 7, 16), date(2026, 9, 18)
    rows, issues, files, closed = [], [], {}, []
    for offset in range((end-start).days+1):
        day = start + timedelta(days=offset)
        if day.weekday() >= 5:
            continue
        path = raw / (day.strftime('%Y%m%d')+'.json')
        if not path.exists():
            issues.append({'date': str(day), 'issue': 'missing_response'})
            continue
        files[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        data = json.loads(path.read_text(encoding='utf-8'))
        records = data.get('data')
        if not data.get('success') or not records:
            if str(day) in fallbacks:
                source = fallbacks[str(day)]
                article = raw / source['raw_file']
                close = float(source['close'])
                if (not source['source_url'].startswith('https://overview.cneeex.com/')
                        or hashlib.sha256(article.read_bytes()).hexdigest() != source['sha256']
                        or not math.isfinite(close) or close <= 0):
                    issues.append({'date': str(day), 'issue': 'invalid_official_article_provenance'})
                else:
                    files[article.name] = source['sha256']
                    rows.append({'date': str(day), 'close': source['close']})
            elif str(day) in holidays:
                closed.append(str(day))
            else:
                issues.append({'date': str(day), 'issue': 'no_quote_on_expected_trading_day'})
            continue
        if len(records) != 1:
            issues.append({'date': str(day), 'issue': 'unexpected_record_count'})
            continue
        record = records[0]
        if record.get('subjCode') != 'COMCEA' or record.get('quotPoin') != day.strftime('%Y%m%d'):
            issues.append({'date': str(day), 'issue': 'quote_identity_mismatch'})
            continue
        close = float(record['closPric'])
        if not math.isfinite(close) or close <= 0:
            issues.append({'date': str(day), 'issue': 'invalid_close'})
            continue
        rows.append({'date': str(day), 'close': record['closPric']})
    report = {'status': 'COMPLETE' if not issues else 'INCOMPLETE',
              'observations': len(rows), 'issues': issues, 'official_closed_days': closed,
              'holiday_file_sha256': hashlib.sha256(holidays_path.read_bytes()).hexdigest(),
              'official_article_fallbacks': fallbacks,
              'raw_response_sha256': files}
    (raw/'completeness_audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    if issues:
        print(f'Incomplete: {len(rows)} quotes, {len(issues)} unresolved dates; no calibration exported')
        return 1
    output = ROOT / 'results/source_backed_formal/calibration'
    output.mkdir(exist_ok=True)
    series = output/'carbon_price_series.csv'
    with series.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'close'])
        writer.writeheader()
        writer.writerows(rows)
    result, diagnostics = fit_official_gbm([r['date'] for r in rows], [r['close'] for r in rows])
    result['official_input_sha256'] = hashlib.sha256(series.read_bytes()).hexdigest()
    result['source_url'] = 'https://shyx.cneeex.com/gateway/common/queryMarketByDate'
    result['goods_code'] = 'COMCEA'
    (output/'carbon_gbm_calibration.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    with (output/'carbon_gbm_diagnostics.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(diagnostics[0]))
        writer.writeheader()
        writer.writerows(diagnostics)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
