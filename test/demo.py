import requests
import json


headers = {
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "content-type": "application/json",
    "origin": "https://www.kards.com",
    "priority": "u=1, i",
    "referer": "https://www.kards.com/",
    "sec-ch-ua": "\"Google Chrome\";v=\"149\", \"Chromium\";v=\"149\", \"Not)A;Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}
url = "https://herokuapi.kards.com/graphql"
data = {
    "operationName": "getCards",
    "variables": {
        "language": "zh",
        "set": "OnlySpawnable",
        "showSpawnables": True,
        "showExiles": False,
        "showReserved": False
    },
    "query": "query getCards($language: String, $offset: Int, $nationIds: [Int], $kredits: [Int], $q: String, $type: [String], $rarity: [String], $set: [String], $showSpawnables: Boolean, $showExiles: Boolean, $showReserved: Boolean) {\n  cards(\n    language: $language\n    first: 20\n    offset: $offset\n    nationIds: $nationIds\n    kredits: $kredits\n    q: $q\n    type: $type\n    set: $set\n    rarity: $rarity\n    showSpawnables: $showSpawnables\n    showExiles: $showExiles\n    showReserved: $showReserved\n  ) {\n    pageInfo {\n      count\n      hasNextPage\n      __typename\n    }\n    edges {\n      node {\n        id\n        cardId\n        importId\n        json\n        reserved\n        imageUrl: image(language: $language)\n        thumbUrl: image(type: thumb, language: $language)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data)

print(response.text)