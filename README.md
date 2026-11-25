# THE WORLD IN ONE DAY

[![make.fun](https://img.shields.io/badge/make.fun-LIVE-brightgreen)](https://make.fun/bounty/news-image-20261124)
[![bounty](https://img.shields.io/badge/bounty-news--image--20261124-blue)](https://make.fun/bounty/news-image-20261124)
[![prize](https://img.shields.io/badge/prize-%24100%20top%2050-gold)](https://make.fun/bounty/news-image-20261124)

**"Sum up 24 November's world news in one image"** — a one-page newspaper
front page drawn entirely in code: **35 stories from 7 regions, every one
first reported on Tuesday 24 November 2026**.

Three illustrated leads (Houthi strike on Riyadh's finance district, the
ADNOC tanker mined in the Strait of Hormuz, China's probe of Politburo
member Chen Jining), ten more featured stories with their own vector
illustrations, a pinned world map, a "day in numbers" stat strip, and a
DATE CHECK box naming the six big stories deliberately left out because
they broke on 21–23 Nov, not the 24th.

## Run

```bash
python3 main.py   # writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png)
```

Python 3 + Pillow 10.2.0, DejaVu fonts. No network, no external assets —
`main.py` draws the whole page programmatically (1600 × 2100).

See [design.md](design.md) for the full 35-story list, sources, region
counts and the DATE CHECK rationale.
