// Technical audit of the reveal.js decks in docs/: every slide and every fragment step is screenshotted and
// measured – text below the footer line, text outside the slide, text covered by a later graphic, text over text,
// fragment steps that change nothing. Usage: node audit_slides.mjs http://127.0.0.1:8932 OUTDIR deck1 deck2 ...
import { chromium } from 'file:///C:/Users/marek.urbaniak/AppData/Local/npm-cache/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const [base, out, ...decks] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: 'C:/Users/marek.urbaniak/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe' });
const report = {};
for (const deck of decks) {
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  const errors = [];
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
  p.on('requestfailed', r => errors.push('REQFAIL ' + r.url()));
  p.on('response', r => { if (r.status() >= 400) errors.push(`HTTP ${r.status()} ${r.url()}`); });
  await p.goto(`${base}/${deck}/`); await p.waitForTimeout(2500);
  fs.mkdirSync(`${out}/${deck}`, { recursive: true });
  const n = await p.evaluate(() => Reveal.getTotalSlides());
  const issues = []; let steps = 0;
  const measure = () => p.evaluate(() => {
    const slide = Reveal.getCurrentSlide();
    const sr = slide.getBoundingClientRect();
    const vis = el => { const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0) return false; for (let a = el; a && a !== slide; a = a.parentElement) { if (a.classList.contains('fragment') && !a.classList.contains('visible')) return false; const st = getComputedStyle(a); if (st.display === 'none' || st.visibility === 'hidden' || parseFloat(st.opacity) === 0) return false; } return true; };
    const texts = []; const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
    let tn; while ((tn = walker.nextNode())) { const t = tn.textContent.trim(); if (!t) continue; const el = tn.parentElement; if (!vis(el)) continue; const range = document.createRange(); range.selectNodeContents(tn); const r = range.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue; texts.push({ t: t.slice(0, 50), x: r.left, y: r.top, r: r.right, b: r.bottom, el }); }
    let footer = null; for (const el of slide.querySelectorAll('*')) { if (el.children.length === 0 && /Pracownia Meteorologii/.test(el.textContent)) { footer = el.getBoundingClientRect(); break; } }
    const footerTop = footer ? footer.top : sr.bottom;
    const graphics = [...slide.querySelectorAll('img, svg, div, section')].filter(g => { if (!vis(g)) return false; const s = getComputedStyle(g); const bg = s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent'; const bi = s.backgroundImage !== 'none'; return g.tagName === 'IMG' || g.tagName === 'SVG' || bg || bi; }).map(g => ({ el: g, r: g.getBoundingClientRect(), img: g.tagName === 'IMG' || g.tagName === 'SVG', z: parseInt(getComputedStyle(g).zIndex) || 0 }));
    const found = [];
    for (const t of texts) {
      if (t.el.textContent.includes('Pracownia Meteorologii')) continue;
      if (t.b > footerTop + 3) found.push({ kind: 'below-footer', text: t.t, px: Math.round(t.b - footerTop) });
      if (t.r > sr.right + 2) found.push({ kind: 'outside-right', text: t.t, px: Math.round(t.r - sr.right) });
      if (t.x < sr.left - 2) found.push({ kind: 'outside-left', text: t.t, px: Math.round(sr.left - t.x) });
      if (t.y < sr.top - 2) found.push({ kind: 'outside-top', text: t.t, px: Math.round(sr.top - t.y) });
      for (const g of graphics) {
        if (g.el === t.el || g.el.contains(t.el) || t.el.contains(g.el)) continue;
        const ix = Math.max(0, Math.min(t.r, g.r.right) - Math.max(t.x, g.r.left)), iy = Math.max(0, Math.min(t.b, g.r.bottom) - Math.max(t.y, g.r.top));
        const area = (t.r - t.x) * (t.b - t.y); if (!area) continue;
        const frac = ix * iy / area; if (frac < 0.25) continue;
        const later = (t.el.compareDocumentPosition(g.el) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
        const tz = parseInt(getComputedStyle(t.el).zIndex) || 0;
        if (g.z > tz || (g.z === tz && later)) found.push({ kind: g.img ? 'covered-by-image' : 'covered-by-box', text: t.t, frac: Math.round(frac * 100) });
      }
      for (const u of texts) { if (u === t || u.el.contains(t.el) || t.el.contains(u.el)) continue; const ix = Math.max(0, Math.min(t.r, u.r) - Math.max(t.x, u.x)), iy = Math.max(0, Math.min(t.b, u.b) - Math.max(t.y, u.y)); const area = (t.r - t.x) * (t.b - t.y); if (area && ix * iy / area > 0.3 && t.t < u.t) found.push({ kind: 'text-over-text', text: t.t, other: u.t }); }
    }
    const sig = texts.map(t => t.t + '@' + Math.round(t.y)).join('|') + '#' + graphics.filter(g => g.img).map(g => g.el.getAttribute('src') + '@' + Math.round(g.r.top)).join('|');
    return { found, sig, fragments: slide.querySelectorAll('.fragment').length, visibleFragments: slide.querySelectorAll('.fragment.visible').length };
  });
  for (let i = 0; i < n; i++) {
    await p.evaluate(i => Reveal.slide(i), i); await p.waitForTimeout(900);
    let step = 0, prev = null;
    while (true) {
      const m = await measure(); steps++;
      await p.screenshot({ path: `${out}/${deck}/s${String(i + 1).padStart(2, '0')}-f${step}.jpg`, type: 'jpeg', quality: 70 });
      for (const f of m.found) issues.push({ slide: i + 1, step, ...f });
      if (step > 0 && prev === m.sig) issues.push({ slide: i + 1, step, kind: 'fragment-no-visible-change' });
      prev = m.sig;
      const more = await p.evaluate(() => { const idx = Reveal.getIndices(); const before = idx.f; Reveal.next(); const after = Reveal.getIndices(); return after.h === idx.h && after.v === idx.v && after.f !== before; });
      if (!more) break; step++; await p.waitForTimeout(700);
      if (step > 25) { issues.push({ slide: i + 1, kind: 'too-many-fragments' }); break; }
    }
  }
  report[deck] = { slides: n, steps, issues, errors: [...new Set(errors)] };
  console.log(`${deck}: ${n} slides, ${steps} steps, ${issues.length} issues, ${report[deck].errors.length} errors`);
  await p.close();
}
fs.writeFileSync(`${out}/report.json`, JSON.stringify(report, null, 1));
await b.close();
