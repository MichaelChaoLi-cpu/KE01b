"""Bounded R2C1 exception; retain Kila's transaction, backups and tracked diff.

Discard only stale automatic pagination caches in the two approved target runs.
These are not explicit page breaks. Word recomputes pagination on rendering.
Never relax field, hyperlink, style, or existing-revision checks.
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
loader = importlib.util.spec_from_file_location('kila_edit', ROOT / '.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py')
k = importlib.util.module_from_spec(loader)
loader.loader.exec_module(k)
original_patch = k.patch_normal
MARKER = k.qn(k.W_NS, 'lastRenderedPageBreak')


def fingerprint(root, query):
    return [k.etree.tostring(n, method='c14n') for n in root.xpath(query, namespaces=k.NS)]


def bounded_patch(root, spec, *args):
    assert spec['comment_id'] == 'reviewer-2/comment-1'
    assert spec['part_id'] in ['part-01', 'part-02', 'part-03']
    approved = json.loads((ROOT / 'Rev/docs/r2c1-edit-specs' / (spec['part_id'] + '.json')).read_text())
    assert spec == approved
    before = copy.deepcopy(root)
    protected = './/w:ins|.//w:del|.//w:instrText|.//w:fldChar|.//w:hyperlink|.//w:bookmarkStart|.//w:bookmarkEnd|.//w:pPr|.//m:oMath'
    old_protected = fingerprint(root, protected)
    paragraphs = k.all_paragraphs(root)
    matches = [p for p in paragraphs if spec['before'] in k.paragraph_text(p)]
    assert len(matches) == 1
    p = matches[0]
    text = k.paragraph_text(p)
    start = text.index(spec['before'])
    stop = start + len(spec['before'])
    # Explicit supplemental authorization KILA-D-20261001-001.
    # Remove only four empty proofing annotations inside this exact target.
    if spec['part_id'] == 'part-01':
        proofing = p.findall('w:proofErr', namespaces=k.NS)
        assert len(proofing) == 4
        for marker in proofing:
            offset = sum(len(k.paragraph_text(c)) for c in list(p)[:p.index(marker)])
            assert start <= offset <= stop and len(marker) == 0
            assert marker.get(k.qn(k.W_NS, 'type')) in {'gramStart', 'gramEnd', 'spellStart', 'spellEnd'}
        for marker in proofing:
            p.remove(marker)
    removed = 0
    for seg in k.text_segments(p):
        if seg['end'] <= start or seg['start'] >= stop:
            continue
        run = seg['node'].getparent()
        markers = run.findall('w:lastRenderedPageBreak', namespaces=k.NS)
        if not markers:
            continue
        assert run.getparent() is p and len(markers) == 1
        assert len(run.findall('w:t', namespaces=k.NS)) == 1
        assert all(c.tag in {MARKER, k.qn(k.W_NS, 't'), k.qn(k.W_NS, 'rPr')} for c in run)
        assert not k.has_ancestor(run, {'ins', 'del', 'moveFrom', 'moveTo'})
        run.remove(markers[0])
        removed += 1
    assert removed == (0 if spec['part_id'] == 'part-02' else 1)
    expected = [k.paragraph_text(x) for x in paragraphs]
    expected[paragraphs.index(p)] = text.replace(spec['before'], spec['after'], 1)
    result = original_patch(root, spec, *args)
    assert [k.paragraph_text(x) for x in k.all_paragraphs(root)] == expected
    # Existing protected objects remain byte-identical and in the same order.
    new_protected = fingerprint(root, protected)
    it = iter(new_protected)
    assert all(any(value == candidate for candidate in it) for value in old_protected)
    old_paras = k.all_paragraphs(before)
    for i, para in enumerate(k.all_paragraphs(root)):
        if i != paragraphs.index(p):
            assert k.etree.tostring(para) == k.etree.tostring(old_paras[i])
    print(f'Pagination cache removed: {removed}; exact text and protected-object checks passed')
    return result


k.patch_normal = bounded_patch
ap = argparse.ArgumentParser()
ap.add_argument('part', choices=['01', '02', '03'])
ap.add_argument('--apply', action='store_true')
args = ap.parse_args()
receipt = k.apply_revision(ROOT / 'Rev/revision/KE01b.rev.markup.docx', ROOT / 'Rev/docs/revisionchanges.md', ROOT / f'Rev/docs/r2c1-edit-specs/part-{args.part}.json', 'Kila', not args.apply)
print(json.dumps(receipt, indent=2))
