from page_parser import ParserSession
from time import sleep
from bot import TelegramNotifier
import config

from logs import logger

parser = ParserSession()
notifier = TelegramNotifier(config.TG_TOKEN)

def main():
    known_dates = set()

    
    logger.info('WAITING FOR INITIAL SUBSCRIBERS (10S)')
    sleep(10)
    notifier.update_subscribers()


    logger.info('Start scannig proccess')
    while True:
        sleep(config.TIMEOUT_BETWEEN_CHECKS) # timeout before reload
        try:
            parser.update_source()
        except Exception as e:
            logger.error('Source code update coused exeption')
            logger.error(e)
            continue

        dates = parser.get_dates()
        for date in dates:
            if date not in known_dates:
                try:
                    notifier.send_notifications(text=f"NEW TICKETS FOR DATE ==> {date}")
                except Exception as e:
                    logger.error('Error while sending notification')
                    logger.error(e)
                known_dates.add(date)

        try:
            notifier.update_subscribers()
        except Exception as e:
            logger.error('Error while updating subscribers')
            logger.error(e)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        notifier.send_file('/Users/matveev/Desktop/projects/vidma-parser/logs/app_logs.log')



