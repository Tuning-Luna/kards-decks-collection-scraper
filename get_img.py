import requests
import os
import time
from PIL import Image
from io import BytesIO

# 使用全局会话对象，避免重复创建
session = requests.Session()


def save_card_image(card_name, custom_filename=None, dest_dir="imgs"):
    """
    下载卡牌图片并将 avif 格式转换为 png，保存到 imgs/ 目录下
    :param card_name: 原始图片文件名 (如 "convoy_attack.avif")
    :param custom_filename: 可选的自定义保存文件名 (如 "护航攻击")，不需要带后缀
    """
    base_url = "https://www.kards.com/images/card/v47/zh-Hans/"
    img_url = base_url + card_name

    headers = {
        "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "accept-language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "i",
        "referer": "https://www.kards.com/zh/decks/collection",
        "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "image",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    }

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    try:
        time.sleep(1)

        response = session.get(img_url, headers=headers)
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


if __name__ == "__main__":
    # 测试代码
    test_card = "convoy_attack.avif"
    save_card_image(test_card)
