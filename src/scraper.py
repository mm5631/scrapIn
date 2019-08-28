
# Imports
import os
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import argparse

import logging
log = logging.Logger(__name__) # How to use?


config = {
    'username_field': 'session_key',
    'filters_button': 'search-filters-bar__all-filters.flex-shrink-zero.mr3.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view',
    'job_title_field': 'search-advanced-title',
    'apply_button': 'search-advanced-facets__button--apply.ml4.mr2.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view'
    'previous_button': 'artdeco-pagination__button--previous',
    'next_button': 'artdeco-pagination__button--next',
}

def argparser()
    pass

class Scraper:

    def __init__(self, credentials):

        self.fail = 0
        self._username = credentials[0]
        self._password = credentials[1]
        self.driver = webdriver.Chrome('./chromedriver')
        self.default_page = None
        self.urls = []

        self._authenticate()


    def _authenticate(self):
        self.driver.get('https://www.linkedin.com')
        time.sleep(2)
        username = self.driver.find_element_by_name('session_key')
        password = self.driver.find_element_by_name('session_password')

        username.send_keys(self._username)
        password.send_keys(self._password)

        sign_in = self.driver.find_element_by_class_name('sign-in-form__submit-btn')
        sign_in.click()


    def make_request(self, func, config):
        try:
            response = func(config)
            self.fail = 0
            return response
        except Exception as e:
            self.fail +=1
            if self.fail <= 5:
                time.sleep(2)
                self.make_request(func, config)
            else:
                print(f'Could not retrieve element, error:\n {e}')

    def find_element(self, by, element_id):
        params = {
            'class_name': self.driver.find_element_by_class_name,
            'id': self.driver.find_element_by_id
            'css_selector': self.driver.find_element_by_css_selector
                 }
        response = self.make_request(params[by], config[element_id])
        return response

    def _page_status(self):
        previous_button = None
        next_button - None
        return self

    def _page_looper(self):
        return self

    def search_job_function(self, job_function):
        filters_button = self.find_element(by='class_name', 'filters_button')) # needs wrapper
        filters_button.click()

        job_title_field = self.find_element(by='id', 'job_title_field')
        job_title_field.clear()
        job_title.send_keys(job_function)

        apply_button = self.find_element(by='class_name', 'apply_button')
        apply_button.click()





    def parse_urls(self):
        search_results = self.find_element(by='css_selector', '.core-rail').get_attribute('outerHTML')
        urls = BeautifulSoup(search_results, 'html.parser').find_all('a')
        return urls
#         target_profiles.append(h.get('href')) for h in urls if h.get('href') not in target_profiles





    def scrape_profiles(self, job_function):
        if self.default_page:
            self.driver.get(default)
        else:
            self.driver.get('https://www.linkedin.com/search/results/people/')

        # while self.page_status():
        #     self.search_job_functions(job_function)
        #     urls = self.parse_urls()
