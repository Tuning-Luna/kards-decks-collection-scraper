"""Kards 卡牌爬虫 —— 配置常量"""

# GraphQL API 端点
API_URL = "https://herokuapi.kards.com/graphql"

# 卡牌图片基础 URL (v51 = 澳新风暴）
IMAGE_BASE_URL = "https://www.kards.com/images/card/v51/zh-Hans/"

# ---- 代理配置 ----
PROXIES = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897",
}

# ---- HTTP 请求头 ----
HEADERS = {
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

# ---- 爬取参数 ----
# 按费用 (kredit) 筛选
KOSTS = [0, 1, 2, 3, 4, 5, 6, 7]

# 国家 ID 列表（0 = 中立）
NATION_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0]
# 传0的时候爬取所有国家，前面国家爬虫过了，只剩下中立国家

# 国家 ID → 中文名称
NATION_NAMES = {
    1: "苏联",
    2: "美国",
    3: "日本",
    4: "德国",
    5: "英国",
    6: "法国",
    7: "意大利",
    8: "波兰",
    9: "芬兰",
    10:"澳新军团",
    0: "中立"
}

# ---- GraphQL 查询语句 ----
CARDS_QUERY = """\
query getCards($language: String, $offset: Int, $nationIds: [Int], \
$kredits: [Int], $q: String, $type: [String], $rarity: [String], \
$set: [String], $showSpawnables: Boolean, $showExiles: Boolean, $showReserved: Boolean) {
  cards(
    language: $language
    first: 20
    offset: $offset
    nationIds: $nationIds
    kredits: $kredits
    q: $q
    type: $type
    set: $set
    rarity: $rarity
    showSpawnables: $showSpawnables
    showExiles: $showExiles
    showReserved: $showReserved
  ) {
    pageInfo {
      count
      hasNextPage
      __typename
    }
    edges {
      node {
        id
        cardId
        importId
        json
        reserved
        imageUrl: image(language: $language)
        thumbUrl: image(type: thumb, language: $language)
        __typename
      }
      __typename
    }
    __typename
  }
}"""
