import logging
import time
import os
import copy
from bs4 import BeautifulSoup
from selenium import webdriver
import getpass
from src import utils
from src.config import (
    CHROMEDRIVER_FILEPATH,
    PARAMS,
)
import inspect

logger = logging.getLogger('scraper')
logging.basicConfig(level=logging.INFO)


class Loader(object):
    def __init__(self, chromedriver_filepath=CHROMEDRIVER_FILEPATH, params=PARAMS):
        logger.info('Loading parameters..')
        self.authenticate_params = params['authenticate']
        self.search_params = params['search']
        self.chromedriver_filepath = chromedriver_filepath
        assert os.path.isfile(self.chromedriver_filepath), 'Please add the chromedriver file to repository root'


class Authenticator(Loader):
    def __init__(self, credentials=None):
        super().__init__()
        if not credentials:
            self._username = input('Enter username:')
            self._password = getpass.getpass('Enter password:')
        else:
            self._username = credentials[0]
            self._password = credentials[1]
        self.driver = None

    def login(self):
        logger.info('Submitting credentials and loging-in')
        self.driver = webdriver.Chrome(self.chromedriver_filepath)
        self.driver.get('https://www.linkedin.com')
        time.sleep(2)

        username_field = self.driver.find_element(by='name', value=self.authenticate_params['username_field'])
        password_field = self.driver.find_element(by='name', value=self.authenticate_params['password_field'])
        signin_button = self.driver.find_element(by='css selector', value=self.authenticate_params['signin_button'])

        username_field.send_keys(self._username)
        password_field.send_keys(self._password)
        signin_button.click()

        return self.driver
        # call destructor ?

    def __del__(self):
        pass


# def find_element(self, func, config):
#     try:
#         response = self.driver.find_element(config[0], config[1])
#         self.fail = 0
#         return response
#     except Exception as e:
#         self.fail += 1
#         if self.fail <= 2:
#             time.sleep(2)
#             self.make_request(func, config)
#             self.fail = 0
#         else:
#             logger.info(f'Could not retrieve element {config}, error:\n {e}')
class Scraper(object):
    def __init__(self, authenticator, timeout=2):
        assert isinstance(authenticator, Authenticator), 'Please instantiate an Authenticator object'
        self.driver = authenticator.login()
        self.results = []

    def _make_request(self, func):
        """Request handler"""
        pass

    # def _search(self):
    # handle text forms
    # handle selectable filters
    # handle next page

    def _grab_results(self, factory):
        time.sleep(1)
        results = self.driver.find_element(factory.main_params['search_container'][0],
                                           factory.main_params['search_container'][1]).get_attribute('outerHTML')
        soup = BeautifulSoup(results, 'html.parser').find_all('a')
        urls = list(set([a.get('href') for a in soup]))
        return urls

    def _search(self, factory):
        time.sleep(2)
        for param, config in factory.search_object.items():
            all_filters_button = self.driver.find_element(factory.main_params['all_filters_button'][0],
                                                          factory.main_params['all_filters_button'][1])
            all_filters_button.click()

            element = self.driver.find_element(config['selenium_location'][0], config['selenium_location'][1])
            element.send_keys(config['input_value'])

            apply_button = self.driver.find_element(factory.main_params['apply_button'][0],
                                                    factory.main_params['apply_button'][1])
            apply_button.click()
            self._grab_results(factory)
            # select or continue

    def search_people(self, search_keywords=None, location=None, industry=None, job_title=None, company=None,
                      default_url=None):
        factory = utils.Search(search_type='people', search_keywords=search_keywords, location=location,
                               industry=industry, job_title=job_title, company=company, default_url=default_url)
        logger.info(f'Passed following parameters: {factory.search_object}')
        self.driver.get(factory.default_url)
        # enter keywords
        # blah
        self._search(factory)
        urls = self._grab_results(factory)
        return urls

    # def search_jobs(self):
    #     kwargs = deepcopy(locals())
    #     search_object = utils.Search(search_type='jobs', **kwargs)
    #     return search_object

    def augment(self):
        pass

# class Scrapers:
#     def __init__(self, default_search=None):
#         self.fail = 0
#         self.default_search = default_search
#         self.urls = []
#
#     def make_request(self, func, config):
#         try:
#             response = func(config)
#             self.fail = 0
#             return response
#         except Exception as e:
#             self.fail += 1
#             if self.fail <= 2:
#                 time.sleep(2)
#                 self.make_request(func, config)
#                 self.fail = 0
#             else:
#                 logger.info(f'Could not retrieve element {config}, error:\n {e}')

# def search_job_function(self, job_function): # def search_job_function
#     print(f'[INFO] Scraping {job_function}')
#
#     assert current_page == None
#     filters_button = self._find_element(by='class_name', 'filters_button')
#     filters_button.click()
#
#     job_title_field = self._find_element(by='id', 'job_title_field')
#     job_title_field.clear()
#     job_title.send_keys(job_function)
#
#     apply_button = self._find_element(by='class_name', 'apply_button')
#     apply_button.click()
#
# def parse_urls(self):
#     search_results = self._find_element(by='css_selector', 'search_container').get_attribute('outerHTML')
#     soup = BeautifulSoup(search_results, 'html.parser').find_all('a')
#     urls = list(set([a.get('href') for a in soup]))
#     return urls

# def get_n_results(self):
#     try:
#         n_results = int(self._find_element(by='tag_name', 'n_results_field').text.split()[1].replace(',', ''))
#         return n_results
#     except FileNotFoundError as e:
#         print('No profiles meeting description')
#         return 0

# def next_page_exists(self):
#     self.next_button = self._find_element('class_name', 'next_button')
#     return next_button.is_enabled()
#
# def scrape_profile_urls(self, job_functions):
#
#     for job_function in job_functions:
#         if self.default_search:
#             self.driver.get(self.default_search)
#         else:
#             self.driver.get('https://www.linkedin.com/search/results/people/')
#
#         self.search_job_function(job_function)
#
#         time.sleep(2)
#
#         n_results = self.get_n_results()
#
#         if n_results >= 1:
#             current_urls = self.parse_urls()
#             self.urls.append(current_urls)
#             while self.next_page_exists():
#                 current_urls = self.parse_urls()
#                 self.urls.append(current_urls)
#                 self.next_button.click()
#                 time.sleep(2)
#         else:
#             continue
#
# def scrape_profile_info(self):
#     return self

# Check if results

# Scrape results

# Check if next page

# Continue scraping
