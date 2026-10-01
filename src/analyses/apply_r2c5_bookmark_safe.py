"""Authorized R2C5 internal split; preserve installed transaction and guards."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
loader = importlib.util.spec_from_file_location('kila', ROOT / '.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py')
k = importlib.util.module_from_spec(loader)
loader.loader.exec_module(k)
original = k.patch_normal
spec_path = ROOT / 'Rev/docs/r2c5-edit-specs/part-01.json'


def fingerprint(root, query):
    return [k.etree.tostring(x, method='c14n') for x in root.xpath(query, namespaces=k.NS)]


def bounded_patch(root, spec, change_id, author, when):
    assert spec == json.loads(spec_path.read_text())
    assert spec['comment_id'] == 'reviewer-2/comment-5' and spec['part_id'] == 'part-01'
    assert 'KILA-D-20261001-006' in spec['decision_ids']
    old = copy.deepcopy(root)
    p, index, offset, _ = k.locate_unique_part(root, spec['before'], spec['paragraph_anchor'])
    assert offset == 0 and k.paragraph_text(p) == spec['before']
    bookmarks = './/w:bookmarkStart|.//w:bookmarkEnd'
    protected = './/w:ins|.//w:del|.//w:instrText|.//w:fldChar|.//w:hyperlink|.//m:oMath|.//w:pPr'
    before_bookmarks = fingerprint(root, bookmarks)
    before_protected = fingerprint(root, protected)
    oldleft, oldright = spec['before'].split(' A second contribution', 1)
    oldright = 'A second contribution' + oldright
    newleft, newright = spec['after'].split(' Second, a separate', 1)
    newright = 'Second, a separate' + newright
    anchors = p.xpath('./w:bookmarkStart|./w:bookmarkEnd', namespaces=k.NS)
    assert [x.get(k.qn(k.W_NS, 'id')) for x in anchors] == ['65', '66', '65', '66']
    assert k.paragraph_text(p[1]) == oldleft
    markers = p.findall('.//w:lastRenderedPageBreak', namespaces=k.NS)
    assert len(markers) == 1
    run = markers[0].getparent()
    assert run.getparent() is p
    assert all(x.tag in {k.qn(k.W_NS, t) for t in ['t', 'rPr', 'lastRenderedPageBreak']} for x in run)
    assert not k.has_ancestor(run, {'ins', 'del', 'moveFrom', 'moveTo'})
    run.remove(markers[0])
    fragments, revision_ids, styles = [], [], []
    for b, a, shift in [(oldright, newright, len(oldleft) + 1), (oldleft, newleft, 0)]:
        piece = {**spec, 'before': b, 'after': a, 'paragraph_anchor': b}
        change_id, fs, ids, style, _ = original(root, piece, change_id, author, when)
        fragments.extend({**f, 'start': f['start'] + shift, 'end': f['end'] + shift} for f in fs)
        revision_ids.extend(ids)
        styles.append(style)
    assert k.paragraph_text(p) == spec['after']
    assert fingerprint(root, bookmarks) == before_bookmarks
    it = iter(fingerprint(root, protected))
    assert all(any(v == item for item in it) for v in before_protected)
    for i, (a, b) in enumerate(zip(k.all_paragraphs(old), k.all_paragraphs(root))):
        if i != index:
            assert k.etree.tostring(a) == k.etree.tostring(b)
    assert len(set(styles)) == 1
    print('Exact text, original bookmarks, existing revisions and unrelated paragraphs preserved.')
    return change_id, sorted(fragments, key=lambda f: f['start']), revision_ids, styles[0], [{'paragraph_index': index, 'character_offset': offset}]


k.patch_normal = bounded_patch
ap = argparse.ArgumentParser()
ap.add_argument('--apply', action='store_true')
args = ap.parse_args()
result = k.apply_revision(ROOT / 'Rev/revision/KE01b.rev.markup.docx', ROOT / 'Rev/docs/revisionchanges.md', spec_path, 'Kila', not args.apply)
print(json.dumps(result, indent=2))
