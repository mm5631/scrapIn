from src.config import (
    SEARCH_PEOPLE_DEFAULT_URL,
    SEARCH_JOBS_DEFAULT_URL
)

class Search:
    def __init__(self):
        self.search_keyword = None
        self.default_urls = {'Jobs': SEARCH_JOBS_DEFAULT_URL, 'People': SEARCH_PEOPLE_DEFAULT_URL}



class Jobs(Search):
    def __init__(self, location: str, job_type: str, industry: str, job_title: str, loop_over: str = None,
                 default_url: str = None):
        super().__init__()

        self.params = {'keyword,'location', 'job_type', 'job_title', 'industry'}
        self.generate_search_object()

    def generate_search_object(self, params):
        return self


class People(Search):
    def __init__(self, search_keywords, location, industry, job_title, company, default_url=None):
        super().__init__()

        self.search_keywords = search_keywords
        self.locations = location
        self.industry = industry
        self.job_title = job_title
        self.company = company

        if not default_url:
            self.default_url = self.default_urls[self.__class__.__name__]
        else:
            assert isinstance(default_url, str), 'Please pass in URL as a string'
            self.default_url = default_url



class Companies(object):
    def __init__(self, **params):
        pass
