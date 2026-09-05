[English](./README.md) | [中文](./README-zh.md)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=fff)
![curl_cffi](https://img.shields.io/badge/curl_cffi-0.15-009688?style=flat-square&logo=libcurl&logoColor=fff&labelColor=555)
![Pillow](https://img.shields.io/badge/Pillow-12-FF3333?style=flat-square&logo=python&logoColor=fff&labelColor=555)
![License](https://img.shields.io/badge/License-MIT-yellowgreen?style=flat-square)

# Kards Card Crawler

Automatically download every card image from [Kards](https://www.kards.com/), the WWII CCG.
Runs on the GraphQL API + `curl_cffi` browser-fingerprint downloads + Pillow conversion across all 11 factions
and every kredit cost, with automatic pagination, deduplication, and **resumable progress**.

## Quick start

```bash
git clone https://github.com/Tuning-Luna/kards-decks-collection-scraper.git
cd kards-decks-collection-scraper
pip install -r requirements.txt
python main.py          # full crawl; add --debug for verbose logs
```

> Progress is stored in `progress.json`; a re-run skips completed nation×cost combos automatically.

## Configuration

Edit `src/config.py`:

| Key | Description | Default |
| --- | --- | --- |
| `PROXIES` | HTTP/HTTPS proxy | `http://127.0.0.1:7897` |
| `NATION_IDS` | Faction IDs (0 = Neutral) | `[1..10, 0]` |
| `KOSTS` | Kredit costs to crawl | `[0..7]` |
| `IMAGE_BASE_URL` | Change the language segment to switch locale | `.../zh-Hans/` |

> ⚠️ **For users in mainland China**: reaching the Kards API/CDN requires a proxy.
> The default `7897` port is the author's local Clash port — **change it to your own** (Clash `7890`,
> v2rayN `10809`, SSR `1080`, etc.). With no proxy client, use `{"http": "", "https": ""}` to go direct —
> only if your network can reach `kards.com`.

## Disclaimer

For personal study only. Crawl at a reasonable rate and respect the game's copyright.
