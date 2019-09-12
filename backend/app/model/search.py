class Search:

    def __init__(self, words="", types=[], ages=[], start=0, size=10, sort=None, category=None):
        self.words = words
        self.total = 0
        self.hits = []
        self.types = types
        self.ages = ages
        self.start = start
        self.size = size
        self.sort = sort
        self.category = category;
        self.type_counts = [];
        self.age_counts = [];

    def add_aggregation(self, field, value, count, is_selected):
        if field == 'ages':
            self.age_counts.append(AggCount(value, count, is_selected))
        if field == 'types':
            self.type_counts.append(AggCount(value, count, is_selected))

class AggCount:
    value = ""
    count = 0
    is_selected = False

    def __init__(self, value, count, is_selected):
        self.value = value
        self.count = count
        self.is_selected = is_selected

class Sort:
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
