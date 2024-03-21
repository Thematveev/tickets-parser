from requests import Session
from bs4 import BeautifulSoup

from logs import logger

class ParserSession(Session):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        # self.headers = {}
        # self.proxies = {}
        self.link = "http://ft.org.ua/ua/performance/konotopska-vidma"
        self.source = None

        logger.info(f'Parser initialized with link -> {self.link}')

    def update_source(self):
        logger.info('Start updating source')

        response = self.get(self.link)
        if not response.ok:
            raise Exception('Incorrect response from server!')
        
        logger.info('Source updated')

        self.source = BeautifulSoup(response.content, features='html.parser')

    def get_name(self):
        logger.info('Trying extract perfomance name')

        name = self.source.find('div', {'class': 'performancepage_info'}).find('h1').text

        logger.info(f'Perfomance name -> {name}')
        return name


    def get_dates(self):
        logger.info('Trying extract perfomance dates')
        date_elements = self.source.find_all('div', {'class': 'performanceevents_item_info_date'})
        dates = list(map(lambda x: x.text, date_elements))
        logger.info(f'Extracted dates -> {dates}')
        return dates
        


    