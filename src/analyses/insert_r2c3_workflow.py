"""Bounded new-paragraph/picture exception approved in KILA-D-20260930-020.

Existing document XML is proved unchanged after removing the new paragraphs.
Normal numeric text edits remain owned by the installed Kila helper.
"""
import argparse
import copy
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import zipfile
from lxml import etree as E

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('kila', ROOT/'.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py')
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)
NS = dict(k.NS, wp='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
          a='http://schemas.openxmlformats.org/drawingml/2006/main',
          r='http://schemas.openxmlformats.org/officeDocument/2006/relationships')
REL='http://schemas.openxmlformats.org/package/2006/relationships'
def canon(x): return E.tostring(x, method='c14n')

def insert(mode, apply=False):
    path=ROOT/'Rev/revision/KE01b.rev.markup.docx'
    log=ROOT/'Rev/docs/revisionchanges.md'
    proposal=(ROOT/'Rev/docs/R2C3-method-workflow-proposal.md').read_text()
    part='part-01' if mode=='overview' else 'part-20'
    k.ensure_part_is_new(log.read_text(), 'reviewer-2/comment-3', part)
    infos,files=k.read_package(path); before=k.sha256_path(path)
    original=dict(files);root=E.fromstring(files['word/document.xml']); initial=copy.deepcopy(root)
    body=root.find('w:body',NS)
    pars=root.findall('.//w:p',NS)
    def exact(text):
        matches=[p for p in pars if k.paragraph_text(p)==text]
        assert len(matches)==1, (text,len(matches))
        return matches[0]
    cid=k.next_change_id([E.fromstring(files[n]) for n in k.story_part_names(files)])
    when=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    ids=[]; added=[]
    def ins():
        nonlocal cid
        x=k.make_change_wrapper('ins',cid,'Mike C. Li',when);ids.append(cid);cid+=1
        return x
    def paragraph(template, text=None, drawing_run=None, keep=False):
        p=E.Element(k.qn(k.W_NS,'p'))
        pp=template.find('w:pPr',NS)
        pp=copy.deepcopy(pp) if pp is not None else E.Element(k.qn(k.W_NS,'pPr'))
        for child in list(pp):
            if E.QName(child).localname in ('sectPr','rPr','pageBreakBefore','keepNext'):pp.remove(child)
        if keep: E.SubElement(pp,k.qn(k.W_NS,'keepNext'))
        # Track the new paragraph mark as well as its text/picture run.
        rp=E.SubElement(pp,k.qn(k.W_NS,'rPr'));rp.append(ins());p.append(pp)
        change=ins()
        if drawing_run is not None:change.append(drawing_run)
        else:
            run=E.SubElement(change,k.qn(k.W_NS,'r'))
            style=template.find('.//w:r/w:rPr',NS)
            if style is not None:run.append(copy.deepcopy(style))
            t=E.SubElement(run,k.qn(k.W_NS,'t'));t.text=text
        p.append(change);added.append(p);return p
    new_media=None
    if mode=='overview':
        heading=exact('Materials and Methods')
        assert k.paragraph_text(heading.getnext())=='Study Area and Data Sources'
        template=heading.getnext().getnext()
        text=re.search(r'Proposed paragraph:\n\n"([^"]+)"',proposal).group(1)
        p=paragraph(template,text)
        body.insert(body.index(heading)+1,p)
        after_text=text;location='After Materials and Methods; before Study Area and Data Sources'
    else:
        heading=exact('Figures')
        caption=exact('Figure 2. Population demand and emergency-care network across Kumamoto')
        pic=caption.getprevious();note=caption.getnext()
        sources=pic.xpath('./w:ins/w:r[w:drawing]',namespaces=NS)
        assert len(sources)==1
        run=copy.deepcopy(sources[0])
        for marker in run.findall('w:lastRenderedPageBreak',NS):run.remove(marker)
        rels=E.fromstring(files['word/_rels/document.xml.rels'])
        rid='rIdR2C3Workflow';new_media='word/media/r2c3_methodological_workflow.png'
        assert new_media not in files and not any(x.get('Id')==rid for x in rels)
        run.find('.//a:blip',NS).set(k.qn(NS['r'],'embed'),rid)
        for ext in run.xpath('.//wp:extent|.//a:xfrm/a:ext',namespaces=NS):
            ext.set('cx','5486400');ext.set('cy','3657600')
        docpr=run.find('.//wp:docPr',NS)
        docpr.set('id',str(max(int(x.get('id')) for x in root.findall('.//wp:docPr',NS))+1))
        docpr.set('name','R2C3 methodological workflow')
        docpr.set('descr','Shared baseline network and two complementary analyses: random-failure reliability and single-section consequence.')
        caption_text=re.search(r'^Caption: "([^"]+)"',proposal,re.M).group(1)
        note_text=re.search(r'^Note: "([^"]+)"',proposal,re.M).group(1)
        for offset,p in enumerate([paragraph(pic,drawing_run=run,keep=True),paragraph(caption,caption_text,keep=True),paragraph(note,note_text)]):
            body.insert(body.index(heading)+1+offset,p)
        E.SubElement(rels,'{'+REL+'}Relationship',Id=rid,Type=NS['r']+'/image',Target=new_media[5:])
        files['word/_rels/document.xml.rels']=k.xml_bytes(rels)
        files[new_media]=(ROOT/'data/exp/r2c3_method_workflow/Figure_methodological_workflow.png').read_bytes()
        assert b'Extension="png"' in files['[Content_Types].xml']
        after_text='[Workflow PNG: '+k.sha256_path(ROOT/'data/exp/r2c3_method_workflow/Figure_methodological_workflow.png')+']\n'+caption_text+'\n'+note_text
        location='Figures section, before the previous first figure'
    rejected=copy.deepcopy(root)
    for p in added:
        idx=body.index(p)
        # Remove by unique inserted revision identity, not shifting indices.
        rid=p.find('w:ins',NS).get(k.qn(k.W_NS,'id'))
        target=rejected.xpath(f'.//w:p[w:ins[@w:id="{rid}"]]',namespaces=NS)
        assert len(target)==1;target[0].getparent().remove(target[0])
    assert canon(rejected)==canon(initial),'Existing document XML changed'
    files['word/document.xml']=k.xml_bytes(root)
    assert k.endnote_hyperlink_guard(files)==k.endnote_hyperlink_guard(original)
    assert all(v==files[n] for n,v in original.items() if n not in ('word/document.xml','word/_rels/document.xml.rels'))
    receipt=dict(part=part,before=before,ids=ids,existing_xml_preserved=True,endnotes_preserved=True,after_text=after_text)
    with tempfile.TemporaryDirectory(dir=path.parent) as td:
        tmp=Path(td)/'checked.docx'
        with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
            for info in infos:z.writestr(info,files[info.filename])
            if new_media:z.writestr(new_media,files[new_media])
        receipt['validation']=k.validate_docx(tmp)
        if apply:
            backup=path.parent/'.kila-backups'/f'R2C3-{part}-{before[:12]}.docx'
            assert not backup.exists();shutil.copy2(path,backup)
            receipt['after']=k.sha256_path(tmp);receipt['backup']=str(backup.relative_to(ROOT))
            entry=f'\n### {part}\n\n- Mode: authorized-tracked-insertion\n- Decision: KILA-D-20260930-020\n- Location: {location}\n- Timestamp: {when}\n- Before: no inserted content at this location\n- After:\n\n~~~~text\n{after_text}\n~~~~\n\n- Revision IDs: {ids}\n- Markup SHA-256 before: {before}\n- Markup SHA-256 after: {receipt["after"]}\n- Backup: {receipt["backup"]}\n- Checks: existing XML restored by removal of inserted paragraphs; original media, endnotes and prior revisions preserved; source paragraph/run styles reused.\n'
            updated=k.update_log(log.read_text(),'reviewer-2/comment-3',[entry])
            os.replace(tmp,path)
            try:log.write_text(updated)
            except Exception:shutil.copy2(backup,path);raise
            (ROOT/f'Rev/docs/R2C3-{part}-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    receipt['status']='applied' if apply else 'dry-run';return receipt

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['overview','figure']);ap.add_argument('--apply',action='store_true')
    args=ap.parse_args();print(json.dumps(insert(args.mode,args.apply),indent=2))
