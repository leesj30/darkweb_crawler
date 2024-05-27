import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
from driver_settings import driver_settings

#pip install selenium webdriver-manager beautifulsoup4 stem requests[socks] 필요
#cmd창에서 tor 실행 필요

# 웹사이트 크롤링 함수
def crawl_site(site_url, site_name):
    driver = driver_settings()
    driver.get(site_url)

    # 페이지 HTML 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 게시글 정보 추출 (카드별로 title, url, text, links)
    cards = soup.select('.card')
    for idx, card in enumerate(cards):
        title = card.select_one('.title').text if card.select_one('.title') else 'No title'
        url = card.select_one('.url').text if card.select_one('.url') else 'No url'
        text = card.select_one('.text').text if card.select_one('.text') else 'No text'
        links = [a['href'] for a in card.select('.links a')] if card.select('.links a') else []

        post_data = {
            'title': title,
            'url': url,
            'text': text,
            'links': links
        }

        # JSON 파일로 저장 (카드별로 개별 파일)
        json_file_path = f"{site_name}_post_{idx+1}.json"
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, ensure_ascii=False, indent=4)

        print(f"Post data has been saved to {json_file_path}")

    driver.quit()

crawl_site('http://weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion/', 'blacksuite')

