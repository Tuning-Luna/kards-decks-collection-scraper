# Kards 卡牌爬虫 — 项目指引

## 项目结构

```
main.py                 # 入口文件，全量爬取（支持 --debug 输出详细日志）
src/
    config.py           # 配置常量(API、请求头、代理、国家/费用参数、GraphQL 查询、请求参数)
    utils.py            # 通用工具（sanitize_filename 文件名清洗）
    image.py            # 图片下载模块（curl_cffi + Pillow，AVIF → PNG）
    scraper.py          # 爬取主逻辑（遍历国家×费用，分页拉取并下载，断点续传）
```

## 运行方式

- `python main.py`               — 全量爬取（推荐）
- `python main.py --debug`       — 全量爬取并输出 DEBUG 详细日志
- `python -m src.scraper`        — 同上（不带 --debug）

## 断点续传

- 进度记录在 `progress.json`（已忽略，不入库）：每个「国家×费用」组合完成后写入
- 组合请求重试仍失败或图片下载失败时**不**标记完成，下次运行自动续爬该组合
- 已存在的图片文件会跳过，不会重复下载

## 代理

- 国内用户需把 `PROXIES` 改为本机代理客户端端口（详见 README，默认 `127.0.0.1:7897` 只是作者本机 Clash 端口）

## 依赖

- `curl_cffi` — GraphQL API 与图片下载（走代理 + 浏览器指纹模拟）
- `Pillow` — 图片格式转换与保存
