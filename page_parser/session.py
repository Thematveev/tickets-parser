from requests import Session
from bs4 import BeautifulSoup

class ParserSession(Session):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        # self.headers = {}
        # self.proxies = {}
        self.link = "http://ft.org.ua/ua/performance/konotopska-vidma"
        self.source = None

    def update_source(self):
        response = self.get(self.link)
        if not response.ok:
            raise Exception('Incorrect correct response from server!')

        self.source = BeautifulSoup(response.content, features='html.parser')

    def get_name(self):
        return self.source.find('div', {'class': 'performancepage_info'}).find('h1').text

    def get_dates(self):
        date_elements = self.source.find_all('div', {'class': 'performanceevents_item_info_date'})
        return list(map(lambda x: x.text, date_elements))
        


    