from elasticsearch_dsl import Date, Keyword, Text, Index, analyzer, Integer, tokenizer, Document
import elasticsearch_dsl
from elasticsearch_dsl.connections import connections
import logging

autocomplete = analyzer('autocomplete',
                        tokenizer=tokenizer('ngram', 'edge_ngram', min_gram=2, max_gram=15,
                                            token_chars=["letter", "digit"]),
                        filter=['lowercase']
                        )
autocomplete_search = analyzer('autocomplete_search',
                               tokenizer=tokenizer('lowercase')
                               )


# Star Documents are ElastciSearch documents and can be used to index an Event, Location, Resource, or Study
class StarDocument(Document):
    type = Keyword()
    id = Integer()
    title = Text(analyzer=autocomplete, search_analyzer=autocomplete_search)
    last_updated = Date()
    content = Text(analyzer=autocomplete, search_analyzer=autocomplete_search)
    organization = Keyword()
    website = Keyword()
    location = Keyword()
    life_age = Keyword()
    category = Keyword(multi=True)
    child_category = Keyword(multi=True)


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
        except:
            self.logger.info("Failed to create the index(s).  They may already exist.")

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
            self.logger.error("Failed to delete the indices.  They night not exist.")

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

    def update_document(self, document, flush=True):
        # update is the same as add, as it will overwrite.  Better to have code in one place.
        self.add_document(document, flush)

    def add_document(self, document, flush=True):
        doc = StarDocument(id=document.id,
                           type=document.__tablename__.upper(),
                           title=document.title,
                           last_updated=document.last_updated,
                           content=document.indexable_content(),
                           location=None,
                           life_age=None,
                           category=[],
                           child_category=[]
                           )

        doc.meta.id = self._get_id(document)

        if document.__tablename__ is not 'study':
            doc.website = document.website

        if document.organization is not None:
            doc.organization = document.organization.name

        for cat in document.categories:
            if cat.category.parent:
                if cat.category.parent.name in ['Locations', 'Virginia', 'West Virginia']:
                    doc.location = cat.category.name
                    doc.child_category.append(cat.category.name)
                elif cat.category.parent.name == 'Life Ages':
                    doc.life_age = cat.category.name
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

        StarDocument.save(doc, index=self.index_name)
        if flush:
            self.index.flush()

    def load_documents(self, events, locations, resources, studies):
        print("Loading search records of events, locations, resources, and studies into %s" % self.index_prefix)
        for e in events:
            self.add_document(e, flush=False)
        for l in locations:
            self.add_document(l, flush=False)
        for r in resources:
            self.add_document(r, flush=False)
        for s in studies:
            self.add_document(s, flush=False)
        self.index.flush()

    def search(self, search):
        document_search = DocumentSearch(search.words, search.jsonFilters(), index=self.index_name)
        document_search = document_search[search.start:search.start + search.size]
        return document_search.execute()


class DocumentSearch(elasticsearch_dsl.FacetedSearch):
    def __init__(self, *args, **kwargs):
        self.index = kwargs["index"]
#        self.date_restriction = kwargs["date_restriction"]
        kwargs.pop("index")
#        kwargs.pop("date_restriction")
        super(DocumentSearch, self).__init__(*args, **kwargs)

    doc_types = [StarDocument]
    fields = ['title^10', 'content^5',  'location^3', 'category^2',  'child_category^2', 'organization', 'website']

    facets = {
        'Location': elasticsearch_dsl.TermsFacet(field='location'),
        'Type': elasticsearch_dsl.TermsFacet(field='type'),
        'Life Ages': elasticsearch_dsl.TermsFacet(field='life_age'),
        'Category': elasticsearch_dsl.TermsFacet(field='category'),
        'Organization': elasticsearch_dsl.TermsFacet(field='organization'),
    }

    def highlight(self, search):
        return search.highlight('content', fragment_size=50)

    def search(self):
        s = super(DocumentSearch, self).search()
        return s
