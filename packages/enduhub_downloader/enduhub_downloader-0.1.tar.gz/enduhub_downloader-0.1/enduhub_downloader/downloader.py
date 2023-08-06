
from os import path
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
import logging
import logging.config
#logging.config.fileConfig(log_file_path, defaults={'logfilename': 'enduhub_downloader/log/debug.log'})
logger = logging.getLogger('enduHuber')
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime
import requests
import urllib.parse
from enduhub_downloader.race_result import RaceResult

class Downloader:
    """
    A class used to represent runner result on Enduhub

    ....

    Attributes
    ----------
    runner :Runner
        Runner object
    to_date :str
        string date format yyyy-mm-dd    
    current_page :int
        page number where EnduhubDownloader is.
    parsed_pages :list
        list holding parsed pages by BeautifulSoup. 
    event_counter: dict
        holidng gropup informations about races. counter, sum_distance, best_resoults

    Methods
    -------
    
    """

    def __init__(self, runner, to_date_result=None):
        self.runner = runner
        self.current_page = 1
        
        logger.debug("Enduhuber created: {}".format(repr(self)))   
        self.parsed_pages = []   
        self.event_counter = {}
        self.to_date_result = to_date_result
    
  
        
    def download_results(self):
        """add rece results to the runner"""
        number_of_pages = self.pages_count()
        while(self.current_page <= number_of_pages):
            soup = self.parse_page()
            for row in soup.find_all('tr', class_='Zawody'):
                year_of_birth = row.find('td', class_='yob').get_text()
                time_result = row.find('td', class_='best').get_text()
                event =  row.find('td', class_='event').get_text()
                race_type = row.find('td', class_='sport').get_text()
                result_date =  row.find('td', class_='date').get_text()
                distance =  row.find('td', class_='distance').get_text()
                if year_of_birth[-2:] == str(self.runner.short_birth_year):
                    race_result = RaceResult(event, result_date, distance, race_type, time_result)
                    
                    if ((self.to_date_result and self.to_date_result >= race_result.result_date) or not self.to_date_result):
                        print(race_result)
                        self.runner.add_race_result(race_result)
            self.current_page += 1        
        logger.info('Founded events: {}'.format(len(self.runner.race_results)))   
    
   
    
    
    def __repr__(self):
        return 'EnduhubDownloader(Runner("{}","{}","{}"))'.format(self.runner.first_name, self.runner.last_name, self.runner.birth_year)
  
    def __str__(self):
        info = '{} {}, {}'.format(self.runner.first_name, self.runner.last_name, self.runner.birth_year)
        info +='\n'
        info +="Event counter:\n"
        info +=str(self.event_counter)
        return info

    def pages_count(self):
        """Counts how many pages have results."""
        soup = self.parse_page()
        butoom_li_number = len(soup.select('ul.pages li'))
        if butoom_li_number >= 4:
            pages = butoom_li_number - 2
        else:
            pages = 1
        logger.info("Pages founded: {}".format(pages))    
        return pages     

    def connect_with_enduhub(self):#
        """Connect to Enduhub and return response"""
        try:
            link="https://enduhub.com/pl/search/?name="+urllib.parse.quote(self.runner.full_name)+'&page='+str(self.current_page)
            req = requests.get(link)
        except Exception:
            logger.error('Cant connect to enduhub!!!!!!!')
            raise SystemExit(0)
        else:
            logger.info(f'Connected to Enduhub! Link: {link}')
            print(f'Connected to Enduhub! Link: {link}')
            return req
    
    def parse_page(self):
        """Return  BeautifulSoup object"""
        current_page = self.current_page
        try: 
            self.parsed_pages[current_page-1]
        except IndexError:
            logger.info(f"page cache not found: {current_page}")
            req = self.connect_with_enduhub()
            soup = BeautifulSoup(req.content, 'html.parser')
            self.parsed_pages.append(soup)
            return soup
        else:
            logger.info(f"page found in cache: {current_page}") 
            return self.parsed_pages[current_page-1]   

    @property
    def to_date_result(self):
        return self._to_date_result

    @to_date_result.setter
    def to_date_result(self, string_date):
        """Parse string and change to date"""
        string_date = datetime.strptime(string_date, '%Y-%m-%d')
        self._to_date_result = string_date.date()     
       