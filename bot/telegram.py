import requests
from time import sleep

class TelegramNotifier:
    def __init__(self, token) -> None:
        self.token = token
        self.chat_ids = []

    def send_notifications(self, text="Newtickets"):
        for chat_id in self.chat_ids:
            requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={text}")

    def update_subscribers(self):
        response = requests.get(f"https://api.telegram.org/bot{self.token}/getUpdates").json()
        for update in response['result']:
            chat_id = update.get('message', {}).get('chat', {}).get('id')
            text = update.get('message', {}).get('text', "").strip().lower()
            if text == 'start' and chat_id and chat_id not in self.chat_ids:
                self.chat_ids.append(chat_id)
                self.send_notifications(text=f'NEW SUBSCRIBER -> {chat_id}')
        print('Subscribers updated', self.chat_ids)
        


if __name__ == "__main__":
    t = TelegramNotifier("6974518937:AAFPSL5wPoiMBhI5-XXHBNlZEVmzJd4rvik")
    while True:
        t.update_subscribers()
        sleep(5)