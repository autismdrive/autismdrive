import datetime

from elasticsearch import RequestError
from elasticsearch_dsl import Date, Keyword, Text, Index, analyzer, Integer, tokenizer, Document, Double, GeoPoint, \
    Search, A, Boolean, analysis
from elasticsearch_dsl.connections import connections
import logging

from elasticsearch_dsl.query import MultiMatch, MatchAll, Query, MoreLikeThis

autocomplete = analyzer('autocomplete',
                        tokenizer=tokenizer('ngram', 'edge_ngram', min_gram=2, max_gram=15,
                                            token_chars=["letter", "digit"]),
                        filter=['lowercase']
                        )
autocomplete_search = analyzer('autocomplete_search',
                               tokenizer=tokenizer('lowercase')
                               )

english_stem_filter = analysis.token_filter('my_english_filter', name="minimal_english", type="stemmer")
stem_analyzer = analyzer('stem_analyzer',
                        tokenizer=tokenizer('standard'),
                        filter=['lowercase', english_stem_filter])


# Star Documents are ElasticSearch documents and can be used to index an Event,
# Location, Resource, or Study
class StarDocument(Document):
    type = Keyword()
    label = Keyword()
    id = Integer()
    title = Text()
    date = Date()
    last_updated = Date()
    content = Text(analyzer=stem_analyzer)
    description = Text()
    organization = Keyword()
    website = Keyword()
    location = Keyword()
    ages = Keyword(multi=True)
    status = Keyword()
    category = Keyword(multi=True)
    latitude = Double()
    longitude = Double()
    geo_point = GeoPoint()
    status = Keyword()
    no_address = Boolean()


