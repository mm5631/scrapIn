from src.config import (
    SEARCH_PEOPLE_DEFAULT_URL,
    SEARCH_JOBS_DEFAULT_URL,
    PARAMS,
)


class Search(object):

    def __init__(self, search_type, **kwargs):
        self._search_type = f'search.{search_type}'

        self.default_url = PARAMS[self._search_type]['default_url']

        self.main_params = PARAMS['search']
        self.secondary_params = PARAMS[self._search_type]
        self.selected_params = kwargs

        self._generate_search_object()

    def _generate_search_object(self):
        self.search_object = {
            k: {'selenium_location': self.secondary_params[k],
                'input_value': v} for k, v in self.selected_params.items() if v}
