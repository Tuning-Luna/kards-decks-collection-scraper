[English](./README.md) | [中文](./README-zh.md)

# Kards Card Crawler (Kards 卡牌爬取工具)

这是一个基于 Python 的自动化工具，用于从 [Kards 官网](https://www.kards.com/) 爬取所有二战题材卡牌游戏 **Kards** 的卡牌图片。

## 🌟 功能特点

- **全自动化爬取**：通过 GraphQL 接口获取所有国家（苏联、美国、日本、德国等）的卡牌信息。
- **多维度分类**：自动按 **国家** 和 **花费 (Kredit)** 创建文件夹，分类保存图片。
- **图片格式转换**：自动将官方使用的 `AVIF` 高压缩格式转换为通用的 `PNG` 格式。
- **智能重命名**：优先使用卡牌的中文名称命名文件，若无中文名则使用原始 ID。
- **防封禁机制**：内置请求延时（1秒）和 Session 复用，保护爬虫稳定运行。

## 📂 目录结构示例

运行后，图片将按以下结构保存：

```
imgs/
├── 苏联/
│   ├── 0k/
│   │   └── 步兵第13步兵团.png
│   └── 1k/
│       └── 扫射.png
├── 美国/
└── ...
```

## 🛠️ 安装依赖

在使用之前，请确保你的环境中安装了 `requests` 和 `Pillow`（用于图片处理）：

Bash

```
pip install requests Pillow
```

## 🚀 使用方法

1. **准备文件**：确保项目目录下有两个 Python 文件：

   - `main.py` (包含爬虫主循环的代码)
   - `get_img.py` (包含图片下载和转换函数的代码)

2. **运行程序**：

   ```bash
   python main.py
   ```

3. **查看结果**：程序运行结束后，所有卡牌图片将出现在 `imgs/` 文件夹中。

4. 但是无法爬取到中立卡牌，所以我又在`get_imgs.py`里面补充了，还需要运行：
   ```bash
   python get_img.py
   ```

   即可获得全部的中立卡牌。



## ⚙️ 核心逻辑说明

- **GraphQL API**：程序通过向 `https://api.kards.com/graphql` 发送 POST 请求来获取分页数据。
- **数据过滤**：目前脚本配置为获取包含：
  - `showSpawnables`: 衍生牌
  - `showExiles`: 流亡牌
  - `showReserved`: 预备牌（退环境卡牌）
- **异常处理**：脚本会自动跳过已下载的图片，并清理文件名中的非法字符（如 `<>:"/\|?*`）。

## ⚙ 配置项

可以修改：

### 国家

```
nationIds = [1,2,3,4,5,6,7,8,9]
```

### 费用（Kredits）

```
kosts = [0,1,2,3,4,5,6,7]
```

### 语言

在`get_img.py`文件的`save_card_image`中有个`base_url`，修改里面的语言即可

```python
base_url = "https://www.kards.com/images/card/v47/zh-Hans/"
```

## ⚠️ 注意事项

- 本工具仅供个人学习及研究使用，请勿用于大规模商业用途。
- 请尊重游戏官方的版权，合理控制爬取频率。

