import logging
import time
import os
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
from src import utils
from src.config import (
    CHROMEDRIVER_FILEPATH,
    PARAMS,
)

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
        logger.info('Loading parameters..\n')
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
        logger.info('Submitting credentials and logging-in\n')
        self.driver = webdriver.Chrome(self.chromedriver_filepath)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com')
        time.sleep(2)

        username_field = self.driver.find_element(self.authenticate_params['username_field'][0],
                                                  self.authenticate_params['username_field'][1])
        password_field = self.driver.find_element(self.authenticate_params['password_field'][0],
                                                  self.authenticate_params['password_field'][1])
        signin_button = self.driver.find_element(self.authenticate_params['signin_button'][0],
                                                 self.authenticate_params['signin_button'][1])

        username_field.send_keys(self._username)
        password_field.send_keys(self._password)
        signin_button.click()

        return self.driver


class Scraper(object):
    def __init__(self, authenticator):
        assert isinstance(authenticator, Authenticator), 'Please instantiate an Authenticator object'
        self.driver = authenticator.login()
        self.results = []

    @element_handler
    def find_element(self, by, path):
        return self.driver.find_element(by, path)

    @staticmethod
    def _absolute_filter(element, value):
        element.clear()
        element.send_keys(value)

    def _fuzzy_filter(self, element, value):
        actions = webdriver.ActionChains(self.driver)
        actions.send_keys_to_element(element, value).pause(1.5).send_keys([Keys.DOWN, Keys.ENTER])
        actions.perform()

    def apply_filters(self, factory):
        all_filters_button = self.find_element(factory.params['all_filters_button'][0],
                                               factory.params['all_filters_button'][1])
        all_filters_button.click()
        for param, config in factory.search_object.items():
            time.sleep(0.5)
            element = self.find_element(config[0], config[1])
            if param in ['job_title']:
                self._absolute_filter(element, config[2])
            else:
                self._fuzzy_filter(element, config[2])

        apply_button = self.find_element(factory.params['apply_button'][0], factory.params['apply_button'][1])
        apply_button.click()

    @staticmethod
    def _grab_urls(search_container, factory):
        urls = []
        url_container = search_container.find_elements(factory.params['url_container'][0],
                                                       factory.params['url_container'][1])
        for url in url_container:
            href = url.get_property('href')
            if '/in/' in href:
                urls.append(href)
            else:
                urls.append('#')
        return urls

    @staticmethod
    def _grab_names(search_container, factory):
        name_container = search_container.find_elements(factory.params['name_container'][0],
                                                        factory.params['name_container'][1])
        names = [name.text for name in name_container]
        return names

    @staticmethod
    def _grab_job_location(search_container, factory):
        jobs_location_container = search_container.find_elements(factory.params['job_location_container'][0],
                                                                 factory.params['job_location_container'][1])
        job_locations = [i.text for i in jobs_location_container]
        job_locations = np.reshape(job_locations, (np.int(len(jobs_location_container) / 2), 2))
        return job_locations

    def _parse_results(self, factory):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        search_container = self.find_element(factory.params['search_container'][0],
                                             factory.params['search_container'][1])
        urls = self._grab_urls(search_container, factory)
        names = self._grab_names(search_container, factory)
        job_location = self._grab_job_location(search_container, factory)
        current_df = pd.DataFrame(columns=['URL', 'Name', 'Title', 'Location'])
        current_df['URL'] = urls
        current_df['Name'] = names
        current_df[['Title', 'Location']] = job_location
        return current_df

    def grab_results(self, factory):
        time.sleep(1)
        df = pd.DataFrame(columns=['URL', 'Name', 'Title', 'Location'])

        core_rail = self.find_element(factory.params['core_rail'][0],
                                      factory.params['core_rail'][1])

        if core_rail.text.startswith('No results'):
            logger.info(f'No results for search {factory.search_object}\n')
            pass
        else:
            n_profiles = core_rail.text.split('\n')[0].replace('Showing', 'Query returned')
            logger.info(f"{n_profiles}\n")
            df = pd.concat([df, self._parse_results(factory=factory)])
            is_next_button = self.driver.find_elements(factory.params['next_button'][0],
                                                       factory.params['next_button'][1])
            if len(is_next_button) == 0:
                logger.info('Reached last searcheable page..')
                pass
            else:
                next_button = is_next_button[0]
                while next_button.is_enabled():
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    next_button.click()
                    time.sleep(1.5)
                    df = pd.concat([df, self._parse_results(factory=factory)])
                df = pd.concat([df, self._parse_results(factory=factory)])

            return df

    def _fetch_profiles(self, factory):
        time.sleep(2)
        self.apply_filters(factory)
        df = self.grab_results(factory)
        logger.info('Retrieved profiles')
        return df

    def search_people(self, search_keywords=None, location=None, industry=None, job_title=None, current_company=None,
                      default_url=None):
        factory = utils.Search(search_type='people', search_keywords=search_keywords, location=location,
                               industry=industry, job_title=job_title, current_company=current_company,
                               default_url=default_url)
        logger.info(f'Passed following parameters: {factory.search_object}\n')
        self.driver.get(factory.default_url)
        df = self._fetch_profiles(factory)
        return df
