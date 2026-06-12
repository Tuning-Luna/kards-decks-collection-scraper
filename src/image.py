"""卡牌图片下载模块"""

import os
import time
from io import BytesIO

from PIL import Image
from curl_cffi import requests

from src.config import IMAGE_BASE_URL, PROXIES


def save_card_image(card_name, custom_filename=None, dest_dir="imgs", retry=3):
    """
    下载并保存单张卡牌图片

    Args:
        card_name: 图片文件名 (如 "12th_guards_mechanised.avif")
        custom_filename: 自定义保存文件名 (不含扩展名)
        dest_dir: 目标目录
        retry: 重试次数
    Returns:
        bool: 是否成功
    """
    img_url = IMAGE_BASE_URL + card_name

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.kards.com/",
    }

    os.makedirs(dest_dir, exist_ok=True)

    for attempt in range(retry):
        try:
            time.sleep(0.5)

            response = requests.get(
                img_url,
                headers=headers,
                impersonate="chrome110",
                proxies=PROXIES,
                timeout=20,
                verify=True,
                http_version=1,
            )

            if response.status_code != 200:
                print(f"[{attempt + 1}] 请求失败 {response.status_code}: {img_url}")
                continue

            try:
                img = Image.open(BytesIO(response.content)).convert("RGBA")
            except Exception as img_err:
                print(f"[{attempt + 1}] 图片解码失败: {img_err}")
                continue

            if custom_filename:
                save_name = custom_filename + ".png"
            else:
                base_name, _ = os.path.splitext(card_name)
                save_name = base_name + ".png"

            invalid_chars = '<>:"/\\|?*'
            for c in invalid_chars:
                save_name = save_name.replace(c, "_")

            path = os.path.join(dest_dir, save_name)
            img.save(path, "PNG")

            print(f"✔ 已保存 {path}")
            return True

        except Exception as e:
            print(f"[{attempt + 1}] 失败: {e}")
            time.sleep(1)

    print(f"❌ 最终失败: {card_name}")
    return False
