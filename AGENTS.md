# Kards 卡牌爬虫 — 项目指引

## 项目结构

```
main.py                 # 入口文件，脚本入口
src/
    config.py           # 配置常量（API、请求头、国家/费用参数、GraphQL 查询）
    image.py            # 图片下载模块（基于 curl_cffi + Pillow）
    scraper.py          # 爬取主逻辑（遍历国家+费用，分页拉取卡牌并下载）
```

## 运行方式

- `python main.py`               — 全量爬取
- `python -m src.scraper`        — 同上
- `python -m src.image`          — 单独下载 3 张中立卡牌

## 依赖

- `requests` — GraphQL API 调用
- `curl_cffi` — 图片下载（含代理 + 浏览器指纹模拟）
- `Pillow` — 图片格式转换与保存
