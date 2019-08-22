from app.resources.SearchEndpoint import SearchEndpoint
from app.model.resource import Resource
from app.model.event import Event
from app.model.location import Location


class SearchResourcesEndpoint(SearchEndpoint):
    def post(self):
        return self._post([
            Resource.__label__,
            Location.__label__,
            Event.__label__
        ])
