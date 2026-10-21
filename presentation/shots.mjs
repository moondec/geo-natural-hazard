import { chromium } from 'file:///C:/Users/marek.urbaniak/AppData/Local/npm-cache/_npx/9833c18b2d85bc59/node_modules/playwright/index.mjs';
const url = process.argv[2], out = process.argv[3];
const b = await chromium.launch({ executablePath: 'C:/Users/marek.urbaniak/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe' }); const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
await p.goto(url); await p.waitForTimeout(2500);
const n = await p.evaluate(() => Reveal.getTotalSlides());
for (let i = 0; i < n; i++) { await p.evaluate(i => { Reveal.slide(i); document.querySelectorAll('.fragment').forEach(f => f.classList.add('visible','current-fragment')); }, i); await p.waitForTimeout(1200); await p.screenshot({ path: `${out}/slide${String(i+1).padStart(2,'0')}.jpg`, type: 'jpeg', quality: 85 }); }
console.log('done', n); await b.close();
