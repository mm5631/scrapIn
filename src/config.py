import os

# Chromedriver executable
CHROMEDRIVER_FILEPATH = os.path.join(os.path.dirname(__file__), '../chromedriver')

# Default URLS used by search methods
SEARCH_PEOPLE_DEFAULT_URL = 'https://www.linkedin.com/people/search/'
SEARCH_JOBS_DEFAULT_URL = 'https://www.linkedin.com/jobs/search/'

PARAMS = {
    'authenticate': {
        'username_field': 'session_key',  # name
        'password_field': 'session_password',  # name
        'signin_button': 'body > nav > section.sign-in-card.show > form > div.sign-in-form__footer > button'  # selector, or use class sign-in-form__submit-btn
    },

    'search': {
        'filters_button': 'search-filters-bar__all-filters.flex-shrink-zero.mr3.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view',
        'job_title_field': 'search-advanced-title',
        'apply_button': 'search-advanced-facets__button--apply.ml4.mr2.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view',
        'previous_button': 'artdeco-pagination__button--previous',
        'next_button': 'artdeco-pagination__button--next',

        'search_container': '.core-rail',
        'n_results_field': 'h3',
        'people': {},
        'jobs': {},
    },
}



