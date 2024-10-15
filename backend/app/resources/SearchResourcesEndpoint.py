from app.resources.SearchEndpoint import SearchEndpoint
from app.resources.Auth import login_optional
from app.models import Resource, Location, Event
from app.models import Location


class SearchResourcesEndpoint(SearchEndpoint):
    @login_optional
    def post(self):
        return self.__post__([Resource.__tablename__, Location.__tablename__, Event.__tablename__])
