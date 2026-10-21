"""Make course content independent of the site theme: embed the IOT styles in each text field.

Moodle shows page/lesson/label/section text with noclean, so a <style> block at the top of the
field survives a course backup/restore — unlike the theme's Raw SCSS, which is site config and was
scoped to `.course-10` (the course id changes on restore). For every working-copy file that uses
`iot-*` classes, this prepends (or replaces) <style data-iot-style="vN"> holding only the rules
whose classes occur in that file.

Usage: inline-iot-css.py SCSS DIR [DIR ...]   (SCSS = dump of theme_boost/scss)"""
import glob, re, sys

VERSION = "v1"
# Moodle layout classes used by the full-width rule; they are on the page, not in our content.
PAGE_CLASSES = {"limitedwidth", "pagelayout-course", "drawers", "main-inner"}
BLOCK = re.compile(r'<style data-iot-style="[^"]*">.*?</style>\n?', re.S)


def theme_css(path):
    s = open(path, encoding="utf-8").read()
    blocks = re.findall(r"/\* IOT [A-Z ]+ START[^*]*\*/(.*?)/\* IOT [A-Z ]+ END[^*]*\*/", s, re.S)
    css = re.sub(r"/\*.*?\*/", "", "\n".join(blocks), flags=re.S)
    css = css.replace("body.course-10", "body")
    css = re.sub(r"\.course-10\s*\{", ":root {", css)
    return css.replace(".course-10 ", "")


def parse(css):
    """Top-level statements: ('rule', selector, body) or ('media', query, [rules])."""
    out, i = [], 0
    while True:
        j = css.find("{", i)
        if j < 0:
            return out
        head = css[i:j].strip()
        if head.startswith("@media"):
            depth, k = 1, j + 1
            while depth:
                depth += {"{": 1, "}": -1}.get(css[k], 0)
                k += 1
            out.append(("media", head, [r for r in parse(css[j + 1:k - 1]) if r[0] == "rule"]))
            i = k
        else:
            k = css.index("}", j)
            out.append(("rule", head, css[j + 1:k].strip()))
            i = k + 1


def keep_selectors(selector, classes):
    kept = []
    for sel in selector.split(","):
        need = set(re.findall(r"\.([\w-]+)", sel)) - PAGE_CLASSES
        if need <= classes:
            kept.append(" ".join(sel.split()))
    return ",".join(kept)


def css_for(stmts, classes):
    parts = []
    for kind, head, body in stmts:
        if kind == "rule":
            sel = keep_selectors(head, classes)
            if sel:
                parts.append(f"{sel}{{{' '.join(body.split())}}}")
        else:
            inner = [f"{s}{{{' '.join(b.split())}}}" for _, h, b in body if (s := keep_selectors(h, classes))]
            if inner:
                parts.append(f"{' '.join(head.split())}{{{''.join(inner)}}}")
    return "".join(parts)


stmts = parse(theme_css(sys.argv[1]))
total = changed = 0
for d in sys.argv[2:]:
    for path in sorted(glob.glob(f"{d}/s*.html")):
        html = open(path, encoding="utf-8").read()
        body = BLOCK.sub("", html)
        classes = {c for attr in re.findall(r'class="([^"]*)"', body) for c in attr.split()}
        if not any(c.startswith("iot-") for c in classes):
            continue
        css = css_for(stmts, classes)
        new = f'<style data-iot-style="{VERSION}">{css}</style>\n{body}'
        total += 1
        if new != html:
            changed += 1
            open(path, "w", encoding="utf-8").write(new)
        print(f"{len(css):6d} B css  {path.split('/')[-1]}")
print(f"files with iot classes: {total}, changed: {changed}")
