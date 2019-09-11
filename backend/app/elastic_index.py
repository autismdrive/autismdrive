from elasticsearch import RequestError
from elasticsearch_dsl import Date, Keyword, Text, Index, analyzer, Integer, tokenizer, Document, Double, GeoPoint, \
    Search, A
import elasticsearch_dsl
from elasticsearch_dsl.connections import connections
import logging

from elasticsearch_dsl.query import MultiMatch, MatchAll

autocomplete = analyzer('autocomplete',
                        tokenizer=tokenizer('ngram', 'edge_ngram', min_gram=2, max_gram=15,
                                            token_chars=["letter", "digit"]),
                        filter=['lowercase']
                        )
autocomplete_search = analyzer('autocomplete_search',
                               tokenizer=tokenizer('lowercase')
                               )


# Star Documents are ElasticSearch documents and can be used to index an Event,
# Location, Resource, or Study
class StarDocument(Document):
    type = Keyword()
    label = Keyword()
    id = Integer()
    title = Text(analyzer=autocomplete, search_analyzer=autocomplete_search)
    last_updated = Date()
    content = Text(analyzer=autocomplete, search_analyzer=autocomplete_search)
    description = Text(analyzer=autocomplete, search_analyzer=autocomplete_search)
    organization = Keyword()
    website = Keyword()
    location = Keyword()
    age_range = Keyword()
    status = Keyword()
    topic = Keyword(multi=True)
    category = Keyword(multi=True)
    child_category = Keyword(multi=True)
    latitude = Double()
    longitude = Double()
    geo_point = GeoPoint()


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
                           age_range=None,
                           status=None,
                           # Fixme:  I'd love to rename topic to category, and remove child_category
                           topic=[],
                           category=[],
                           child_category=[],
                           latitude=None,
                           longitude=None,
                           geo_point=None
                           )

        doc.meta.id = self._get_id(document)

        if document.__tablename__ is not 'study':
            doc.website = document.website
        elif document.status is not None:
                doc.status = document.status.value

        if document.organization is not None:
            doc.organization = document.organization.name

        for cat in document.categories:
            doc.topic.extend(cat.category.all_search_paths())
            # Fixme:  I think we can drop all of this logic around parent category and cateogry fields
            if cat.category.parent:
                if cat.category.parent.name in ['Locations', 'Virginia', 'West Virginia']:
                    doc.location = cat.category.name
                    doc.child_category.append(cat.category.name)
                elif cat.category.parent.name == 'Age Range':
                    doc.age_range = cat.category.name
                    doc.child_category.append(cat.category.name)
                elif cat.category.parent.name == 'Type of Resources':
                    doc.child_category.append(cat.category.name)
                elif cat.category.parent.parent_id:
                    doc.category.append(cat.category.parent.parent.name)
                    doc.child_category.append(cat.category.name)
                else:
                    doc.category.append(cat.category.parent.name)
                    doc.child_category.append(cat.category.name)
            else:
                doc.category.append(cat.category.name)

        if (doc.type is 'location') and None not in (latitude, longitude):
            doc.latitude = latitude
            doc.longitude = longitude
            doc.geo_point = dict(lat=latitude, lon=longitude)

        StarDocument.save(doc, index=self.index_name)
        if flush:
            self.index.flush()

    def load_documents(self, resources, events, locations, studies):
        print("Loading search records of events, locations, resources, and studies into Elasticsearch index: %s" % self.index_prefix)
        for r in resources:
            self.add_document(r, flush=False)
        for e in events:
            self.add_document(e, flush=False)
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
            query = MultiMatch(query=search.words, fields=['title^10', 'content^5', 'description^5', 'location^3', 'category^2', 'child_category^2',
                      'organization', 'website'])

        elastic_search = Search(index=self.index_name)\
            .doc_type(StarDocument)\
            .query(query)\
            .highlight('content', fragment_size=50)

        for f in search.filters:
            elastic_search = elastic_search.filter('terms', **{f.field: f.value})

        if sort is not None:
            elastic_search = elastic_search.sort(sort)

        if search.category and search.category.id:
            elastic_search = elastic_search.post_filter('terms', topic=[str(search.category.search_path())])
            if search.category.calculate_level() == 0:
                exclude = ".*\\,.*\\,.*";
                include = str(search.category.id) + "\\,.*"
                aggregation = A("terms", field='topic', exclude=exclude, include=include)
            elif search.category.calculate_level() == 1:
                include = ".*\\,.*\\,.*";
                aggregation = A("terms", field='topic', include=include)
            else:
                aggregation = A("terms", field='topic')
        else:
            aggregation = A("terms", field='topic', exclude=".*\\,.*")

        elastic_search.aggs.bucket('terms', aggregation)

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
