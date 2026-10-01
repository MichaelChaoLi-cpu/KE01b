"""Execute approved number-only edits with the installed Kila helper."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
helper=ROOT/'.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py'
proposal=(ROOT/'Rev/docs/R2C3-method-workflow-proposal.md').read_text()
out=ROOT/'Rev/docs/r2c3-edit-specs'
out.mkdir(exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');args=ap.parse_args()
for match in re.finditer(r'## Part (\d+) — (?:callout|caption) renumbering\n(.*?)(?=\n## |\Z)',proposal,re.S):
    n=int(match[1]);text=match[2]
    before=re.search(r'^Target: "(.+)"$',text,re.M)[1]
    after=re.search(r'^Replace with: "(.+)"$',text,re.M)[1]
    spec=dict(schema_version=1,comment_id='reviewer-2/comment-3',part_id=f'part-{n:02d}',
        location=re.search(r'^Location: (.+)$',text,re.M)[1],reason='Renumber existing figure after workflow Figure 1 insertion.',
        decision_ids=['KILA-D-20260930-020'],mode='replace',before=before,after=after,paragraph_anchor=before)
    file=out/f'part-{n:02d}.json';file.write_text(json.dumps(spec,indent=2)+'\n')
    cmd=[sys.executable,str(helper),'apply','--docx',str(ROOT/'Rev/revision/KE01b.rev.markup.docx'),
         '--log',str(ROOT/'Rev/docs/revisionchanges.md'),'--spec',str(file)]
    for dry in ([True,False] if args.apply else [True]):
        result=subprocess.run(cmd+(['--dry-run'] if dry else []),capture_output=True,text=True)
        (out/f'part-{n:02d}-{"dry" if dry else "applied"}.txt').write_text(result.stdout+result.stderr)
        print(f'part-{n:02d} {"dry" if dry else "applied"}: {result.returncode}',flush=True)
        if result.returncode:
            print(result.stdout,result.stderr);sys.exit(result.returncode)
