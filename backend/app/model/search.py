class Search:
    words = ""
    filters = []
    total = 0
    hits = []
    facets = []
    start = 0
    size = 0
    sort = None
    category = None

    def __init__(self, words="", filters=[], start=0, size=10, sort=None, category=None):
        self.words = words
        self.filters = filters
        self.start = start
        self.size = size
        self.sort = sort
        self.category = category;

    def jsonFilters(self):
        jfilter = {}
        for f in self.filters:
            jfilter[f.field] = f.value
        return jfilter




class Facet:
    field = ""
    facetCounts = []

    def __init__(self, field):
        self.field = field


class FacetCount:
    def __init__(self, category, hit_count, is_selected):
        self.category = category
        self.hit_count = hit_count
        self.is_selected = is_selected


class Filter:
    field = ""
    value = ""

    def __init__(self, field, value):
        self.field = field
        self.value = value


class Sort:
    field = ""
    latitude = None
    longitude = None
    order = "desc"
    unit = "mi"

    def __init__(self, field, latitude, longitude, order, unit):
        self.field = field
        self.latitude = latitude
        self.longitude = longitude
        self.order = order
        self.unit = unit

    def translate(self):
        if None not in (self.latitude, self.latitude):
            return {
                '_geo_distance': {
                    self.field: {
                        'lat': self.latitude,
                        'lon': self.longitude
                    },
                    'order': self.order,
                    'unit': self.unit
                }
            }
        else:
            return {self.field: {'order': self.order}}


class Hit:

    def __init__(self, result_id, content, description, title, doc_type, label, last_updated, highlights, latitude, longitude):
        self.id = result_id
        self.content = content
        self.description = description
        self.title = title
        self.type = doc_type
        self.label = label
        self.last_updated = last_updated
        self.highlights = highlights
        self.latitude = latitude
        self.longitude = longitude
