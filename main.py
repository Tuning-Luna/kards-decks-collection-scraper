"""Kards 卡牌爬虫 —— 入口"""

import argparse
import logging

from src.scraper import scrape_all_cards


def main():
    parser = argparse.ArgumentParser(description="Kards 卡牌全量爬取")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="输出 DEBUG 级别的详细日志",
    )
    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG if args.debug else logging.INFO,
    )

    scrape_all_cards()


if __name__ == "__main__":
    main()
