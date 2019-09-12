class Search:
    words = ""
    total = 0
    hits = []
    start = 0
    size = 0
    sort = None
    types = []  # list of types to include in search
    ages = []  # list of age ranges to include in the search
    aggregations = {}

    category = None

    def __init__(self, words="", types=[], ages=[], start=0, size=10, sort=None, category=None):
        self.words = words
        self.types = types
        self.ages = ages
        self.start = start
        self.size = size
        self.sort = sort
        self.category = category;

    def add_aggregation(self, field, value, count, is_selected):
        if field not in self.aggregations:
            self.aggregations[field] = {}
            self.aggregations[field][value] = {}
        elif value not in self.aggregations[field]:
            self.aggregations[field][value] = {}
        self.aggregations[field][value]={"hit_count": count, "is_selected": is_selected};


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
