import json
import os
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from discord import send_to_discord
from driver_settings import settings

#pip install selenium webdriver-manager beautifulsoup4 stem requests[socks] 필요
#cmd창에서 tor 실행 필요

def create_save_dir(base_directory='json', site_name=''):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(script_dir, base_directory, site_name)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def get_existing_post_hashes(save_dir):
    existing_hashes = set()
    for filename in os.listdir(save_dir):
        if filename.endswith('.json'):
            existing_hashes.add(filename[:-5])  # Remove .json extension
    return existing_hashes

def hash_data(*args):
    hasher = hashlib.md5()
    for arg in args:
        hasher.update(arg.encode('utf-8'))
    return hasher.hexdigest()

def save_post_data(save_dir, post_data, hash_value):
    json_file_path = os.path.join(save_dir, f"{hash_value}.json")
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(post_data, f, ensure_ascii=False, indent=4)
    print(f"Post data has been saved to {json_file_path}")

# 웹사이트 크롤링 함수
def crawl_blacksuite(site_url, site_name):
    
    driver = settings()
    driver.get(site_url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    save_dir = create_save_dir('json', site_name)
    # 기존에 저장된 포스트 URL 읽기
    existing_hashes = get_existing_post_hashes(save_dir)

    # 게시글 정보 추출 (카드별로 title, url, text, links)
    cards = soup.select('.card')
    for idx, card in enumerate(cards):
        title = card.select_one('.title').text if card.select_one('.title') else 'No title'
        url = card.select_one('.url').text if card.select_one('.url') else 'No url'
        text = card.select_one('.text').text if card.select_one('.text') else 'No text'
        links = [a['href'] for a in card.select('.links a')] if card.select('.links a') else []

        post_data = {
            'title': title,
            'text': text,
            'links': links,
            'operator':'blacksuite'
        }

     # Create a hash from title and url
        hash_value = hash_data(title, url)

        if hash_value not in existing_hashes:
            save_post_data(save_dir, post_data, hash_value)
            send_to_discord('blacksuite', 'post_data', post_data)

    driver.quit()
    
def crawl_bianlianl(url, site_name):
    proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
    }
    save_dir = create_save_dir('json', site_name)
    existing_hashes = get_existing_post_hashes(save_dir)
    
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Initial request error: {e}')
        return

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
                'additional_info': None,
                'operator':'bianlianl'
            }
            
            # 4. 'read more' 링크를 따라가 추가 정보 추출
            additional_url = url + read_more_link
            response_additional = requests.get(additional_url, proxies=proxies)
            
            if response_additional.status_code == 200:
                soup_additional = BeautifulSoup(response_additional.content, 'html.parser')
                
                # 추가로 추출하고자 하는 정보를 추출
                additional_info = soup_additional.find('div', class_='additional-info')
                if additional_info:
                    result['additional_info'] = additional_info.get_text(strip=True)
            # Create a hash from title and url
            hash_value = hash_data(title, read_more_link)
            if hash_value not in existing_hashes:
                save_post_data(save_dir, result, hash_value)
                send_to_discord('bianlianl', 'result', result)

def crawl_3am(site_url, site_name):
    driver = settings()
    driver.get(site_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    save_dir = create_save_dir('json', site_name)
    
    existing_hashes = get_existing_post_hashes(save_dir)
    # 'post bad' 클래스의 모든 포스트 찾기
    posts = soup.find_all('div', class_='post bad')

    if not posts:
        print("No posts found. The structure of the webpage might have changed or the webpage is empty.")
        
    # 각 포스트에서 타이틀과 텍스트 정보를 추출하여 개별 JSON 파일로 저장
    for idx, post in enumerate(posts):
        title_block = post.find('div', class_='post-title-block')
        text_block = post.find('div', class_='post-body').find('div', class_='post-text')  # post-text 요소 찾기

        if title_block and text_block:
            title = title_block.get_text(strip=True)
            text = text_block.get_text(strip=True)
            
            # 데이터를 딕셔너리로 저장
            data = {
                'title': title,
                'text': text,
                'operator':'3am'
            }
            
            # Create a hash from title and url
            hash_value = hash_data(title, text)

            if hash_value not in existing_hashes:
                save_post_data(save_dir, data, hash_value)
                send_to_discord('3am', 'data', data)
    
    driver.quit()

#크롤링을 막아둬서인지, 데이터 수집이 안됨
def crawl_blackbasta(site_url, site_name):
    driver = settings()
    driver.get(site_url)
        
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    save_dir = create_save_dir('json', site_name)
    existing_hashes = get_existing_post_hashes(save_dir)
    
    cards = soup.select('.card')
    for idx, card in enumerate(cards):
        title = card.select_one('.title').text if card.select_one('.title') else 'No title'
        blog_name_link = card.select_one('.blog_name_link')
        blog_url = blog_name_link['href'] if blog_name_link else 'No URL'
        p_element = card.select_one('p[data-v-md-line="5"]').text if card.select_one('p[data-v-md-line="5"]') else 'No content'

        post_data = {
            'title': title,
            'url': blog_url,
            'content': p_element
        }

        hash_value = hash_data(title, blog_url)

        if hash_value not in existing_hashes:
            save_post_data(save_dir, post_data, hash_value)
    
    driver.quit()
    


#crawl_blacksuite('http://weg7sdx54bevnvulapqu6bpzwztryeflq3s23tegbmnhkbpqz637f2yd.onion/', 'blacksuite')
#crawl_bianlianl('http://bianlianlbc5an4kgnay3opdemgcryg2kpfcbgczopmm3dnbz3uaunad.onion', 'bianlianl')
crawl_3am('http://threeamkelxicjsaf2czjyz2lc4q3ngqkxhhlexyfcp2o6raw4rphyad.onion','3am')
