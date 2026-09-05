"""卡牌图片下载模块"""

import logging
import os
import time
from io import BytesIO

from curl_cffi import requests
from curl_cffi.const import CurlHttpVersion
from PIL import Image

from src.config import IMAGE_BASE_URL, PROXIES

logger = logging.getLogger(__name__)


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
                http_version=CurlHttpVersion.V1_0,
            )

            if response.status_code != 200:
                logger.warning("[%d] 请求失败 %s: %s", attempt + 1, response.status_code, img_url)
                continue

            try:
                img = Image.open(BytesIO(response.content)).convert("RGBA")
            except Exception as img_err:
                logger.warning("[%d] 图片解码失败: %s", attempt + 1, img_err)
                continue

            if custom_filename:
                save_name = custom_filename + ".png"
            else:
                base_name, _ = os.path.splitext(card_name)
                save_name = base_name + ".png"

            path = os.path.join(dest_dir, save_name)
            img.save(path, "PNG")

            logger.info("已保存 %s", path)
            return True

        except Exception as e:
            logger.warning("[%d] 失败: %s", attempt + 1, e)
            time.sleep(1)

    logger.error("最终失败: %s", card_name)
    return False
