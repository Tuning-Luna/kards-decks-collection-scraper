[English](./README.md) | [中文](./README-zh.md)

# Kards Card Crawler

Automatically download all card images from [Kards](https://www.kards.com/), the WWII CCG.

## How it works

1. **GraphQL API** — queries `https://herokuapi.kards.com/graphql` for card metadata (name, faction, kredit cost, image path)
2. **Image download** — fetches AVIF images from the CDN via `curl_cffi` (browser fingerprint impersonation)
3. **Format conversion** — converts AVIF to PNG using Pillow

The crawler iterates over all factions (11 nations including Neutral) and kredit costs (0–7), with pagination and deduplication.

## Folder structure

```
imgs/
├── 苏联/
│   ├── 0k/
│   │   └── 步兵第13步兵团_13th_rifles.png
│   └── ...
├── 美国/
│   └── ...
├── 中立/
│   ├── 0k/
│   ├── 1k/
│   └── ...
└── ...
```

Each file is named `{卡牌中文名}_{cardId}.png`. Falls back to `unknown_{cardId}.png` if no Chinese name is available.

## Usage

```bash
git clone https://github.com/Tuning-Luna/kards-decks-collection-scraper.git
cd kards-decks-collection-scraper
pip install -r requirements.txt
python main.py
```

## Configuration

Edit `src/config.py`:

| Key              | Description                                 | Default                    |
| ---------------- | ------------------------------------------- | -------------------------- |
| `NATION_IDS`     | Faction IDs (0 = Neutral)                   | `[1..10, 0]`               |
| `KOSTS`          | Kredit costs to crawl                       | `[0, 1, 2, 3, 4, 5, 6, 7]` |
| `IMAGE_BASE_URL` | Change language (e.g. `zh-Hans` -> `en-EN`) | `.../zh-Hans/`             |
| `PROXIES`        | HTTP/HTTPS proxy                            | `http://127.0.0.1:7897`    |

## Project structure

```
main.py                 # Entry point
src/
    config.py           # API config, headers, query, nation/kredit params
    scraper.py          # Crawl orchestration (pagination, dedup)
    image.py            # AVIF → PNG download (curl_cffi + Pillow)
```

## Disclaimer

For personal study only. Please control crawl frequency and respect the game developer's copyright.
