import os

# Chromedriver executable
CHROMEDRIVER_FILEPATH = os.path.join(os.path.dirname(__file__), '../chromedriver')

# Default URLS used for search methods
SEARCH_PEOPLE_DEFAULT_URL = 'https://www.linkedin.com/people/search/'
SEARCH_JOBS_DEFAULT_URL = 'https://www.linkedin.com/jobs/search/'


PARAMS = {
    # Login page
    'authenticate': {
        'username_field': ['name', 'session_key'],  # name
        'password_field': ['name', 'session_password'],  # name
        'signin_button': ['xpath', "//button[contains(text(), 'Sign in')]"]
    },

    # Search page
    'search': {
        # 'default_url': {
        #     'search.people': SEARCH_PEOPLE_DEFAULT_URL,
        #     'search.jobs': SEARCH_JOBS_DEFAULT_URL
        # },
        'search_field': ['xpath', "//input[contains(@class, 'search-global-typeahead')]"],
        'all_filters_button': ['xpath', "//button[@data-control-name='all_filters']"],
        'apply_button': ['xpath', "//button[@data-control-name='all_filters_apply']"],
        'search_container': ['css selector', '.core-rail'],
        'core_results': ['xpath', "//div[contains(@class, 'search-result__info')]"],
        'profile_data': ['xpath', "//span[contains(@class, 'actor-name')]"],
        'next_button': ['xpath', "//button[@aria-label='Next']"]
    },

    # People-specific search page
    'search.people': {
        'default_url': SEARCH_PEOPLE_DEFAULT_URL,
        'location': ['xpath', "//input[contains(@placeholder, 'country')]"],
        'industry': ['xpath', "//input[contains(@placeholder, 'industry')]"],
        'current_company': ['xpath', "//input[contains(@placeholder, 'company')]"],

        'job_title': ['xpath', "//input[@id='search-advanced-title']"],  # text
    },
    # Job-specific search page
    'search.jobs': {
        'default_url': SEARCH_JOBS_DEFAULT_URL
    },
}



