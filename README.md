[English](./README.md) | [中文](./README-zh.md)

# Kards Card Crawler

A Python-based automation tool designed to crawl card images from the official [Kards](https://www.kards.com/) website, covering all cards from the WWII-themed CCG.

## 🌟 Key Features

- **Automated Crawling**: Fetches comprehensive card information for all nations (Soviet, USA, Japan, Germany, etc.) via the official GraphQL API.
- **Multi-dimensional Organization**: Automatically categorizes and saves images into folders based on **Nation** and **Kredit Cost**.
- **Format Conversion**: Automatically converts high-compression `AVIF` images from the official server into the widely compatible `PNG` format.
- **Smart Renaming**: Prioritizes the Chinese card title for filenames; falls back to the original image ID if a name is unavailable.
- **Anti-Ban Mechanism**: Includes built-in request delay and `curl_cffi` browser fingerprint impersonation for stable crawling.

## 📂 Directory Structure

```
imgs/
├── 苏联/
│   ├── 0k/
│   │   └── 步兵第13步兵团.png
│   └── 1k/
│       └── 扫射.png
├── 美国/
├── 中立/
│   ├── production_生产.png
│   ├── routed_troops_溃军.png
│   └── plan_计划.png
└── ...
```

## 🛠️ Dependencies

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Key packages: `requests` (GraphQL API), `curl_cffi` (image download with fingerprint impersonation), `Pillow` (image format conversion).

## 🚀 Usage

Simply run:

```bash
python main.py
```

This will:
1. Crawl all regular cards across all nations and kredit costs
2. Automatically download 3 neutral cards (Production, Routed Troops, Plan)

All images will be saved in the `imgs/` folder.

## 📁 Project Structure

```
main.py                 # Entry point
src/
    config.py           # Configuration (API URL, headers, nations, query)
    image.py            # Image download module (curl_cffi + Pillow)
    scraper.py          # Crawler main logic (pagination, dedup, orchestration)
```

## ⚙️ Core Logic

- **GraphQL API**: Sends POST requests to `https://herokuapi.kards.com/graphql` to fetch paginated card data.
- **Data Filtering**: Includes `showSpawnables` (token cards), `showExiles` (exile cards), `showReserved` (reserved pool cards).
- **Deduplication**: Skips previously downloaded cards by tracking `cardId` across sessions.
- **Exception Handling**: Automatically skips existing images and sanitizes filenames.

## ⚙️ Configuration

Edit `src/config.py` to customize:

- **Nations**: `NATION_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9]`
- **Kredit Costs**: `KOSTS = [0, 1, 2, 3, 4, 5, 6, 7]`
- **Language**: Change the language segment in `IMAGE_BASE_URL` (e.g., `zh-Hans` → `en-EN`)
- **Proxy**: Update `PROXIES` if needed

## ⚠️ Disclaimer

- This tool is for personal study and research purposes only. Do not use it for large-scale commercial purposes.
- Please respect the copyright of the game developers and control the crawling frequency reasonably.
