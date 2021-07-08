from app.model.age_range import AgeRange


class AggCount:
    value = ""
    count = 0
    is_selected = False

    def __init__(self, value, count, is_selected):
        self.value = value
        self.count = count
        self.is_selected = is_selected


class Search:
    # Creates a pre ordered list of aggregation counts based on order in Age Range class.
    @staticmethod
    def known_age_counts():
        return list(map(lambda age_name: (AggCount(age_name, 0, False)), AgeRange.ages))

    @staticmethod
    def known_language_counts():
        return list(map(lambda age_name: (AggCount(age_name, 0, False)),
                        ['english', 'spanish', 'chinese', 'korean', 'vietnamese', 'arabic', 'tagalog']))

    def __init__(self, words="", types=None, ages=None, languages=None, start=0, size=10, sort=None, category=None, date=None,
                 map_data_only=False, geo_point = None, geo_box = None):
        self.words = words
        self.total = 0
        self.hits = []
        self.types = [] if types is None else types
        self.ages = [] if ages is None else ages
        self.languages = [] if languages is None else languages
        self.start = start
        self.size = size
        self.sort = sort
        self.category = category
        self.type_counts = []
        self.age_counts = Search.known_age_counts()
        self.language_counts = Search.known_language_counts()
        self.date = date
        self.map_data_only = map_data_only  # When we should return a limited set of details just for mapping.
        self.geo_box = geo_box

    # Method called when updating a search with fresh results.
    # This should zero-out any existing data that should be overwritten.
    def reset(self):
        self.type_counts = []
        self.age_counts = Search.known_age_counts()
        self.language_counts = Search.known_language_counts()
        self.hits = []
        self.total = 0

    def add_aggregation(self, field, value, count, is_selected):
        if field == 'ages':
            try:
                ac = next(ac for ac in self.age_counts if ac.value == value)
                ac.count = count
                ac.is_selected = is_selected
            except StopIteration:  # Go ahead and add it so it shows up, but this is bad data..
                self.age_counts.append(AggCount(value, count, is_selected))
        if field == 'languages':
            try:
                lc = next(lc for lc in self.language_counts if lc.value == value)
                lc.count = count
                lc.is_selected = is_selected
            except StopIteration:  # Go ahead and add it so it shows up, but this is bad data..
                self.language_counts.append(AggCount(value, count, is_selected))
        if field == 'types':
            self.type_counts.append(AggCount(value, count, is_selected))

    # can be used to verify that a given age range is supported.
    @staticmethod
    def has_age_range():
        return next((ac for ac in Search.known_age_counts if ac.value == 'value'), None) is not None

    # can be used to verify that a given language is supported.
    @staticmethod
    def has_language():
        return next((ac for ac in Search.known_language_counts() if ac.value == 'value'), None) is not None

class Geopoint:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class Geobox:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

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

    def __init__(self, result_id, content, description, title, doc_type, label, date, last_updated, highlights, latitude,
                 longitude, status, no_address, is_draft, post_event_description):
        self.id = result_id
        self.content = content
        self.description = description
        self.post_event_description = post_event_description
        self.title = title
        self.type = doc_type
        self.label = label
        self.date = date
        self.last_updated = last_updated
        self.highlights = highlights
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.no_address = no_address
        self.is_draft = is_draft


class MapHit:

    def __init__(self, result_id, doc_type, latitude, longitude, no_address):
        self.id = result_id
        self.latitude = latitude
        self.longitude = longitude
        self.type = doc_type
        self.no_address = no_address
