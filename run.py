from page_parser import ParserSession
from time import sleep
from bot import TelegramNotifier

if __name__ == "__main__":
    known_dates = set()

    parser = ParserSession()
    notifier = TelegramNotifier("6974518937:AAFPSL5wPoiMBhI5-XXHBNlZEVmzJd4rvik")
    print('WAITING FOR INITIAL SUBSCRIBERS (10S)')
    sleep(10)
    notifier.update_subscribers()

    print("STARTING SCANNER")
    while True:
        sleep(5) # timeout before reload
        parser.update_source()
        dates = parser.get_dates()
        for date in dates:
            if date not in known_dates:
                notifier.send_notifications(text=f"NEW TICKETS FOR DATE ==> {date}")
                known_dates.add(date)
        notifier.update_subscribers()



