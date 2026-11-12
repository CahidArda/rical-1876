# Rical 1876

**Live:** [rical-1876.cahidarda.com](https://rical-1876.cahidarda.com) · **Write-up:** [cahidarda.com/articles/rical-1876](https://cahidarda.com/articles/rical-1876)

> Made by Cahid Arda Öz with Claude. The app was prepared with AI, so details may be wrong.
> The historical content was written by the agent; it isn't my claim or opinion.

Interactive storylines of chaotic political eras: who stood with whom, who turned on whom,
and who outlived whom. Three timelines, switchable with the tabs at the top:

| Tab | Span | Cast |
|---|---|---|
| Roman Republic (`#rome`) | 133–27 BC | the Gracchi, Marius, Sulla, Pompey, Crassus, Caesar, Cicero, Cato, Brutus, Antony, Octavian |
| United States (`#america`) | 1765–1865 | Washington, Franklin, Adams, Jefferson, Hamilton, Burr, Jackson, Clay, Calhoun, Lincoln, Douglass, Lee, Grant |
| French Revolution (`#france`) | 1789–1850 | Lafayette, Danton, Robespierre, Fouché, Talleyrand, Barras, Napoleon, Bernadotte |
| Ottoman Empire (`#ottoman`) | 1865–1964 | Midhat, Abdülhamid, Enver, Talât, Kemal and the rest of the *ricâl-i devlet* |
| Bolsheviks (`#bolsheviks`) | 1903–1953 | Lenin, Martov, Trotsky, Zinoviev, Kamenev, Bukharin, Stalin, Molotov, Beria |

Each vertical line is a person and time flows down. When people take part in an event their
lines merge into the event's box, each sitting inside the party they were on. A line ends
where the person dies. Hover over a line, a box or a ✕ for details, or tap it on a phone.

## How it is built

Static files, no build step, no runtime dependencies: `index.html` holds the renderer (plain
JavaScript drawing an SVG), and each timeline is a data file in `timelines/`.

The page is pre-drawn. `bake.py` solves every layout (a few hundred milliseconds each), stores
the results in `timelines/layout-cache.js`, then renders every timeline for desktop and mobile
and writes the finished SVG, legends, tabs and titles into `index.html` between the
`<!--BAKE:…-->` markers. The browser paints the chart straight from the HTML; the script then
swaps in identical, interactive copies (~20 ms each). After editing a timeline or the
renderer, re-bake:

```sh
pip install playwright && playwright install chromium
python3 bake.py
```

A GitHub Action (`.github/workflows/bake.yml`) does this on every push to `main` that touches
the timelines, `index.html` or `bake.py`, and commits the result if anything changed. If you
forget and the Action hasn't run yet, nothing breaks: the cache entry carries a signature of the data, and on a
mismatch the page solves the layout in the browser; the live copy replaces the stale
pre-drawn one as soon as the script runs. `bake.py` also warns if a
timeline gets wider than the shared desktop width (`MIN_W`, 1170px), which keeps tabs from
shifting when you switch.

The layout is a storyline visualization, in the spirit of Tanahashi & Ma (2012) and
StoryFlow (Liu et al., 2013):

1. **Ordering.** Every event is a layer. Lines, event groups and parties inside an event
   are re-sorted by barycenter sweeps (down using the layer above, up using the layer
   below), keeping the order with the fewest crossings.
2. **Straightening.** With the order fixed, x positions minimize how far each line moves
   between layers, subject to minimum gaps and box widths. Each layer is a weighted
   isotonic regression solved with pool-adjacent-violators, iterated to convergence.
   A final top-down pass keeps lines that are not part of an event perfectly straight, so
   they only move when a box needs the room.

## Link preview

`og.png` is the 1200×630 image link previews show (the `og:` and `twitter:` tags in
`index.html`). `og.py` draws it from the baked French Revolution chart, tilted behind the
title and centred on the king's trial. It is not part of the bake or the GitHub Action, so
the preview stays put as the timelines change. To redraw it, run it by hand after a bake:

```sh
python3 og.py
```

The timeline and the event it centres on are set at the top of `og.py`.

## Run locally

```sh
npx serve .
```

or just open `index.html` in a browser.

## Editing the data

Each file in `timelines/` defines `GROUPS` (factions and colours), `P` (people: name,
faction, colour, bio, how they died) and `ROWS` (events, deaths and time gaps, in order),
and registers itself on `window.TIMELINES`. To add a timeline, add a file, a `<script>` tag
and its id in `TL_ORDER` in `index.html`.

Each person and event can also carry `wiki` (an English Wikipedia article title, shown as a
link in the tooltip), and optionally `img` (an image URL, e.g. from Wikimedia Commons) with
`imgPage` (its source page) and `imgR` (width / height). The image sits left of the text at a
fixed height; `imgR` lets the tooltip reserve its exact space with a spinner before the image
arrives. Ratios for the Commons files live in `timelines/img-ratios.js`. Images are never hosted here.

The images that are filled in come from each article's Wikidata image (P18) and are served by
Wikimedia Commons. Only paintings, engravings, coins, sculpture and documents are used;
photographs of people are deliberately left out, which is why most of the Ottoman cast has none. An event lists its
parties and their members; `dies` marks people who die in that event.

A row with `t:"m"` is a milestone: an event none of the people took part in (Trafalgar, say).
It has a date, title, description and optional `wiki`/image, draws as a faint dashed rule, and
the lines pass straight through it.

A timeline can also export `SPANS`: periods drawn as a faint band from one event (`from`, by
title) to another (`to`), with a bracket and labels at its start and end on the right edge, and a tooltip (`label`, `result`,
`date`, `desc`). Overlapping periods nest like brackets: the one that starts first hugs the right edge, later ones sit one lane in. Every timeline uses them: wars and constitutional eras for the Ottomans, civil wars for Rome, regimes and the seven coalitions for France, the war and the presidencies for America, and the war, NEP and trial years for the Bolsheviks.

## Deployment

Deployed on Vercel as a static site straight from `main`.

---

Made by Cahid Arda Öz with Claude · [Blog post](https://cahidarda.com/articles/rical-1876) · [GitHub](https://github.com/CahidArda) · [@cahidarda](https://x.com/cahidarda)

