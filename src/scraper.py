"""Kards 卡牌爬取主逻辑 —— 遍历国家与费用，分页拉取所有卡牌信息并下载图片"""

import os
import re
import time

import requests

from src.config import API_URL, HEADERS, KOSTS, NATION_IDS, NATION_NAMES, CARDS_QUERY
from src.image import save_card_image


def sanitize_filename(name):
    """将文件名中的非法字符替换为下划线"""
    return re.sub(r'[\\/:*?"<>|]', "_", name)


def scrape_all_cards():
    """遍历所有国家与费用组合，分页爬取卡牌并下载图片"""
    downloaded_ids = set()
    selected_nation_ids = NATION_IDS if NATION_IDS else list(NATION_NAMES.keys())

    for nid in selected_nation_ids:
        nname = NATION_NAMES.get(nid, str(nid))
        for k in KOSTS:
            offset = 0
            while True:
                variables_payload = {
                    "language": "zh",
                    "showSpawnables": True,
                    "showExiles": True,
                    "showReserved": True,
                    "kredits": [k],
                    "offset": offset,
                }
                # 不为0时，添加国家ID，否则爬取所有国家（只剩下中立国家）
                if nid != 0:
                    variables_payload["nationIds"] = [nid]

                json_data = {
                    "operationName": "getCards",
                    "variables": variables_payload,
                    "query": CARDS_QUERY,
                }

                time.sleep(1)

                response = requests.post(
                    API_URL, headers=HEADERS, json=json_data
                )

                data = response.json()
                if "data" not in data or "cards" not in data["data"]:
                    break

                edges = data["data"]["cards"]["edges"]
                for edge in edges:
                    node = edge.get("node", {})
                    card_json = node.get("json", {})

                    card_id = node.get("cardId")
                    image_name = card_json.get("image")
                    chinese_name = card_json.get("title", {}).get("zh-Hans")

                    if not (image_name and card_id):
                        continue

                    title = chinese_name if chinese_name else "unknown"
                    title = sanitize_filename(title)

                    save_name = f"{title}_{card_id}"
                    dest_dir = os.path.join("imgs", nname, f"{k}k")
                    os.makedirs(dest_dir, exist_ok=True)
                    target_path = os.path.join(dest_dir, save_name + ".png")

                    if card_id in downloaded_ids:
                        print(f"已下载过，跳过：{card_id}")
                        continue

                    if os.path.exists(target_path):
                        print(f"文件已存在，跳过：{target_path}")
                        downloaded_ids.add(card_id)
                        continue

                    save_card_image(image_name, save_name, dest_dir)
                    downloaded_ids.add(card_id)

                has_next = (
                    data.get("data", {})
                    .get("cards", {})
                    .get("pageInfo", {})
                    .get("hasNextPage", False)
                )
                if has_next:
                    offset += 20
                else:
                    break

    print("爬取完成")


if __name__ == "__main__":
    scrape_all_cards()
