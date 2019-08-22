from app.resources.SearchEndpoint import SearchEndpoint
from app.model.study import Study


class SearchStudiesEndpoint(SearchEndpoint):
    def post(self):
        return self._post([
            Study.__label__
        ])
