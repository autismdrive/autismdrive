from app.models import Event, Location, Resource
from app.resources.Auth import login_optional
from app.resources.SearchEndpoint import SearchEndpoint


class SearchResourcesEndpoint(SearchEndpoint):
    @login_optional
    def post(self):
        return self.__post__([Resource.__tablename__, Location.__tablename__, Event.__tablename__])
