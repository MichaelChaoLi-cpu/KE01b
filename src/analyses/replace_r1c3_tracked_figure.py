"""One-picture tracked replacement, explicitly authorized in KILA-D-20260930-015.

Reuses Kila package validation and backup conventions. Refuses any picture run
that is not a standalone untracked inline drawing immediately before its caption.
"""
import argparse
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile
from lxml import etree as E
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('kila', ROOT/'.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py')
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)
NS = dict(k.NS, wp='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
          a='http://schemas.openxmlformats.org/drawingml/2006/main',
          r='http://schemas.openxmlformats.org/officeDocument/2006/relationships')
REL='http://schemas.openxmlformats.org/package/2006/relationships'
def serial(x): return E.tostring(x, method='c14n')

def replace(n, apply=False):
    path=ROOT/'Rev/revision/KE01b.rev.markup.docx'
    asset=ROOT/f'data/exp/r1c3_revised_figures/Figure_{n:02d}.png'
    log=ROOT/'Rev/docs/revisionchanges.md'
    part=f'figure-{n:02d}'
    k.ensure_part_is_new(log.read_text(), 'reviewer-1/comment-3', part)
    infos,files=k.read_package(path)
    before=k.sha256_path(path)
    root=E.fromstring(files['word/document.xml'])
    rels=E.fromstring(files['word/_rels/document.xml.rels'])
    pars=root.findall('.//w:p',NS)
    captions=[p for p in pars if k.paragraph_text(p).startswith(f'Figure {n}. ')]
    assert len(captions)==1, 'Caption must be unique'
    caption=captions[0]; p=caption.getprevious()
    runs=p.findall('w:r',NS)
    assert len(runs)==1 and len(p.findall('.//w:drawing',NS))==1
    run=runs[0]
    assert all(c.tag in (k.qn(k.W_NS,'rPr'),k.qn(k.W_NS,'drawing'),k.qn(k.W_NS,'lastRenderedPageBreak')) for c in run)
    assert not p.xpath('.//w:ins|.//w:del|.//w:hyperlink',namespaces=NS)
    assert run.find('w:drawing/wp:inline',NS) is not None
    original_root=copy.deepcopy(root)
    old_rev=[serial(x) for x in root.xpath('.//w:ins|.//w:del',namespaces=NS)]
    pp=serial(p.find('w:pPr',NS)) if p.find('w:pPr',NS) is not None else None
    newrun=copy.deepcopy(run)
    blip=newrun.find('.//a:blip',NS)
    oldrid=blip.get(k.qn(NS['r'],'embed'))
    oldtarget=next(x.get('Target') for x in rels if x.get('Id')==oldrid)
    rid=f'rIdR1C3Figure{n:02d}'
    media=f'word/media/r1c3_figure_{n:02d}.png'
    assert media not in files and not any(x.get('Id')==rid for x in rels)
    blip.set(k.qn(NS['r'],'embed'),rid)
    with Image.open(asset) as im: width,height=im.size
    assert width==3600
    cx=5486400;cy=round(cx*height/width)
    for ext in newrun.xpath('.//wp:extent|.//a:xfrm/a:ext',namespaces=NS):
        ext.set('cx',str(cx));ext.set('cy',str(cy))
    drawid=max(int(x.get('id')) for x in root.findall('.//wp:docPr',NS))+1
    newrun.find('.//wp:docPr',NS).set('id',str(drawid))
    roots=[E.fromstring(files[name]) for name in k.story_part_names(files)]
    cid=k.next_change_id(roots)
    when=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    deletion=k.make_change_wrapper('del',cid,'Mike C. Li',when)
    insertion=k.make_change_wrapper('ins',cid+1,'Mike C. Li',when)
    idx=p.index(run);p.remove(run);deletion.append(run);insertion.append(newrun)
    p.insert(idx,deletion);p.insert(idx+1,insertion)
    # Rejecting only this new pair must restore the entire original document XML.
    rejected=copy.deepcopy(root)
    ins=rejected.xpath(f'.//w:ins[@w:id="{cid+1}"]',namespaces=NS)[0]
    ins.getparent().remove(ins)
    dele=rejected.xpath(f'.//w:del[@w:id="{cid}"]',namespaces=NS)[0]
    parent=dele.getparent();idx=parent.index(dele);old=dele[0];dele.remove(old)
    parent.remove(dele);parent.insert(idx,old)
    assert serial(rejected)==serial(original_root), 'Reject-view restoration failed'
    assert old_rev==[serial(x) for x in root.xpath('.//w:ins|.//w:del',namespaces=NS) if x.get(k.qn(k.W_NS,'id')) not in (str(cid),str(cid+1))]
    assert pp==(serial(p.find('w:pPr',NS)) if p.find('w:pPr',NS) is not None else None)
    E.SubElement(rels, '{'+REL+'}Relationship',Id=rid,Type=NS['r']+'/image',Target=media[5:])
    files['word/document.xml']=k.xml_bytes(root)
    files['word/_rels/document.xml.rels']=k.xml_bytes(rels)
    files[media]=asset.read_bytes()
    settings=E.fromstring(files['word/settings.xml']);k.enable_track_revisions(settings)
    files['word/settings.xml']=k.xml_bytes(settings)
    assert b'Extension="png"' in files['[Content_Types].xml']
    _,original=k.read_package(path)
    assert k.endnote_hyperlink_guard(files)==k.endnote_hyperlink_guard(original)
    allowed={'word/document.xml','word/_rels/document.xml.rels','word/settings.xml'}
    assert all(files[name]==data for name,data in original.items() if name not in allowed)
    receipt=dict(figure=n,caption=k.paragraph_text(caption),before=before,asset=str(asset.relative_to(ROOT)),
        asset_sha256=k.sha256_path(asset),old_target=oldtarget,revision_ids=[cid,cid+1],extent=[cx,cy],
        prior_revisions_preserved=True,endnotes_preserved=True,reject_view_restores_original=True)
    with tempfile.TemporaryDirectory(dir=path.parent) as td:
        temp=Path(td)/'validated.docx'
        with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
            for info in infos:z.writestr(info,files[info.filename])
            z.writestr(media,files[media])
        receipt['structure']=k.validate_docx(temp)
        if apply:
            backup=path.parent/'.kila-backups'/f'R1C3-{part}-{before[:12]}.docx'
            backup.parent.mkdir(exist_ok=True)
            assert not backup.exists()
            shutil.copy2(path,backup)
            assert k.sha256_path(backup)==before
            receipt['after']=k.sha256_path(temp);receipt['backup']=str(backup.relative_to(ROOT))
            os.replace(temp,path)
            entry=(f'\n### {part}\n\n- Timestamp: {when}\n- Mode: authorized-tracked-picture-replacement\n'
                f'- Decision: KILA-D-20260930-015\n- Location: image preceding {receipt["caption"]}\n'
                f'- Before: {oldtarget}; preserved within tracked deletion {cid}.\n'
                f'- After: {receipt["asset"]}, SHA-256 {receipt["asset_sha256"]}; tracked insertion {cid+1}.\n'
                f'- Markup SHA-256 before: {before}\n- Markup SHA-256 after: {receipt["after"]}\n'
                f'- Backup: {receipt["backup"]}\n- Extent: {cx} x {cy} EMU, six-inch width, preserved aspect ratio.\n'
                '- Checks: prior revisions, paragraph/run styling, captions, other package parts and endnotes preserved; rejecting this pair restores original XML.\n')
            updated=k.update_log(log.read_text(),'reviewer-1/comment-3',[entry])
            try:log.write_text(updated)
            except Exception:
                shutil.copy2(backup,path);raise
            (ROOT/f'Rev/docs/R1C3-{part}-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
        receipt['status']='applied' if apply else 'dry-run'
        return receipt

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('figure',type=int,choices=range(1,10));ap.add_argument('--apply',action='store_true')
    args=ap.parse_args();print(json.dumps(replace(args.figure,args.apply),indent=2))
