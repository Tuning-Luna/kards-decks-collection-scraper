"""Kards 卡牌爬虫 — 入口文件"""

from src.scraper import scrape_all_cards
from src.image import download_neutral_cards

if __name__ == "__main__":
    scrape_all_cards()
    download_neutral_cards()
