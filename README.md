# The World in One Picture — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Erwinsays12/makefun-news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Erwinsays12/makefun-news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121)

Entry for the [make.fun competition "Sum up 21 November's world news in one image"](https://make.fun/c/news-image-20261121).

## What it is

A one-page newspaper front page that sums up Saturday 21 November 2026's
world news in a single image (`entry.png`, 1024×1024):

- **Lead story — Russian missiles land in Poland.** Two Russian missiles
  and a suspected drone came down in south-east Poland during an overnight
  barrage on Ukraine. PM Donald Tusk calls it a deliberate provocation;
  NATO chief Mark Rutte calls it a grave violation and travels to Warsaw.
- **Kyiv hit in a huge overnight barrage** — 400+ drones and 110 missiles,
  at least 8 killed; France seeks a UN Security Council meeting.
- **Wall Street slumps into correction** — the S&P 500 and Dow enter
  correction as AI shares plunge; the Nasdaq fell 5.28% on Friday.
- **Trump–Xi–Putin summit ends thin** — the first trilateral summit ends
  with few concrete results.
- **World Court: Myanmar committed genocide** — the ICJ rules against
  Myanmar over the Rohingya.
- **Also today:** Riyadh intercepts Houthi missiles, Kryvyi Rih
  casualties, Estonia to shut its Russia border, and UK–EU deals.

All stories are as reported on 21 November 2026, figures as stated by
officials and wire reports. The image is drawn from scratch with Pillow
by `draw_poster.py` — no photographs, no copied artwork.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. Run it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the poster from its source, run `python3 draw_poster.py`
(requires Pillow, build time only).

## License

MIT — see [LICENSE](LICENSE).
