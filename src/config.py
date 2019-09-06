import os

CHROMEDRIVER_FILEPATH = os.path.join(os.path.dirname(__file__), '../chromedriver')
assert os.path.isfile(CHROMEDRIVER_FILEPATH), 'Please download chromedriver'

PARAMS = {
    'authenticate': {
        'username_field': 'session_key',
        'password_field': 'session_password',
        'signin_button': 'sign-in-form__submit-btn'
    },

    'search': {
        'filters_button': 'search-filters-bar__all-filters.flex-shrink-zero.mr3.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view',
        'job_title_field': 'search-advanced-title',
        'apply_button': 'search-advanced-facets__button--apply.ml4.mr2.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view',
        'previous_button': 'artdeco-pagination__button--previous',
        'next_button': 'artdeco-pagination__button--next',
        'search_container': '.core-rail',
        'n_results_field': 'h3'
    },
}



