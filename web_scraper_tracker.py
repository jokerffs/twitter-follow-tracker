import requests
from bs4 import BeautifulSoup
import time

# Telegram Bot Notification Function
def send_telegram_message(chat_id, message):
    bot_token = "7788051366:AAEGYsJY1JdF8-unUxSGslNll1G3BOOgOds"
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.get(telegram_url, params=params)
    return response

# Target Twitter username
username = "Gautamguptagg"
url = f"https://twitter.com/{username}/following"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Previous followings
prev_followings = set()

def fetch_followings():
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Scrape users from profile (limited and not always reliable)
        users = set()
        for tag in soup.find_all("a"):
            href = tag.get("href", "")
            if href.startswith("/") and href.count("/") == 1 and href.strip("/") != username:
                users.add(href.strip("/"))
        return users
    except Exception as e:
        print(f"[Error] {e}")
        return set()

# Start tracking
print(f"Tracking @{username}'s follows (web scraping)...\n")
prev_followings = fetch_followings()

while True:
    time.sleep(60)
    current_followings = fetch_followings()

    new_follows = current_followings - prev_followings
    if new_follows:
        for user in new_follows:
            follow_message = f"🟢 @{username} followed: @{user}"
            print(follow_message)  # Print it in the terminal
            send_telegram_message('977248982', follow_message)  # Send to Telegram
    else:
        print("No new follows...")

    prev_followings = current_followings
