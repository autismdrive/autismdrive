import datetime


class Search:
    query = ""
    filters = []
    total = 0
    hits = []
    facets = []
    start = 0
    size = 0
    sort = None

    def __init__(self, query="", filters=[], start=0, size=10, sort=None):
        self.query = query
        self.filters = filters
        self.start = start
        self.size = size
        self.sort = sort

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


class Hit:

    def __init__(self, result_id, content, title, doc_type, last_updated, highlights):
        self.id = result_id
        self.content = content
        self.title = title
        self.type = doc_type
        self.last_updated = last_updated
        self.highlights = highlights
