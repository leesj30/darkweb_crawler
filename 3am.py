import requests
from bs4 import BeautifulSoup
import json
import os

# Tor 네트워크 설정
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# 웹 페이지 URL
url = 'http://threeamkelxicjsaf2czjyz2lc4q3ngqkxhhlexyfcp2o6raw4rphyad.onion'

# Tor 네트워크를 통해 페이지 요청 및 BeautifulSoup 객체 생성
try:
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    print("Successfully fetched the webpage.")

    soup = BeautifulSoup(response.content, 'html.parser')

    # 'post bad' 클래스의 모든 포스트 찾기
    posts = soup.find_all('div', class_='post bad')
    print(f"Found {len(posts)} posts.")

    if not posts:
        print("No posts found. The structure of the webpage might have changed or the webpage is empty.")
    
    # JSON 파일 저장 경로
    output_dir = r'E:\DarkWeb_Crawling\JSON\3am'
    os.makedirs(output_dir, exist_ok=True)

    # 각 포스트에서 타이틀과 텍스트 정보를 추출하여 개별 JSON 파일로 저장
    for idx, post in enumerate(posts):
        print(f"Post {idx + 1} HTML: {post.prettify()}")  # 각 포스트의 HTML 출력

        title_block = post.find('div', class_='post-title-block')
        text_block = post.find('div', class_='post-body').find('div', class_='post-text')  # post-text 요소 찾기

        if title_block and text_block:
            title = title_block.get_text(strip=True)
            text = text_block.get_text(strip=True)
            
            # 파일 이름으로 사용할 수 있도록 타이틀에서 공백을 '_'로 변경
            file_name = title.replace(' ', '_') + '.json'
            output_file = os.path.join(output_dir, file_name)
            
            # 데이터를 딕셔너리로 저장
            data = {
                'title': title,
                'text': text
            }

            # JSON 파일로 저장
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f'크롤링 데이터가 {output_file}에 저장되었습니다. 데이터: {data}')
        else:
            print(f"Post {idx + 1} is missing title_block or text_block")

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')