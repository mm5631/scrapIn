import os
import time
import argparse
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

import logging
log = logging.Logger(__name__)  # How to use?


def argparser():
    pass


config = {
    # Login page
    'username_field': 'session_key',
    'password_field': 'session_password',
    'signin_button': 'sign-in-form__submit-btn',

    # People search page
    'filters_button': 'search-filters-bar__all-filters.flex-shrink-zero.mr3.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view',
    'job_title_field': 'search-advanced-title',
    'apply_button': 'search-advanced-facets__button--apply.ml4.mr2.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view'
    'previous_button': 'artdeco-pagination__button--previous',
    'next_button': 'artdeco-pagination__button--next',
    'search_container': '.core-rail'
    'n_results_field': 'h3'
}


class Scraper:

    def __init__(self, credentials, default_search=None):

        self.fail = 0
        self._username = credentials[0]
        self._password = credentials[1]
        self.driver = webdriver.Chrome('./chromedriver')
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
            else:
                print(f'Could not retrieve element {config}, error:\n {e}')

    def _find_element(self, by, label):
        params = {
            'class_name': self.driver.find_element_by_class_name,
            'id': self.driver.find_element_by_id
            'css_selector': self.driver.find_element_by_css_selector,
            'name': self.driver.find_element_by_name,
            'tag_name': self.driver.find_element_by_tag_name
        }
        response = self.make_request(params[by], config[label])
        return response

    def _authenticate(self):
        self.driver.get('https://www.linkedin.com')
        time.sleep(2)
        username = self._find_element(by='name', 'username_field')
        password = self._find_element(by='name', 'password_field')

        username.send_keys(self._username)
        password.send_keys(self._password)

        signin = self._find_element(by='class_name', 'signin_button')
        signin.click()

    def search_job_function(self, job_function):
        print(f'[INFO] Scraping {job_function}')

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
            n_results = np.int(self._find_element(by='tag_name', 'n_results_field').text.split()[1].replace(',', ''))
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
