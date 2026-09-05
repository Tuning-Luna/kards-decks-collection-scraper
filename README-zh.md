[English](./README.md) | [中文](./README-zh.md)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=fff)
![curl_cffi](https://img.shields.io/badge/curl_cffi-0.15-009688?style=flat-square&logo=libcurl&logoColor=fff&labelColor=555)
![Pillow](https://img.shields.io/badge/Pillow-12-FF3333?style=flat-square&logo=python&logoColor=fff&labelColor=555)
![License](https://img.shields.io/badge/License-MIT-yellowgreen?style=flat-square)

# Kards 卡牌爬虫

自动下载 [Kards](https://www.kards.com/)（二战卡牌游戏）全部卡牌图片的 Python 工具。
基于 GraphQL API + `curl_cffi` 浏览器指纹 + Pillow 格式转换，遍历 11 个阵营与全部费用，自动分页、去重，并支持**断点续传**。

## 快速开始

```bash
git clone https://github.com/Tuning-Luna/kards-decks-collection-scraper.git
cd kards-decks-collection-scraper
pip install -r requirements.txt
python main.py          # 全量爬取；加 --debug 查看详细日志
```

> 进度记录在 `progress.json`，中断后重新运行会自动跳过已完成的组合。

## 配置

编辑 `src/config.py`：

| 配置 | 说明 | 默认值 |
| --- | --- | --- |
| `PROXIES` | HTTP/HTTPS 代理 | `http://127.0.0.1:7897` |
| `NATION_IDS` | 阵营 ID 列表（0 = 中立） | `[1..10, 0]` |
| `KOSTS` | 卡牌费用范围 | `[0..7]` |
| `IMAGE_BASE_URL` | 修改路径里的语言段即可切换语言 | `.../zh-Hans/` |

> ⚠️ **国内用户必看**：Kards 的 API 与 CDN 需通过代理才能访问。
> 默认端口 `7897` 是作者本机 Clash 的口，**换成本机你自己的**（Clash `7890`、v2rayN `10809`、SSR `1080` 等）。
> 本机无代理时设为 `{"http": "", "https": ""}` 走直连（仅当你的网络能直接访问 `kards.com` 时可用）。

## 免责声明

仅供个人学习研究。请合理控制爬取频率，尊重游戏版权。
