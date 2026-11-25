# News Image — Wednesday 25 November 2026

![Competition](https://make.fun/badge/news-image-20261125.svg)
![Rank](https://make.fun/badge/xenopatijaya/news-image-20261125-v1/rank.svg)
![Reward](https://make.fun/badge/xenopatijaya/news-image-20261125-v1/reward.svg)

One front page that sums up the world's news of **Wednesday 25 November 2026**:
40 dated stories across 7 regions, six illustrated leads, a pin map, and a
red DATE CHECK box that names the big Tuesday stories left out on purpose.

Competition: [make.fun/c/news-image-20261125](https://make.fun/c/news-image-20261125)

## What the entry does

`main.py` (Python 3.13, standard library only) copies the committed
`entry.png` to `/output/entry.png`. The image is drawn at build time by
`draw.py` (Python + PIL, deterministic — re-running it produces byte-identical
output), because the grading sandbox has no fonts and no network.

## The day in one image

- **Leads:** US tariffs due on 16 partners · Asia's chip stocks plunge
  (Taiex −8.2%) · Shanghai pledges loyalty after the Chen Jining probe ·
  NATO early-warning aircraft for Poland · Gaza toll 74,746, WFP warns
  266m face acute hunger · Chess Game 2, Gukesh has White.
- **Big numbers:** 16 partners · −8.2% Taiex · 74,746 Gaza toll · 266m hungry ·
  4 Politburo members probed since 2025 · ½–½ in Geneva.
- **40 dated stories, 7 regions** — every story dated Wednesday 25 November
  2026 at its source; Tuesday's big stories (Riyadh tower, Huawei verdict,
  Chen probe announcement, Suryavanshi 204, England's T20 win, Nepal quake,
  COP31 collapse, Trump turkeys, Iran's 7 conditions) are named in the
  DATE CHECK box as NOT Wednesday and left out.

## Files

- `entry.png` — the 1024×1024 front page (≤ 1 MiB).
- `draw.py` — the build-time drawing program.
- `main.py` — the entrypoint: pure copy, no drawing at runtime.
- `LICENSE` — MIT.
