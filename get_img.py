import requests
import os
import time
from PIL import Image
from io import BytesIO
import httpx
from curl_cffi import requests

# 使用全局会话对象，避免重复创建
# session = requests.Session()

proxies = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897",
}


def save_card_image(card_name, custom_filename=None, dest_dir="imgs"):
    """
    下载卡牌图片并将 avif 格式转换为 png，保存到 imgs/ 目录下
    :param card_name: 原始图片文件名 (如 "convoy_attack.avif")
    :param custom_filename: 可选的自定义保存文件名 (如 "护航攻击")，不需要带后缀
    """
    base_url = "https://www.kards.com/images/card/v48/zh-Hans/"
    # v47：国土阵线
    # v48是目前最新版本：国土阵线：早期战争
    # 之前的版本会403
    img_url = base_url + card_name

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.kards.com/",
    }

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    try:
        time.sleep(1)

        # response = session.get(img_url, headers=headers, timeout=10)

        # client = httpx.Client(headers=headers, http2=True)
        # response = client.get(img_url)

        response = requests.get(
            img_url, headers=headers, impersonate="chrome110", proxies=proxies
        )

        if response.status_code == 200:
            # 将 avif 转为 png
            img = Image.open(BytesIO(response.content))

            if custom_filename:
                # 使用自定义文件名
                save_name = custom_filename + ".png"
            else:
                # 使用原始文件名的 base_name
                base_name, _ = os.path.splitext(card_name)
                save_name = base_name + ".png"

            # 清理文件名中的非法字符
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                save_name = save_name.replace(char, "_")

            new_filename = os.path.join(dest_dir, save_name)

            img.save(new_filename, "PNG")
            print(f"图片已保存为 {new_filename}")
            return True
        else:
            print(f"请求失败，状态码：{response.status_code}, URL: {img_url}")
            return False
    except Exception as e:
        print(f"处理图片 {card_name} 时出错: {e}")
        return False


def save_neutral_card_image(card_name, custom_filename):
    save_card_image(card_name, custom_filename, "imgs/中立")


if __name__ == "__main__":

    production = "production.avif"
    routed_troops = "routed_troops.avif"
    plan = "plan.avif"

    save_neutral_card_image(production, "production_生产")
    save_neutral_card_image(routed_troops, "routed_troops_溃军")
    save_neutral_card_image(plan, "plan_计划")

# save_card_image("2nd_california.avif", "加州_2nd_california", "./")
