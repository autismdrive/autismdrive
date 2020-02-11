from app.resources.SearchEndpoint import SearchEndpoint
from app.resources.Auth import login_optional
from app.model.study import Study


class SearchStudiesEndpoint(SearchEndpoint):
    @login_optional
    def post(self):
        return self.__post__([
            Study.__tablename__
        ])
