"""Kards 卡牌爬取主逻辑 —— 遍历国家与费用，分页拉取所有卡牌信息并下载图片"""

import json
import os
import time

from curl_cffi import requests  # noqa: ICN001 — 项目统一用 curl_cffi 以便走代理

from src.config import (
    API_URL,
    CARDS_QUERY,
    HEADERS,
    KOSTS,
    NATION_IDS,
    NATION_NAMES,
    PROXIES,
    REQUEST_TIMEOUT,
    RETRY,
)
from src.image import save_card_image
from src.utils import sanitize_filename

# 分页大小（与 CARDS_QUERY 中 first: 20 保持一致）
PAGE_SIZE = 20
# 断点续传文件，记录已完成的国家×费用组合（格式 "国家ID_费用"）
CHECKPOINT_FILE = "progress.json"


def fetch_card_page(nid, k, offset):
    """请求单个分页，返回 (edges, has_next) 二元组。

    请求异常或非 2xx 时抛出 requests.exceptions.RequestException（由调用方决定续爬）；
    响应结构缺失 data.cards 时返回空列表（视为无更多数据）。
    """
    variables_payload = {
        "language": "zh",
        "showSpawnables": True,
        "showExiles": True,
        "showReserved": True,
        "kredits": [k],
        "offset": offset,
    }
    # 不为 0 时添加国家 ID，否则爬取所有国家（只剩中立国家）
    if nid != 0:
        variables_payload["nationIds"] = [nid]

    json_data = {
        "operationName": "getCards",
        "variables": variables_payload,
        "query": CARDS_QUERY,
    }

    for attempt in range(1, RETRY + 1):
        try:
            time.sleep(1)
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json=json_data,
                proxies=PROXIES,
                timeout=REQUEST_TIMEOUT,
                impersonate="chrome110",
                verify=True,
            )
            response.raise_for_status()
            data = response.json()
            cards = data.get("data", {}).get("cards", {})
            if not cards:
                return [], False
            return cards.get("edges", []), cards.get("pageInfo", {}).get("hasNextPage", False)
        except requests.exceptions.RequestException as e:
            print(f"请求失败（第 {attempt}/{RETRY} 次）：{e}")
            time.sleep(2**attempt)

    raise requests.exceptions.RequestException(
        f"请求重试 {RETRY} 次仍失败：nid={nid} k={k} offset={offset}"
    )


def parse_card_node(node):
    """从单个节点解析出下载所需元数据。

    返回 (card_id, image_name, title)；缺少 image 或 cardId 时返回 None。
    """
    node_json = node.get("json") or {}
    card_id = node.get("cardId")
    image_name = node_json.get("image")
    if not (image_name and card_id):
        return None

    chinese_name = node_json.get("title", {}).get("zh-Hans")
    title = sanitize_filename(chinese_name if chinese_name else "unknown")
    return card_id, image_name, title


def _load_checkpoint():
    """读取断点文件，返回已完成组合的集合；文件缺失或损坏时返回空集合。"""
    try:
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("completed", []))
    except (FileNotFoundError, ValueError):
        return set()


def _save_checkpoint(completed):
    """将已完成组合集合写入断点文件（先写临时文件再原子替换，避免中断损坏）。"""
    tmp = CHECKPOINT_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"completed": sorted(completed)}, f, ensure_ascii=False, indent=2)
    os.replace(tmp, CHECKPOINT_FILE)


def scrape_all_cards():
    """遍历所有国家与费用组合，分页爬取卡牌并下载图片，支持断点续传。

    每个「国家×费用」组合完成后写入 checkpoint；组合发生未捕获异常或
    有图片下载失败时**不**标记完成，下次运行会重新尝试该组合。
    """
    completed = _load_checkpoint()
    downloaded_ids = set()
    selected_nation_ids = NATION_IDS if NATION_IDS else list(NATION_NAMES.keys())

    for nid in selected_nation_ids:
        nname = NATION_NAMES.get(nid, str(nid))
        for k in KOSTS:
            key = f"{nid}_{k}"
            if key in completed:
                print(f"跳过已完成组合：{key}（{nname}，{k}k）")
                continue

            failed_downloads = 0
            offset = 0
            while True:
                try:
                    edges, has_next = fetch_card_page(nid, k, offset)
                except requests.exceptions.RequestException as e:
                    print(f"组合 {key} 请求最终失败：{e}，本组合不标记完成，下次续爬")
                    failed_downloads = -1  # 标记为整体失败
                    break

                for edge in edges:
                    parsed = parse_card_node(edge.get("node", {}))
                    if parsed is None:
                        continue
                    card_id, image_name, title = parsed
                    save_name = f"{title}_{card_id}"
                    dest_dir = os.path.join("imgs", nname, f"{k}k")

                    if card_id in downloaded_ids:
                        print(f"已下载过，跳过：{card_id}")
                        continue

                    target_path = os.path.join(dest_dir, save_name + ".png")
                    if os.path.exists(target_path):
                        print(f"文件已存在，跳过：{target_path}")
                        downloaded_ids.add(card_id)
                        continue

                    if save_card_image(image_name, save_name, dest_dir):
                        downloaded_ids.add(card_id)
                    else:
                        failed_downloads += 1

                if has_next:
                    offset += PAGE_SIZE
                else:
                    break

            if failed_downloads:
                reason = "请求失败" if failed_downloads < 0 else f"{failed_downloads} 张图片下载失败"
                print(f"组合 {key} {reason}，不标记完成，下次续爬")
                continue

            completed.add(key)
            _save_checkpoint(completed)
            print(f"完成组合：{key}（{nname}，{k}k）")

    print("爬取完成")


if __name__ == "__main__":
    scrape_all_cards()
