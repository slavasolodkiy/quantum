"""Run one authorized Atlas job; credentials stay in process memory only."""
import getpass
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone
import poe

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence'
OUT.mkdir(exist_ok=True)
API = 'https://api.mothquantum.com/api/v1'

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2), encoding='utf-8')

def call(path, key, body=None):
    request = urllib.request.Request(API + path,
        data=None if body is None else json.dumps(body).encode(),
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
                 'User-Agent': 'proof-of-exit/1.0', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        payload = error.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'HTTP {error.code}: {payload[:3000]}') from None

key = getpass.getpass('Atlas API key (not stored): ')
engine = call('/engines/graph-v1', key)
save('atlas-engine-live.json', engine)
print(json.dumps(engine, indent=2), flush=True)
print('PREFLIGHT COMPLETE. Type RUN to create exactly one emu job.', flush=True)
if input().strip() != 'RUN':
    raise SystemExit('Run not authorized by controller')
proved, proof_ms, proof_method = poe.theorem_proved()
assert proved
shots = 4096
body = {'mode': 'emu', 'params': {
    'num_qubits': poe.N,
    'coupling_map': [list(edge) for edge in poe.DOORS],
    'operations': [{'type': 'relationship', 'qubits': [u, v],
                    'paulis': {'ZZ': 0.0 if (u, v) in poe.COIN_DOORS else 1.0}}
                   for u, v in poe.DOORS],
    'shots': shots}}
save('atlas-request.json', {'method': 'POST', 'url': API + '/engines/graph-v1/process',
                          'body': body, 'credential_headers_omitted': True,
                          'recorded_at': datetime.now(timezone.utc).isoformat()})
created = call('/engines/graph-v1/process', key, body)
save('atlas-created.json', created)
job_id = created['job_id']
print('CREATED JOB: ' + job_id, flush=True)
for attempt in range(300):
    status = call('/jobs/' + job_id + '/status', key)
    save('atlas-status.json', status)
    with (OUT / 'atlas-status-history.jsonl').open('a', encoding='utf-8') as log:
        log.write(json.dumps(status) + '\n')
    print('STATUS: ' + status.get('status', 'unknown'), flush=True)
    if status.get('status') in ('completed', 'failed', 'cancelled'):
        break
    time.sleep(3)
else:
    raise SystemExit('Job remains unfinished; use saved ID to resume polling, do not resubmit.')
if status['status'] != 'completed':
    raise SystemExit('Atlas job did not complete: ' + json.dumps(status))
raw = call('/jobs/' + job_id + '/result', key)
save('atlas-raw-result.json', raw)
key = None
save('atlas-run-summary.json', {'job_id': job_id, 'engine_id': 'graph-v1', 'mode': 'emu',
     'status': status['status'], 'shots_requested': shots, 'theorem_proved': proved,
     'proof_ms': proof_ms, 'proof_method': proof_method})
print('REAL ATLAS JOB: PASS\nRAW JSON SAVED', flush=True)
print(json.dumps(raw, indent=2), flush=True)
