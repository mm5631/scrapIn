import os

# Chromedriver executable
CHROMEDRIVER_FILEPATH = os.path.join(os.path.dirname(__file__), '../chromedriver')

# Default URLS used for search methods
SEARCH_PEOPLE_DEFAULT_URL = 'https://www.linkedin.com/people/search/'
SEARCH_JOBS_DEFAULT_URL = 'https://www.linkedin.com/jobs/search/'


PARAMS = {
    # Login page
    'authenticate': {
        'sign_in_card': ['xpath', "//section[@class='sign-in-card']"],
        'username_field': ['name', 'session_key'],
        'password_field': ['name', 'session_password'],
        'signin_button': ['xpath', "//button[contains(text(), 'Sign in')]"]
    },

    # Search page
    'search': {
        'search_field': ['xpath', "//input[contains(@class, 'search-global-typeahead')]"],
        'all_filters_button': ['xpath', "//button[@data-control-name='all_filters']"],
        'apply_button': ['xpath', "//button[@data-control-name='all_filters_apply']"],

        'core_rail': ['css selector', '.core-rail'],
        'search_container': ['xpath', "//ul[contains(@class, 'search-result')]"],
        'url_container': ['xpath', "//div[contains(@class, 'info')]/a[@href]"],
        'name_container': ['xpath', "li//span[contains(@class, 'actor-name')]"],
        'job_location_container': ['xpath', "//p[contains(@class, 'subline')]/span[@dir]"],

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



