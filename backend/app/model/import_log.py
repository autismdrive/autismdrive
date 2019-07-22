import datetime

from dateutil.tz import tzutc
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import func

from app import db, ma


class ImportLog(db.Model):
    __tablename__ = 'import_log'
    __no_export__ = True  # Don't export the import log
    id = db.Column(db.Integer, primary_key=True)
    date_started = db.Column(db.DateTime(timezone=True), default=func.now())
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    class_name = db.Column(db.String)
    successful = db.Column(db.Boolean)
    success_count = db.Column(db.Integer, default=0)
    failure_count = db.Column(db.Integer, default=0)
    errors = db.Column(db.TEXT, default="")

    def handle_failure(self, error):
        if not self.errors:
            self.errors = ""
        self.errors += str(error)
        self.failure_count += 1
        self.successful = False

    def handle_success(self):
        self.success_count += 1


class ImportLogSchema(ModelSchema):
    class Meta:
        model = ImportLog
        ordered = True
        include_fk = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.importlogendpoint', id='<id>')
    })


class ImportLogPagesSchema(ma.Schema):
    pages = fields.Integer()
    total = fields.Integer()
    items = ma.List(ma.Nested(ImportLogSchema))
