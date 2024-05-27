import requests
from bs4 import BeautifulSoup
import json
import os
import re

# Tor 네트워크를 통한 프록시 설정
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# 다크웹 시드 URL 설정
seed_url = "http://bianlianlbc5an4kgnay3opdemgcryg2kpfcbgczopmm3dnbz3uaunad.onion"

# JSON 파일을 저장할 디렉토리 설정
save_dir = "E:\\DarkWeb_Crawling\\JSON"

# 디렉토리가 존재하지 않으면 생성
os.makedirs(save_dir, exist_ok=True)

# 파일명을 안전하게 변환하는 함수
def safe_filename(filename):
    # 공백을 '_'로 변환하고 '&'를 제거
    filename = filename.replace(' ', '_').replace('&', '')
    # 불법 문자 제거
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Tor 네트워크를 통해 웹페이지 요청
try:
    response = requests.get(seed_url, proxies=proxies)
    response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

    # 요청이 성공했는지 확인
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 모든 포스트를 찾아서 처리
        posts = soup.find_all('section', class_='list-item')
        for post in posts:
            # 1. 타이틀 추출
            title = post.find('h1', class_='title').get_text(strip=True)
            
            # 2. 설명 정보 추출
            description = post.find('div', class_='description').get_text(strip=True)
            
            # 3. 'read more'에 있는 URL 추출
            read_more_link = post.find('a', class_='readmore')['href']
            
            # 결과를 저장할 딕셔너리 초기화
            result = {
                'title': title,
                'description': description,
                'read_more_url': read_more_link,
                'additional_info': None
            }
            
            # 4. 'read more' 링크를 따라가 추가 정보 추출
            additional_url = seed_url + read_more_link
            response_additional = requests.get(additional_url, proxies=proxies)
            
            if response_additional.status_code == 200:
                soup_additional = BeautifulSoup(response_additional.content, 'html.parser')
                
                # 추가로 추출하고자 하는 정보를 추출
                additional_info = soup_additional.find('div', class_='additional-info')
                if additional_info:
                    result['additional_info'] = additional_info.get_text(strip=True)
            
            # 결과를 JSON 파일로 저장
            filename = os.path.join(save_dir, f"{safe_filename(title)}.json")
            with open(filename, 'w') as json_file:
                json.dump(result, json_file, indent=4)
            
            print(f"{filename} 저장 완료")
    else:
        print("다크웹 페이지 접근 실패:", response.status_code)
except requests.exceptions.RequestException as e:
    print("서버 요청 중 오류 발생:", e)