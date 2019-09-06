import time

from bs4 import BeautifulSoup
from selenium import webdriver
# from logger import get_logger

from src.config import (CHROMEDRIVER_FILEPATH, PARAMS)

class Loader:
    def __init__(self, chromedriver_filepath=CHROMEDRIVER_FILEPATH, params=PARAMS):
        self.driver = self.driver = webdriver.Chrome(chromedriver_filepath)
        self.authenticate_params = params['authenticate']
        self.search_params = params['search']


class Authenticator(Loader):
    def  __init__(self, credentials=None):
        if not credentials:
            self._username = input('Enter username:')
            self._password = input('Enter password:')
        else:
            self._username = credentials[0]
            self._password = credentials[1]


    def authenticate(self):
        self.driver.get('https://www.linkedin.com')
        time.sleep(2)
        username_field = self.driver.find_element(by='name', value=self.authenticate_params['username_field'])
        password_field = self.driver.find_element(by='name', value=self.authenticate_params['password_field'])

        username_field.send_keys(self._username)
        password_field.send_keys(self._password)

        signin = self.driver.find_element(by='class_name', value=self.search_params['signin_button'])
        signin.click()



class Scraper:

    def __init__(self, default_search=None):

        self.fail = 0
        self._username = credentials[0]
        self._password = credentials[1]
        self.driver = webdriver.Chrome(CHROMEDRIVER_FILEPATH)
        self.default_search = default_search
        self.urls = []

        self._authenticate()

    def make_request(self, func, config):
        try:
            response = func(config)
            self.fail = 0
            return response
        except Exception as e:
            self.fail += 1
            if self.fail <= 2:
                time.sleep(2)
                self.make_request(func, config)
                self.fail = 0
            else:
                print(f'Could not retrieve element {config}, error:\n {e}')

    def search_job_function(self, job_function): # def search_job_function
        print(f'[INFO] Scraping {job_function}')

        assert current_page == None

        filters_button = self._find_element(by='class_name', 'filters_button')
        filters_button.click()

        job_title_field = self._find_element(by='id', 'job_title_field')
        job_title_field.clear()
        job_title.send_keys(job_function)

        apply_button = self._find_element(by='class_name', 'apply_button')
        apply_button.click()

    def parse_urls(self):
        search_results = self._find_element(by='css_selector', 'search_container').get_attribute('outerHTML')
        soup = BeautifulSoup(search_results, 'html.parser').find_all('a')
        urls = list(set([a.get('href') for a in soup]))
        return urls

    def get_n_results(self):
        try:
            n_results = int(self._find_element(by='tag_name', 'n_results_field').text.split()[1].replace(',', ''))
            return n_results
        except FileNotFoundError as e:
            print('No profiles meeting description')
            return 0

    def next_page_exists(self):
        self.next_button = self._find_element('class_name', 'next_button')
        return next_button.is_enabled()

    def scrape_profile_urls(self, job_functions):

        for job_function in job_functions:
            if self.default_search:
                self.driver.get(self.default_search)
            else:
                self.driver.get('https://www.linkedin.com/search/results/people/')

            self.search_job_function(job_function)

            time.sleep(2)

            n_results = self.get_n_results()

            if n_results >= 1:
                current_urls = self.parse_urls()
                self.urls.append(current_urls)
                while self.next_page_exists():
                    current_urls = self.parse_urls()
                    self.urls.append(current_urls)
                    self.next_button.click()
                    time.sleep(2)
            else:
                continue

    def scrape_profile_info(self):
        return self

        # Check if results

        # Scrape results

        # Check if next page

        # Continue scraping
