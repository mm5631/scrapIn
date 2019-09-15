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


def element_handler(func):
    def wrapper(*args, **kwargs):
        n_failures = 0
        element = None
        while (n_failures <= 2) & (element is None):
            try:
                element = func(*args, **kwargs)
            except Exception as e:
                logger.info(f'Failed to grab element, error {e}')
                time.sleep(2)
                n_failures += 1
        return element

    return wrapper


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

        self.driver.maximize_window()
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


class Scraper(object):
    def __init__(self, authenticator):
        assert isinstance(authenticator, Authenticator), 'Please instantiate an Authenticator object'
        self.driver = authenticator.login()
        self.results = []

    @element_handler
    def find_element(self, by, path):
        return self.driver.find_element(by, path)

    def apply_filters(self, factory):
        all_filters_button = self.find_element(factory.params['all_filters_button'][0],
                                               factory.params['all_filters_button'][1])
        all_filters_button.click()

        for param, config in factory.search_object.items():
            element = self.find_element(config[0], config[1])
            element.send_keys(config[2])  # do something

        apply_button = self.find_element(factory.params['apply_button'][0], factory.params['apply_button'][1])
        apply_button.click()

    @staticmethod
    def _parse_results(results, urls):
        soup = BeautifulSoup(results.get_attribute('outerHTML'), 'html.parser').find_all('a')
        urls_ = list(set([a.get('href') for a in soup]))
        urls.extend(urls_)

    def grab_results(self, factory):
        time.sleep(1)
        urls = []
        results = self.find_element(factory.params['search_container'][0],
                                    factory.params['search_container'][1])

        if results.text.startswith('No results'):
            logger.info(f'No results for search {factory.search_object}')
            pass
        else:
            self._parse_results(results, urls)
            is_next_button = self.driver.find_elements(factory.params['next_button'][0],
                                                       factory.params['next_button'][1])
            if len(is_next_button) == 0:
                pass
            else:
                next_button = is_next_button[0]
                while next_button.is_enabled():
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # self.driver.implicitly_wait(0.5)
                    next_button.click()
                    time.sleep(1.5)
                    self._parse_results(results, urls)
                self._parse_results(results, urls)

            urls = list(filter(lambda x: '/in/' in x, urls))
            return urls

    def _fetch_urls(self, factory):
        time.sleep(2)
        self.apply_filters(factory)
        urls = self.grab_results(factory)
        logger.info('Retrieved profile urls')
        return urls

    def query_results(self, urls):
        pass

    def search_people(self, search_keywords=None, location=None, industry=None, job_title=None, company=None,
                      default_url=None):
        factory = utils.Search(search_type='people', search_keywords=search_keywords, location=location,
                               industry=industry, job_title=job_title, company=company, default_url=default_url)
        logger.info(f'Passed following parameters: {factory.search_object}')
        self.driver.get(factory.default_url)
        urls = self._fetch_urls(factory)
        return urls
