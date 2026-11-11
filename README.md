# Rical 1876

> Made by Cahid Arda Öz with Claude. The app was prepared with AI, so details may be wrong.
> The historical content was written by the agent; it isn't my claim or opinion.

Interactive storylines of chaotic political eras: who stood with whom, who turned on whom,
and who outlived whom. Three timelines, switchable with the tabs at the top:

| Tab | Span | Cast |
|---|---|---|
| Ottoman Empire (`#ottoman`) | 1865–1964 | Midhat, Abdülhamid, Enver, Talât, Kemal and the rest of the *ricâl-i devlet* |
| Roman Republic (`#rome`) | 133–27 BC | the Gracchi, Marius, Sulla, Pompey, Crassus, Caesar, Cicero, Cato, Brutus, Antony, Octavian |
| French Revolution (`#france`) | 1789–1850 | Lafayette, Danton, Robespierre, Fouché, Talleyrand, Barras, Napoleon, Bernadotte |

Each vertical line is a person and time flows down. When people take part in an event their
lines merge into the event's box, each sitting inside the party they were on. A line ends
where the person dies. Hover over a line, a box or a ✕ for details, or tap it on a phone.

## How it is built

Static files, no build step, no runtime dependencies: `index.html` holds the renderer (plain
JavaScript drawing an SVG), and each timeline is a data file in `timelines/`.

Solving a layout takes a few hundred milliseconds, so the solved layouts (desktop and mobile)
are stored in `timelines/layout-cache.js` and the page only draws, in ~20 ms. After editing a
timeline, regenerate it:

```sh
pip install playwright && playwright install chromium
python3 bake.py
```

If you forget, nothing breaks: the cache entry carries a signature of the data, and on a
mismatch the page solves the layout in the browser as before. `bake.py` also warns if a
timeline gets wider than the shared desktop width (`MIN_W`, 1150px), which keeps tabs from
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

A timeline can also export `SPANS`: periods drawn as a faint band from one event (`from`, by
title) to another (`to`), with a small label on the right edge and a tooltip (`label`,
`date`, `desc`). The French timeline uses them for the seven coalitions.

## Deployment

Deployed on Vercel as a static site straight from `main`.

---

Made by Cahid Arda Öz with Claude · [Blog post](https://cahidarda.com/articles/rical-1876) · [GitHub](https://github.com/CahidArda) · [@cahidarda](https://x.com/cahidarda)

