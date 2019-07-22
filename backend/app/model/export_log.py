import datetime

from dateutil.tz import tzutc
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import func

from app import db, ma


class ExportLog(db.Model):
    __tablename__ = 'export_log'
    __no_export__ = True  # Don't export this logging information.
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    available_records = db.Column(db.Integer)
    alerts_sent = db.Column(db.Integer, default=0)


class ExportLogSchema(ModelSchema):
    class Meta:
        model = ExportLog
        ordered = True
        include_fk = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.exportlogendpoint', id='<id>')
    })


class ExportLogPagesSchema(ma.Schema):
    pages = fields.Integer()
    total = fields.Integer()
    items = ma.List(ma.Nested(ExportLogSchema))
