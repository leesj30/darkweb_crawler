import os
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Selenium을 사용하여 웹 페이지 로드
def fetch_url_with_selenium(url):
    # Chrome 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--proxy-server=socks5://127.0.0.1:9050')  # Tor 프록시 설정

    # ChromeDriver 경로 설정 및 드라이버 초기화
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL 로드
    driver.get(url)
    
    try:
        # 페이지가 로드될 때까지 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'post bad'))
        )
    except:
        print("페이지 로드 대기 중 오류 발생")
    
    # 페이지 소스 가져오기
    page_source = driver.page_source
    driver.quit()
    return page_source

# 파일명을 안전하게 변환하는 함수
def safe_filename(filename):
    filename = filename.replace(' ', '_').replace('&', '')
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# JSON 파일을 저장할 디렉토리 설정
save_dir = "E:\\DarkWeb_Crawling\\JSON\\Blackbasta"
os.makedirs(save_dir, exist_ok=True)

# 웹 페이지 로드할 URL 설정
url = 'http://stniiomyjliimcgkvdszvgen3eaaoz55hreqqx6o77yvmpwt7gklffqd.onion/'

# 웹 페이지 로드
html = fetch_url_with_selenium(url)
soup = BeautifulSoup(html, 'html.parser')

# 페이지 소스 출력 (디버깅용)
print(soup.prettify())

posts = soup.find_all('div', class_='post bad')
print(f"Found {len(posts)} posts.")

for post in posts:
    title = post.find('div', class_='post-title-block').get_text(strip=True)
    text = post.find('div', class_='post-text').get_text(strip=True)
    more_link = post.find('a', class_='post-more-link')

    if more_link:
        more_href = more_link.get('onclick')
        if more_href and "location.href=" in more_href:
            more_href = more_href.split("location.href='")[1].split("'")[0]
            more_url = url + more_href
            additional_html = fetch_url_with_selenium(more_url)
            additional_soup = BeautifulSoup(additional_html, 'html.parser')
            additional_info = additional_soup.get_text(strip=True)
        else:
            additional_info = ""

        result = {
            'title': title,
            'text': text,
            'more_url': more_url,
            'additional_info': additional_info
        }

        filename = os.path.join(save_dir, f"{safe_filename(title)}.json")
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, indent=4, ensure_ascii=False)

        print(f"{filename} 저장 완료")