[English](./README.md) | [中文](./README-zh.md)

# Kards Card Crawler（Kards 卡牌爬虫）

自动下载 [Kards](https://www.kards.com/) 所有卡牌图片的 Python 工具。

## 工作原理

1. **GraphQL API** — 请求 `https://herokuapi.kards.com/graphql` 获取卡牌元数据（名称、阵营、费用、图片路径）
2. **图片下载** — 通过 `curl_cffi`（浏览器指纹模拟）从 CDN 拉取 AVIF 格式原图
3. **格式转换** — 用 Pillow 将 AVIF 转为 PNG

爬虫遍历所有阵营（11 个国家 + 中立）和费用（0–7），自动分页并去重。

## 目录结构

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

文件名格式 `{中文名}_{cardId}.png`，无中文名则回退为 `unknown_{cardId}.png`。

## 使用

```bash
git clone https://github.com/Tuning-Luna/kards-decks-collection-scraper.git
cd kards-decks-collection-scraper
pip install -r requirements.txt
python main.py
```

## 配置项

编辑 `src/config.py`：

| 配置             | 说明                     | 默认值                     |
| ---------------- | ------------------------ | -------------------------- |
| `NATION_IDS`     | 阵营 ID 列表（0 = 中立） | `[1..10, 0]`               |
| `KOSTS`          | 卡牌费用范围             | `[0, 1, 2, 3, 4, 5, 6, 7]` |
| `IMAGE_BASE_URL` | 修改语言段切换语言       | `.../zh-Hans/`             |
| `PROXIES`        | HTTP/HTTPS 代理          | `http://127.0.0.1:7897`    |

> ⚠️ **国内用户注意**:Kards 的 API 与 CDN 需通过可访问国外网络的代理才能拉取成功。
> 仓库默认的 `PROXIES` 端口（`7897`）是作者本机 Clash 的端口,**不一定适用于你的电脑**。
> 请务必把它改成你自己代理软件的监听端口（例如 Clash 默认 `7890`、v2rayN 默认 `10809`、SSR 默认 `1080`
> 等，以你本地代理客户端的实际设置为准），否则请求会因无法连接代理而失败。
>
> 如果你本机没有代理客户端，将 `PROXIES` 设为 `{"http": "", "https": ""}` 即可走直连（仅当你的网络
> 能直接访问 `kards.com` 时可用）。

## 项目结构

```
main.py                 # 入口
src/
    config.py           # API 配置、请求头、GraphQL 查询、阵营/费用参数
    scraper.py          # 爬取主逻辑（分页、去重、编排）
    image.py            # AVIF → PNG 下载（curl_cffi + Pillow）
```

## 免责声明

仅供个人学习研究。请合理控制爬取频率，尊重游戏版权。
