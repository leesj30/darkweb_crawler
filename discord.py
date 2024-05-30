import requests

DISCORD_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1245288715761356890/weaEDKbF5Q1vfF7rTaxr52NzKDVBMqBwctvnimZj6ilLL9JJbUbacI8oH4jla1P426-T'

def send_discord_notification(post_data):
    content = f"New post found:\nTitle: {post_data['title']}\nURL: {post_data['url']}\nDescription: {post_data.get('description', 'No description')}"
    data = {
        "content": content
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {response.status_code}")