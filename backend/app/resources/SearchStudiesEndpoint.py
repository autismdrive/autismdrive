from app.resources.SearchEndpoint import SearchEndpoint
from app.model.study import Study


class SearchStudiesEndpoint(SearchEndpoint):
    def post(self):
        return self.__post__([
            Study.__label__
        ])
