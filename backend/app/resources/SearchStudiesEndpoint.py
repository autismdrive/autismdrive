from app.models import Study
from app.resources.Auth import login_optional
from app.resources.SearchEndpoint import SearchEndpoint


class SearchStudiesEndpoint(SearchEndpoint):
    @login_optional
    def post(self):
        return self.__post__([Study.__tablename__])
