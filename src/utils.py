from src.config import (
    SEARCH_PEOPLE_DEFAULT_URL,
    SEARCH_JOBS_DEFAULT_URL,
    PARAMS,
)


class Search:
    def __init__(self, search_type, **kwargs):
        self._search_type = f'search.{search_type}'
        self.search_keyword = None
        self.default_urls = {'search.people': SEARCH_PEOPLE_DEFAULT_URL, 'search.jobs': SEARCH_JOBS_DEFAULT_URL}
        self.filter_settings = {
            'people': ['search_keywords',
                       'locations',
                       'industries',
                       'schools',
                       'job_title'],
            'jobs': None,
        }
        self.base_params = PARAMS['search']
        self.default_url = self.default_url[self._search_type]
        self.params = PARAMS[self._search_type]

    def generate_search_object(self, **kwargs):
        pass


class People(Search):
    def __init__(self, search_keywords, location, industry, job_title, company, default_url=None):
        super().__init__()
        self.filters = self.filter_settings[self.__class__.__name__]
        if not default_url:
            self.default_url = self.default_urls[self.__class__.__name__]
        else:
            assert isinstance(default_url, str), 'Please pass in URL as a string'
            self.default_url = default_url


class Jobs(Search):
    def __init__(self):
        super().__init__()
