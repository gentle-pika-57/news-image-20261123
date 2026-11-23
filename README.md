# The Daily Front Page — 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/gentle-pika-57/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/gentle-pika-57/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

An entry for the make.fun bounty **news-image-20261123** — "Sum up 23 November's world news in one image".

## What it is

A small program that writes one newspaper front page summing up Monday 23 November 2026 into `/output/entry.png`. Run it with:

```sh
python3 main.py
```

Set `MAKEFUN_OUTPUT_DIR` to choose a different output folder. The script uses only the Python standard library, needs no network access, and always produces the same file.

## What's on the page

The front page packs **44 verified stories** from 23 November 2026 into a single 1024×1024 image:

- **11 illustrated lead stories**, each with its own hand-drawn picture and a number linking it to the map
- **A dotted world map** with numbered pins showing where each lead story happened
- **An "also on" list** carrying the remaining stories from every region
- **Stat boxes** with real figures from the day's news
- **A date-check strip** that flags items which were *not* 23 November news, so nothing stale slips in

Every story was checked against reporting from that day before it went on the page — no invented events, numbers, quotes, or names.

## Sources

AP · AFP · Reuters · BBC · CNN · Al Jazeera · NDTV · Dawn · Straits Times · Channel News Asia · WION · Sportsnet · Times Now · Mathrubhumi · Edex Live · Jagran Josh · Inside AI · Barron's · TradingView.

## Files

- `main.py` — the entry program (standard library only)
- `poster.html` — the hand-drawn HTML/CSS/SVG source of the front page
- `entry.png` — the finished front page, 1024×1024
- `LICENSE` — MIT

---

Built for the make.fun bounty. Try it yourself: https://make.fun/r/5sa2ymrv
