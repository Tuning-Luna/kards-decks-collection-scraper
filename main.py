import requests
import os
from get_img import save_card_image

# 爬取Kards所有卡牌

headers = {
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://www.kards.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.kards.com/",
    "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
}

kosts = [0, 1, 2, 3, 4, 5, 6, 7]
nationIds = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 不会使用，只是为了方便查看
nation_names = {
    1: "苏联",
    2: "美国",
    3: "日本",
    4: "德国",
    5: "英国",
    6: "法国",
    7: "意大利",
    8: "波兰",
    9: "芬兰",
}

# 用于记录已经下载过的 cardId
downloaded_ids = set()

selected_nation_ids = nationIds if nationIds else list(nation_names.keys())

for nid in selected_nation_ids:
    nname = nation_names.get(nid, str(nid))
    for k in kosts:
        offset = 0
        while True:
            variables_payload = {
                "language": "zh",
                "showSpawnables": True,  # 是否包含衍生牌
                "showExiles": True,  # 是否包含流亡牌
                "showReserved": True,  # 是否包含预备牌
                "nationIds": [nid],  # 国家ID
                "kredits": [k],  # 费用
                "offset": offset,  # 分页偏移量，每次请求20条
            }

            json_data = {
                "operationName": "getCards",
                "variables": variables_payload,
                "query": "query getCards($language: String, $offset: Int, $nationIds: [Int], $kredits: [Int], $q: String, $type: [String], $rarity: [String], $set: [String], $showSpawnables: Boolean, $showExiles: Boolean, $showReserved: Boolean) {\n  cards(\n    language: $language\n    first: 20\n    offset: $offset\n    nationIds: $nationIds\n    kredits: $kredits\n    q: $q\n    type: $type\n    set: $set\n    rarity: $rarity\n    showSpawnables: $showSpawnables\n    showExiles: $showExiles\n    showReserved: $showReserved\n  ) {\n    pageInfo {\n      count\n      hasNextPage\n      __typename\n    }\n    edges {\n      node {\n        id\n        cardId\n        importId\n        json\n        reserved\n        imageUrl: image(language: $language)\n        thumbUrl: image(type: thumb, language: $language)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
            }

            response = requests.post(
                "https://herokuapi.kards.com/graphql", headers=headers, json=json_data
            )

            data = response.json()
            if "data" not in data or "cards" not in data["data"]:
                break

            edges = data["data"]["cards"]["edges"]
            for edge in edges:
                node = edge.get("node", {})
                card_json = node.get("json", {})

                card_id = node.get("cardId")  # 用这个做唯一标识,而不是中文
                image_name = card_json.get("image")
                chinese_name = card_json.get("title", {}).get("zh-Hans")

                if image_name and card_id:

                    import re

                    def sanitize_filename(name):
                        return re.sub(r'[\\/:*?"<>|]', "_", name)

                    title = chinese_name if chinese_name else "unknown"
                    title = sanitize_filename(title)

                    save_name = f"{title}_{card_id}"

                    dest_dir = os.path.join("imgs", nname, f"{k}k")
                    os.makedirs(dest_dir, exist_ok=True)

                    target_path = os.path.join(dest_dir, save_name + ".png")

                    # 优先用 card_id 判断是否重复
                    if card_id in downloaded_ids:
                        print(f"已下载过，跳过：{card_id}")
                        continue

                    # 如果文件已存在，也加入集合
                    if os.path.exists(target_path):
                        print(f"文件已存在，跳过：{target_path}")
                        downloaded_ids.add(card_id)
                        continue

                    # 下载
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
