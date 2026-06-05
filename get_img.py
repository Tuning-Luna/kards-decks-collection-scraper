import os
import time
from PIL import Image
from io import BytesIO
from curl_cffi import requests

proxies = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897",
}

def save_card_image(card_name, custom_filename=None, dest_dir="imgs", retry=3):
    base_url = "https://www.kards.com/images/card/v48/zh-Hans/"
    # v47：国土阵线
    # v48：国土阵线：早期战争
    img_url = base_url + card_name

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
                proxies=proxies,
                timeout=20,
                verify=True,
                http_version=1,
            )

            if response.status_code != 200:
                print(f"[{attempt+1}] 请求失败 {response.status_code}: {img_url}")
                continue

            try:
                img = Image.open(BytesIO(response.content)).convert("RGBA")
            except Exception as img_err:
                print(f"[{attempt+1}] 图片解码失败: {img_err}")
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
            print(f"[{attempt+1}] 失败: {e}")
            time.sleep(1)

    print(f"❌ 最终失败: {card_name}")
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
