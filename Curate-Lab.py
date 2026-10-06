"""Run the provided curator workflow and retain its unedited model response."""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from langchain_core.callbacks import UsageMetadataCallbackHandler
from lab.curator import curate_skills
from lab.model import make_model
from lab.tasks import ROOT

parser = argparse.ArgumentParser()
parser.add_argument('--attempt', type=int, choices=[1, 2, 3], required=True)
args = parser.parse_args()
report = ROOT / 'report'
usage = UsageMetadataCallbackHandler()
model = make_model()
audit = {'attempt': args.attempt, 'timestamp': datetime.now(timezone.utc).isoformat(),
         'model': model.model, 'error': None, 'skills': []}
start = time.monotonic()


class RecordingModel:
    def invoke(self, prompt):
        (report / f'curator-input-{args.attempt}.txt').write_text(prompt, encoding='utf-8')
        response = model.invoke(prompt, config={'callbacks': [usage]})
        (report / f'curator-response-{args.attempt}.md').write_text(response.text, encoding='utf-8')
        return response


try:
    audit['skills'] = [str(p) for p in curate_skills(model=RecordingModel())]
    print('Written skills:', audit['skills'], flush=True)
except Exception as exc:
    audit['error'] = f'{type(exc).__name__}: {exc}'
    raise
finally:
    audit['seconds'] = round(time.monotonic() - start, 1)
    audit['usage'] = usage.usage_metadata
    (report / f'curator-run-{args.attempt}.json').write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
