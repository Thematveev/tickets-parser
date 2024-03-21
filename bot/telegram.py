import requests
from logs import logger

class TelegramNotifier:
    def __init__(self, token) -> None:
        self.token = token
        self.chat_ids = []

        logger.info('Telegram notifier initialized')

    def send_notifications(self, text="Newtickets"):
        logger.info(f'Start sending notifications to ids -> {self.chat_ids}')

        for chat_id in self.chat_ids:
            requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={text}")
            
            logger.info(f'Notification with text "{text}" send to chat -> {chat_id}')
        
        logger.info('End sending notifications')

    def update_subscribers(self):
        logger.info('Try to update subscribers')

        response = requests.get(f"https://api.telegram.org/bot{self.token}/getUpdates").json()
        for update in response['result']:
            chat_id = update.get('message', {}).get('chat', {}).get('id')
            text = update.get('message', {}).get('text', "").strip().lower()
            if text == 'ok' and chat_id and chat_id not in self.chat_ids:
                self.chat_ids.append(chat_id)
                # self.send_notifications(text=f'NEW SUBSCRIBER -> {chat_id}')
                logger.info(f'NEW SUBSCRIBER -> {chat_id}')
        logger.info(f'Subscribers updated. List -> {self.chat_ids}')

    def send_file(self, path):
        with open(path, "rb") as file:
            data = {"document":file}
            title = file.name
            for chat_id in self.chat_ids:
                r = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendDocument",
                    data={"chat_id":chat_id, "caption":title},
                    files=data
                    )
        


if __name__ == "__main__":
    t = TelegramNotifier("6974518937:AAFPSL5wPoiMBhI5-XXHBNlZEVmzJd4rvik")
    # while True:
    #     t.update_subscribers()
    #     sleep(5)