import requests
import json

DISCORD_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1245288715761356890/weaEDKbF5Q1vfF7rTaxr52NzKDVBMqBwctvnimZj6ilLL9JJbUbacI8oH4jla1P426-T'

def send_to_discord(operator, data_type, data):
    """
    디스코드 웹훅으로 데이터를 전송하는 범용적인 메소드.
    
    :param operator: 운영자 정보
    :param data_type: 데이터 형식 ('post_data', 'result', 'data')
    :param data: 전송할 데이터 딕셔너리
    """
    
    # 전송할 데이터의 공통 형식을 만듭니다.
    payload = {
        'username': 'Leak Notification',  # 디스코드에서 표시될 봇의 이름
        'embeds': []
    }
    
    # 데이터 형식에 따라 적절한 형식으로 변환
    if data_type == 'post_data':
        embed = {
            'title': f"Victim Company: {data.get('title', 'N/A')} - Operator: {operator}",
            'description': data.get('text', 'N/A'),
            'url': ', '.join(data.get('links', ['N/A'])) if data.get('links') else 'N/A'  # 링크들을 콤마로 구분하여 문자열로 변환
        }
    elif data_type == 'result':
        embed = {
            'title': f"Victim Company: {data.get('title', 'N/A')} - Operator: {operator}",
            'description': data.get('description', 'N/A'),
            'url': data.get('read_more_url', 'N/A')
        }
    elif data_type == 'data':
        embed = {
            'title': f"Victim Company: {data.get('title', 'N/A')} - Operator: {operator}",
            'description': data.get('text', 'N/A')
        }
    elif data_type == 'detailed_data':
        embed = {
            'title': f"Victim Company: {data.get('title', 'N/A')} - Operator: {operator}",
            'description': (
                f"Date: {data.get('datetime', 'N/A')}\n"
                f"Summary: {data.get('entry_summary', 'N/A')}\n"
                f"Leaked Data Size: {data.get('leaked_data_size', 'N/A')}\n"
            )
        }
    else:
        raise ValueError("Invalid data_type provided. Choose from 'post_data', 'result', or 'data'.")
    
    # URL 검증: 유효하지 않은 URL일 경우 URL 필드 제거
    if embed.get('url') == 'N/A' or (embed.get('url') and not embed.get('url').startswith('http')):
        embed.pop('url', None)
    
    payload['embeds'].append(embed)
    
    # 디스코드 웹훅으로 POST 요청을 보냅니다.
    response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    
    # 요청 결과를 반환합니다.
    if response.status_code == 204:
        print("메시지가 성공적으로 전송되었습니다.")
    else:
        print(f"메시지 전송 실패: {response.status_code}, {response.text}")


