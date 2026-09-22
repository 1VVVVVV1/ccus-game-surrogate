"""Archive public CNEEEX COMCEA daily responses; never fill missing prices."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from pathlib import Path
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/source_backed_formal/source_audit/official_carbon_api'
URL = 'https://shyx.cneeex.com/gateway/common/queryMarketByDate'


def fetch(day):
    target = OUT / (day.strftime('%Y%m%d') + '.json')
    if target.exists():
        data = json.loads(target.read_text(encoding='utf-8'))
        if data.get('success'):
            return day.isoformat(), None
    payload = {'tradeDate': day.strftime('%Y%m%d'), 'goodsCode': 'COMCEA'}
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            raw = response.read()
        data = json.loads(raw)
        target.write_bytes(raw)
        if not data.get('success'):
            return day.isoformat(), data
        return day.isoformat(), None
    except Exception as exc:
        return day.isoformat(), str(exc)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    # Last complete trading day at retrieval (2026-09-21 11:08 Asia/Shanghai).
    start, end = date(2021, 7, 16), date(2026, 9, 18)
    days = [start + timedelta(days=i) for i in range((end-start).days+1)
            if (start + timedelta(days=i)).weekday() < 5]
    errors = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        pending = {pool.submit(fetch, day): day for day in days}
        for n, future in enumerate(as_completed(pending), 1):
            day, error = future.result()
            if error is not None:
                errors[day] = error
            if n % 100 == 0:
                print(f'{n}/{len(days)} requests, {len(errors)} errors', flush=True)
    manifest = {'source_url': URL, 'goods_code': 'COMCEA', 'start': str(start),
        'end': str(end), 'requested_weekdays': len(days), 'errors': errors,
        'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(OUT.glob('20*.json'))},
        'status': 'RAW_RESPONSES_ONLY_REQUIRES_COMPLETENESS_AUDIT'}
    (OUT / 'retrieval_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Finished: {len(days)} requests; {len(errors)} errors', flush=True)
