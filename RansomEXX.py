import os
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# Tor 프록시 설정
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# 크롤링할 URL
url = "http://rnsm777cdsjrsdlbs4v5qoeppu3px6sb2igmh53jzrx7ipcrbjz5b2ad.onion/"

# JSON 파일 저장 디렉토리 설정
output_dir = "E:\\DarkWeb_Crawling\\JSON\\RansomEXX"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    # 요청 보내기
    response = requests.get(url, proxies=proxies, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # 모든 포스트 찾기
    posts = soup.find_all('article')

    # 포스트 정보 추출 및 저장
    for post in posts:
        try:
            title_tag = post.find('h2', class_='entry-title').find('a')
            title = title_tag.get('href') if title_tag else 'No Title'
            title = title.split('/')[-2]  # 타이틀에서 파일명 부분만 추출
            
            datetime_tag = post.find('time', class_='entry-date published')
            datetime_str = datetime_tag.get('datetime') if datetime_tag else None
            if datetime_str:
                datetime_str = datetime_str.replace('T', ' ')
            datetime_obj = datetime.fromisoformat(datetime_str) if datetime_str else 'No Date'

            entry_summary_tag = post.find('div', class_='entry-summary')
            entry_summary = entry_summary_tag.text.strip() if entry_summary_tag else 'No Summary'

            # Leaked data size 추출
            leaked_data_size_match = re.search(r'Leaked data size: ([\d.]+[A-Z]+)', entry_summary)
            leaked_data_size = leaked_data_size_match.group(1) if leaked_data_size_match else 'No Data Size'

            # entry_summary에서 Leaked data size 부분 제거
            entry_summary = re.sub(r'\nLeaked data size: [\d.]+[A-Z]+.', '', entry_summary)

            country_tag_tag = post.find('a', rel='tag')
            country_tag = country_tag_tag.get('href') if country_tag_tag else 'No Country'

            # 파일명 생성 (공백을 '_'로 변환, '&' 제거, 불법 문자 제거)
            filename = re.sub(r'[^\w\s-]', '', title).replace(' ', '_').replace('&', '')
            filepath = os.path.join(output_dir, f"{filename}.json")
            
            # JSON 데이터 생성
            data = {
                'title': title,
                'datetime': datetime_obj.isoformat() if isinstance(datetime_obj, datetime) else datetime_str,
                'entry_summary': entry_summary,
                'leaked_data_size': leaked_data_size
            }
            
            # JSON 파일 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error processing post: {e}")

    print("Crawling and saving complete.")
except requests.RequestException as e:
    print(f"Error fetching the page: {e}")