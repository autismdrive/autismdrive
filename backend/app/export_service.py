# Thanks to https://gist.github.com/piersstorey/b32583f0cc5cba0a38a11c2b123af687
from flask import url_for
from sqlalchemy import func
from sqlalchemy.ext.serializer import loads, dumps
from app import db
from app.model.export_info import ExportInfo
from app.question_service import QuestionService


class DataExport:

    @staticmethod
    def get_model_for_table(table):
        for c in db.Model._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == table.name:
                return c

    @staticmethod
    def get_model_for_name(name):
        for c in db.Model._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == name:
                return c

    # Returns a list of everything that can be exported from the sytsem.
    @staticmethod
    def all_exportable_data_names():
        tables = []
        for table in db.metadata.sorted_tables:
            db_model = DataExport.get_model_for_table(table)
            export_info = ExportInfo()
            export_info.name = db_model.__name__
            export_info.size = db.session.execute(db.select([func.count()]).select_from(table)).scalar()
            export_info.url = url_for("api.exportendpoint", name=QuestionService.snake_case_it(db_model.__name__))
            if hasattr(db_model, '__question_type__'):
                export_info.type = db_model.__question_type__
            tables.append(export_info)

        return tables

    def get_mapped_classes(self):
        self.models = []
        """Gets a list of SQLALchemy mapped classes"""
        self.add_subclasses(db.Model)
        return self.models

    def add_subclasses(self, model):
        """Feed self.models filtering `do_not_backup` and abstract models"""
        if model.__subclasses__():
            for submodel in model.__subclasses__():
                self.add_subclasses(submodel)
        else:
            self.models.append(model)

    def get_data(self, modelName):
        print("Exporting " + modelName)
        """Go through every mapped class and dumps the data"""
        model = DataExport.get_model_for_name(modelName)
        query = db.session.query(model)
        return query.all()

    def parse_data(self, contents):
        """Loads a dump and convert it into rows """
        db = self.db()
        return loads(contents, db.metadata, db.session)
