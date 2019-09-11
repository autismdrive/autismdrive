from app.resources.SearchEndpoint import SearchEndpoint
from app.model.resource import Resource
from app.model.event import Event
from app.model.location import Location


class SearchResourcesEndpoint(SearchEndpoint):
    def post(self):
        return self.__post__([
            Resource.__tablename__,
            Location.__tablename__,
            Event.__tablename__
        ])
