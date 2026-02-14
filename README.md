[English](./README.md) | [中文](./README-zh.md)

# Kards Card Crawler

A Python-based automation tool designed to crawl card images from the official [Kards](https://www.kards.com/) website, covering all cards from the WWII-themed CCG.

## 🌟 Key Features

- **Automated Crawling**: Fetches comprehensive card information for all nations (Soviet, USA, Japan, Germany, etc.) via the official GraphQL API.
- **Multi-dimensional Organization**: Automatically categorizes and saves images into folders based on **Nation** and **Kredit Cost**.
- **Format Conversion**: Automatically converts high-compression `AVIF` images from the official server into the widely compatible `PNG` format.
- **Smart Renaming**: Prioritizes the Chinese card title for filenames; falls back to the original image ID if a name is unavailable.
- **Anti-Ban Mechanism**: Includes a built-in request delay (1s) and `Session` reuse to ensure stable and respectful crawling.

## 📂 Directory Structure Example

After running, images are organized as follows:

Plaintext

```
imgs/
├── Soviet/
│   ├── 0k/
│   │   └── 13th_Rifle_Regiment.png
│   └── 1k/
│       └── Strafe.png
├── USA/
└── ...
```

## 🛠️ Dependencies

Ensure you have `requests` and `Pillow` (for image processing) installed in your environment:

Bash

```
pip install requests Pillow
```

## 🚀 Usage

1. **Prepare Files**: Ensure you have the following two Python files in your project directory:

   - `main.py` (Contains the main crawler loop)
   - `get_img.py` (Contains image downloading and conversion functions)

2. **Run the Program**:

   Bash

   ```
   python main.py
   ```

3. **View Results**: Once finished, all card images will be available in the `imgs/` folder.

## ⚙️ Core Logic

- **GraphQL API**: The program sends POST requests to `https://api.kards.com/graphql` to fetch paginated card data.
- **Data Filtering**: The script is currently configured to include:
  - `showSpawnables`: Token/Spawned cards.
  - `showExiles`: Exile cards.
  - `showReserved`: Reserved pool cards (rotated out of standard).
- **Exception Handling**: The script automatically skips existing images and sanitizes filenames by removing illegal characters (e.g., `<>:"/\|?*`).

## ⚙️ Configuration

You can customize the following parameters in the script:

- **Nations**: `nationIds = [1, 2, 3, 4, 5, 6, 7, 8, 9]`
- **Kredit Costs**: `kosts = [0, 1, 2, 3, 4, 5, 6, 7]`
- **Language**: `"language": "zh"` (Change to `"en"` for English data)

## ⚠️ Disclaimer

- This tool is for personal study and research purposes only. Do not use it for large-scale commercial purposes.
- Please respect the copyright of the game developers and control the crawling frequency reasonably.

