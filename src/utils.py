from src.config import (
    SEARCH_PEOPLE_DEFAULT_URL,
    SEARCH_JOBS_DEFAULT_URL,
    PARAMS,
)


class Search(object):

    def __init__(self, search_type, **kwargs):
        self._search_type = f'search.{search_type}'

        self.default_url = PARAMS[self._search_type]['default_url']

        self.params = PARAMS['search']
        self.params.update(PARAMS[self._search_type])   # print(self.params)
        self.default_url = self.params['default_url']
        # self.secondary_params = PARAMS[self._search_type]
        self.selected_params = kwargs

        self._generate_search_object()

    def _generate_search_object(self):
        self.search_object = {
            k: self.params[k] + [v] for k, v in self.selected_params.items() if v}
