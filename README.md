# Rical 1876

**Pashas, plots and gallows.** An interactive storyline of the late Ottoman statesmen
(*ricâl-i devlet*), 1865–1964: who stood with whom, who turned on whom, and who outlived whom.

Each vertical line is a person and time flows down. When people take part in an event their
lines merge into the event's box, each sitting inside the party they were on: raiders and
government, sentenced and court, sent away and those who sent them. A line ends where the
person dies. Hover over a line, a box or a ✕ for details, or tap it on a phone.

The cast runs from the Young Ottomans and the 1876 deposition of Abdülaziz, through Midhat
Paşa, the Çerkes Hasan raid, 1908, 31 Mart, the Bab-ı Ali raid, the triumvirate and the
Malta exiles, to the national movement and the opposition parties of the Republic.

## How it is built

One self-contained `index.html`: the data (people, events, parties) and the renderer are
plain JavaScript drawing an SVG. No build step, no dependencies.

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

`P` (people: name, faction, colour, bio, how they died) and `ROWS` (events, deaths and
time gaps, in order) sit at the top of the script in `index.html`. An event lists its
parties and their members; `dies` marks people who die in that event. The layout is
recomputed on load.

## Deployment

Deployed on Vercel as a static site straight from `main`.

---

Made by Cahid Arda Öz with Claude · [Blog post](https://cahidarda.com/articles/rical-1876) · [GitHub](https://github.com/CahidArda) · [@cahidarda](https://x.com/cahidarda)

Prepared with AI. The names, dates and descriptions were written by Claude and may contain mistakes.
