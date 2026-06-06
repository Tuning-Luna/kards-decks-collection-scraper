[English](./README.md) | [中文](./README-zh.md)

# Kards Card Crawler (Kards 卡牌爬取工具)

这是一个基于 Python 的自动化工具，用于从 [Kards 官网](https://www.kards.com/) 爬取所有二战题材卡牌游戏 **Kards** 的卡牌图片。

## 🌟 功能特点

- **全自动化爬取**：通过 GraphQL 接口获取所有国家（苏联、美国、日本、德国等）的卡牌信息。
- **多维度分类**：自动按 **国家** 和 **花费 (Kredit)** 创建文件夹，分类保存图片。
- **图片格式转换**：自动将官方使用的 `AVIF` 高压缩格式转换为通用的 `PNG` 格式。
- **智能重命名**：优先使用卡牌的中文名称命名文件，若无中文名则使用原始 ID。
- **防封禁机制**：内置请求延时和 `curl_cffi` 浏览器指纹模拟，保障稳定爬取。

## 📂 目录结构示例

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

## 🛠️ 安装依赖

通过 `requirements.txt` 一键安装：

```bash
pip install -r requirements.txt
```

核心依赖：`requests` (API 请求)、`curl_cffi` (图片下载，含指纹模拟)、`Pillow` (图片格式转换)。

## 🚀 使用方法

直接运行主程序即可：

```bash
python main.py
```

脚本会自动完成：
1. 爬取所有国家、所有费用的常规卡牌
2. 自动下载 3 张特殊的中立卡牌（生产、溃军、计划）

所有图片保存在 `imgs/` 文件夹中。

## 📁 项目结构

```
main.py                 # 入口文件，脚本启动
src/
    config.py           # 配置常量（API 地址、请求头、国家/费用参数、GraphQL 查询）
    image.py            # 图片下载模块（基于 curl_cffi + Pillow）
    scraper.py          # 爬取主逻辑（分页、去重、编排）
```

## ⚙️ 核心逻辑说明

- **GraphQL API**：向 `https://herokuapi.kards.com/graphql` 发送 POST 请求获取分页数据。
- **数据过滤**：包含 `showSpawnables`（衍生牌）、`showExiles`（流亡牌）、`showReserved`（预备牌）。
- **去重机制**：通过 `cardId` 追踪已下载的卡牌，避免重复。
- **异常处理**：自动跳过已存在图片，清理文件名中的非法字符。

## ⚙ 配置项

修改 `src/config.py` 进行调整：

- **国家**：`NATION_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9]`
- **费用**：`KOSTS = [0, 1, 2, 3, 4, 5, 6, 7]`
- **语言**：修改 `IMAGE_BASE_URL` 中的语言段（如 `zh-Hans` → `en-EN`）
- **代理**：按需更新 `PROXIES`

## ⚠️ 注意事项

- 本工具仅供个人学习及研究使用，请勿用于大规模商业用途。
- 请尊重游戏官方的版权，合理控制爬取频率。
