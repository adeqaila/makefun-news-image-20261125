# THE WORLD IN ONE DAY

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/adeqaila/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/adeqaila/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

A classic broadsheet front page summing up Wednesday 25 November 2026 in one image: 30 verified news stories across 7 regions, led by Australia's 4.9% CPI release, Kyiv sinking a Russian warship off Libya, and the Houthi strike on Riyadh's tallest tower — with a 12-pin world map, a UTC timeline, and a stat strip.

## How it works

- `main.py` — entrypoint: copies `entry.png` to `/output/entry.png` (no network, deterministic; two runs write identical bytes).
- `draw_entry.py` — renders `entry.png` from the 30 verified stories (re-running it reproduces the image byte-for-byte).
- `entry.png` — the front page (1024×1024, 157,082 bytes).

License: MIT (see LICENSE).