class ElasticIndex:

    logger = logging.getLogger("ElasticIndex")

    def __init__(self, app):
        self.logger.debug("Initializing Elastic Index")
        self.establish_connection(app.config['ELASTIC_SEARCH'])
        self.index_prefix = app.config['ELASTIC_SEARCH']["index_prefix"]

        self.index_name = '%s_resources' % self.index_prefix
        self.index = Index(self.index_name)
        self.index.doc_type(StarDocument)
        try:
            self.index.create()
        except RequestError as requestError:
            if requestError.error == 'resource_already_exists_exception':
                self.logger.info("The index already exists.")
            else:
                self.logger.fatal("Error Creating Index. ")
                raise requestError
        except Exception as e:
            self.logger.info("Failed to create the index(s).  They may already exist." + str(e))

    def establish_connection(self, settings):
        """Establish connection to an ElasticSearch host, and initialize the Submission collection"""
        if settings["http_auth_user"] != '':
            self.connection = connections.create_connection(
                hosts=settings["hosts"],
                port=settings["port"],
                timeout=settings["timeout"],
                verify_certs=settings["verify_certs"],
                use_ssl=settings["use_ssl"],
                http_auth=(settings["http_auth_user"],
                           settings["http_auth_pass"]))
        else:
            # Don't set an http_auth at all for connecting to AWS ElasticSearch or you will
            # get a cryptic message that is darn near ungoogleable.
            self.connection = connections.create_connection(
                hosts=settings["hosts"],
                port=settings["port"],
                timeout=settings["timeout"],
                verify_certs=settings["verify_certs"],
                use_ssl=settings["use_ssl"])

    def clear(self):
        try:
            self.logger.info("Clearing the index.")
            self.index.delete(ignore=404)
            self.index.create()
        except:
            self.logger.error("Failed to delete the indices. They might not exist.")

    def remove_document(self, document, flush=True):
        obj = self.get_document(document)
        obj.delete()
        if flush:
            self.index.flush()

    @staticmethod
    def _get_id(document):
        return document.__tablename__.lower() + '_' + str(document.id)

    def get_document(self, document):
        uid = self._get_id(document)
        return StarDocument.get(id=uid, index=self.index_name)

    def update_document(self, document, flush=True, latitude=None, longitude=None):
        # update is the same as add, as it will overwrite.  Better to have code in one place.
        self.add_document(document, flush, latitude, longitude)

    def add_document(self, document, flush=True, latitude=None, longitude=None):
        doc = StarDocument(id=document.id,
                           type=document.__tablename__,
                           label=document.__label__,
                           title=document.title,
                           last_updated=document.last_updated,
                           content=document.indexable_content(),
                           description=document.description,
                           location=None,
                           ages=document.ages,
                           status=None,
                           category=[],
                           latitude=None,
                           longitude=None,
                           geo_point=None
                           )

        if hasattr(document, 'date'):
            doc.date = document.date
        if hasattr(document, 'website'):
            doc.website = document.website
        if hasattr(document, 'status'):
            doc.status = document.status.value

        doc.meta.id = self._get_id(document)

        if document.organization is not None:
            doc.organization = document.organization.name

        for cat in document.categories:
            doc.category.extend(cat.category.all_search_paths())

        if document.__tablename__ is 'study':
            doc.title = document.short_title
            doc.description = document.short_description

        if (doc.type in ['location', 'event']) and None not in (latitude, longitude):
            doc.latitude = latitude
            doc.longitude = longitude
            doc.geo_point = dict(lat=latitude, lon=longitude)
            doc.no_address = not document.street_address1

        StarDocument.save(doc, index=self.index_name)
        if flush:
            self.index.flush()

    def load_documents(self, resources, events, locations, studies):
        print("Loading search records of events, locations, resources, and studies into Elasticsearch index: %s" % self.index_prefix)
        for r in resources:
            self.add_document(r, flush=False)
        for e in events:
            self.add_document(e, flush=False, latitude=e.latitude, longitude=e.longitude)
        for l in locations:
            self.add_document(l, flush=False, latitude=l.latitude, longitude=l.longitude)
        for s in studies:
            self.add_document(s, flush=False)
        self.index.flush()

    def search(self, search):
        sort = None if search.sort is None else search.sort.translate()

        if not search.words:
            query = MatchAll()
        else:
            query = MultiMatch(query=search.words, fields=['content'])

        elastic_search = Search(index=self.index_name)\
            .doc_type(StarDocument)\
            .query(query)\
            .highlight('content', type='unified', fragment_size=50)

        elastic_search = elastic_search[search.start:search.start + search.size]

        # Filter results for type and ages
        if search.types:
            elastic_search = elastic_search.filter('terms', **{"type": search.types})
        if search.ages:
            elastic_search = elastic_search.filter('terms', **{"ages": search.ages})

        # Filter results by date
        if search.date:
            elastic_search = elastic_search.filter('range', **{"date": {"gte": search.date}})
        else:
            elastic_search = elastic_search.filter('bool', **{"should": [
                {"range": {"date": {"gte": datetime.datetime.now()}}},  # Future events OR
                {"bool": {"must_not": {"exists": {"field": "date"}}}}   # Date field is empty
            ]})

        if sort is not None:
            elastic_search = elastic_search.sort(sort)

        if search.category and search.category.id:
            elastic_search = elastic_search.filter('terms', category=[str(search.category.search_path())])
            if search.category.calculate_level() == 0:
                exclude = ".*\\,.*\\,.*";
                include = str(search.category.id) + "\\,.*"
                aggregation = A("terms", field='category', exclude=exclude, include=include)
            elif search.category.calculate_level() == 1:
                include = ".*\\,.*\\,.*";
                aggregation = A("terms", field='category', include=include)
            else:
                aggregation = A("terms", field='category')
        else:
            aggregation = A("terms", field='category', exclude=".*\\,.*")

        elastic_search.aggs.bucket('terms', aggregation)
        elastic_search.aggs.bucket('type', A("terms", field='type'))
        elastic_search.aggs.bucket('ages', A("terms", field='ages'))

        # KEEPING FOR NOW - THESE WERE THE ORIGINAL FACETS WE HAD SET UP.  WILL NEED TO CONVERT TO AGGREGATIONS
        # IF WE WANT TO KEEP ANY OF THESE.
        # 'Location': elasticsearch_dsl.TermsFacet(field='location'),
        # 'Type': elasticsearch_dsl.TermsFacet(field='label'),
        # 'Age Range': elasticsearch_dsl.TermsFacet(field='age_range'),
        # 'Category': elasticsearch_dsl.TermsFacet(field='category'),
        # 'Organization': elasticsearch_dsl.TermsFacet(field='organization'),
        # 'Status': elasticsearch_dsl.TermsFacet(field='status'),
        # 'Topic': elasticsearch_dsl.TermsFacet(field='topic'),

        return elastic_search.execute()

    # Finds all resources related to the given item.
    def more_like_this(self, item, max_hits=3):

        query = MoreLikeThis(
            like=[
                # {'_id': ElasticIndex._get_id(item), '_index': self.index_name},
                item.indexable_content(),
                item.category_names()
            ],
            min_term_freq=1,
            min_doc_freq=2,
            max_query_terms=12,
            fields=['title', 'content', 'description', 'location', 'category', 'organization', 'website'])

        elastic_search = Search(index=self.index_name)\
            .doc_type(StarDocument)\
            .query(query)

        elastic_search = elastic_search[0:max_hits]


        return elastic_search.execute()
