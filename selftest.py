# -*- coding: utf-8 -*-
"""Self-check suite for the cantilever-beam project. Run twice per spec."""
import io, os, csv, re, sys

FOLDER = r'C:\Users\Kanav\Downloads\Biomni Research 1'
fails = []
passes = []

def check(name, cond, detail=''):
    if cond:
        passes.append(name)
    else:
        fails.append(name + (' :: ' + detail if detail else ''))

html = io.open(os.path.join(FOLDER, 'index.html'), encoding='utf-8').read()
css = io.open(os.path.join(FOLDER, 'style.css'), encoding='utf-8').read()
js = io.open(os.path.join(FOLDER, 'script.js'), encoding='utf-8').read()

# 1) no em/en dashes anywhere in HTML/CSS/JS
for name, txt in [('index.html', html), ('style.css', css), ('script.js', js)]:
    check('no em dash in ' + name, '\u2014' not in txt)
    check('no en dash in ' + name, '\u2013' not in txt)
    check('no &8212; entity in ' + name, '&#8212;' not in txt)
    check('no &8211; entity in ' + name, '&#8211;' not in txt)
# 1b) stylesheet and script are externalized
check('style.css linked', '<link rel="stylesheet" href="style.css">' in html)
check('script.js loaded', '<script src="script.js"></script>' in html)
check('no inline style block', '<style>' not in html)
for token in ['const DATA', 'const GEOMETA', 'const TOPO']:
    check('inline %s removed from html' % token.split()[1], token not in html)
    check('%s present in script.js' % token, token in js)
# 3) forbidden words absent on page
for w in ['limitation','caveat','future work','open question','unresolved','weakness','not modeled','did not model']:
    check('no "%s" on page' % w, w not in html.lower())
# 4) the bug value 30.78 gone
check('CH-30 SF 30.78 removed', '30.78' not in html)
check('CH-30 SF 9.33 present', '9.33' in html)
# 5) balanced structural tags
for tag in ['section','style','script','head','body','html','div']:
    o = len(re.findall(r'<%s[\s>]' % tag, html))
    c = html.count('</%s>' % tag)
    check('balanced <%s> (%d=%d)' % (tag, o, c), o == c, 'open %d close %d' % (o, c))
# 6) single title, favicon link
check('has title', '<title>' in html and '</title>' in html)
check('has favicon link', 'rel="icon"' in html and 'favicon.svg' in html)
# 7) images referenced exist on disk
imgs = re.findall(r'<img src="([^"]+)"', html)
for src in imgs:
    path = src.split('?')[0]
    check('img exists: ' + path, os.path.exists(os.path.join(FOLDER, path)), 'missing')
# 8) download links exist
for lnk in ['research_paper_humanized.md','research_paper.md','dataset.csv']:
    check('download exists: ' + lnk, os.path.exists(os.path.join(FOLDER, lnk)))
# 9) favicon exists
check('favicon.svg exists', os.path.exists(os.path.join(FOLDER, 'favicon.svg')))
# 10) no leftover temp helper files
for f in os.listdir(FOLDER):
    if f.startswith('_') and (f.endswith('.py') or f.endswith('.css')):
        check('no temp helper: ' + f, False, 'found ' + f)
# 11) dataset key values
rows = list(csv.DictReader(io.open(os.path.join(FOLDER, 'dataset.csv'), encoding='utf-8')))
check('dataset 494 rows', len(rows) == 494, 'got %d' % len(rows))
def sf(gid, lc):
    for r in rows:
        if r['geometry_id'] == gid and r['load_case'] == lc:
            return float(r['safety_factor'])
    return None
def mean_sf(gid):
    v = [float(r['safety_factor']) for r in rows if r['geometry_id'] == gid]
    return sum(v) / len(v) if v else None
def safe_close(got, target, tol):
    return got is not None and abs(got - target) < tol
check('SIMP-TIP-2 mean SF ~3.46', safe_close(mean_sf('SIMP-TIP-2'), 3.46, 0.01), str(mean_sf('SIMP-TIP-2')))
check('CH-30 mean SF ~1.06', safe_close(mean_sf('CH-30'), 1.06, 0.02), str(mean_sf('CH-30')))
check('SIMP-TIP-2 P100 SF 31.27', safe_close(sf('SIMP-TIP-2','P100'), 31.27, 0.02), str(sf('SIMP-TIP-2','P100')))
check('CH-30 P100 SF 9.33', safe_close(sf('CH-30','P100'), 9.33, 0.01), str(sf('CH-30','P100')))
check('SIMP-TIP-2 P1000 SF 3.13', safe_close(sf('SIMP-TIP-2','P1000'), 3.13, 0.02), str(sf('SIMP-TIP-2','P1000')))
# 12) papers no em/en dash
for md in ['research_paper.md','research_paper_humanized.md','handoff.md']:
    t = io.open(os.path.join(FOLDER, md), encoding='utf-8').read()
    check('no em dash in ' + md, '\u2014' not in t)
    check('no en dash in ' + md, '\u2013' not in t)

print('==== SELF-CHECK PASS: %d   FAIL: %d ====' % (len(passes), len(fails)))
for p in passes:
    print('  [PASS]', p)
for f in fails:
    print('  [FAIL]', f)
sys.exit(1 if fails else 0)