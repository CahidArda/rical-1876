"""Render og.png, the 1200x630 link-preview image.

The background is one pre-drawn timeline from index.html, tilted and faded behind the
title; the foreground uses the app's own wordmark, type and colours. Re-run after a re-bake
if you want the preview to pick up new lines:

    pip install playwright && playwright install chromium
    python3 og.py
"""
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent
W, H = 1200, 630

# which timeline sits in the background, and the event (as titled in the data) to centre on
BG_TIMELINE, BG_EVENT = "france", "The king's trial"

COMPOSE = r"""
([W, H, id, event]) => {
  const eras = [...document.querySelectorAll('#tabs a')].map(a => a.firstChild.textContent.trim());
  const svg = document.querySelector(`#charts svg.baked[data-tl="${id}"][data-v="d"]`).cloneNode(true);

  document.documentElement.setAttribute('data-theme', 'light');
  document.body.innerHTML = '';
  document.body.style.cssText = 'margin:0;overflow:hidden;background:var(--bg)';

  const card = document.createElement('div');
  card.id = 'og';
  card.innerHTML = `
    <style>
      #og { position:relative; width:${W}px; height:${H}px; overflow:hidden; background:var(--bg); color:var(--fg);
            font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }
      #og .bg { position:absolute; inset:0; }
      #og .bg svg { display:block; position:absolute; transform-origin:0 0; opacity:.7; }
      /* keep lines, boxes and labels; drop guides and row shading so it stays light */
      #og .bg svg :is(.rowline, .span, .gapband, .guide, .mline) { display:none; }
      #og .fade { position:absolute; inset:0;
        background: linear-gradient(90deg, var(--bg) 0%, var(--bg) 34%, color-mix(in srgb, var(--bg) 70%, transparent) 52%, transparent 74%); }
      #og .fg { position:absolute; left:72px; top:0; bottom:0; width:720px; display:flex; flex-direction:column; padding:64px 0 60px; }
      #og .brand { align-self:flex-start; font-weight:700; font-size:24px; letter-spacing:-.01em; padding-bottom:6px;
                   border-bottom:3px solid #dc2626; }
      #og h1 { margin:auto 0 0; font-size:72px; line-height:1; letter-spacing:-.04em; font-weight:700; }
      #og p { margin:22px 0 0; font-size:23px; line-height:1.4; color:var(--muted); max-width:580px; }
      #og .eras { margin-top:auto; font-size:16px; line-height:1.7; color:var(--muted); letter-spacing:.01em; }
      #og .eras span { white-space:nowrap; }
      #og .eras i { font-style:normal; opacity:.5; padding:0 7px; }
    </style>
    <div class="bg"></div>
    <div class="fade"></div>
    <div class="fg">
      <div class="brand">Rical</div>
      <h1>Who stood<br>next to whom</h1>
      <p>Five political eras drawn as lines that meet when people's paths cross. Pick an era and follow anyone from rise to fall.</p>
      <div class="eras">${eras.map(e => `<span>${e}</span>`).join('<i>·</i>')}</div>
    </div>`;
  document.body.appendChild(card);

  // one timeline, scaled up and tilted so its lines sweep across the right of the card
  const [, , vw, vh] = svg.getAttribute('viewBox').split(' ').map(Number);
  svg.classList.remove('baked');
  const anchor = [...svg.querySelectorAll('text')].find(t => t.textContent.trim().toLowerCase() === event.toLowerCase());
  if (!anchor) throw new Error(`no event titled "${event}" in ${id}`);
  const ay = +anchor.getAttribute('y');
  // the date column on the chart's left edge would sit behind the title as faint smudges
  svg.querySelectorAll('text').forEach(t => { if (+t.getAttribute('x') < 320) t.remove(); });
  svg.style.width = vw + 'px'; svg.style.height = vh + 'px';
  const scale = 0.85;
  svg.style.transform = `translate(360px, -60px) rotate(-14deg) scale(${scale}) translateY(${-ay + 470}px)`;
  card.querySelector('.bg').appendChild(svg);
}
"""


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1, color_scheme="light")
        await pg.add_init_script("window.BAKING = true")  # keep the pre-drawn markup, skip the live swap
        await pg.goto((ROOT / "index.html").resolve().as_uri())
        await pg.evaluate(COMPOSE, [W, H, BG_TIMELINE, BG_EVENT])
        await pg.wait_for_timeout(200)
        await pg.locator("#og").screenshot(path=str(ROOT / "og.png"))
        await b.close()


asyncio.run(main())
