import datetime

from dateutil.tz import tzutc
from marshmallow_sqlalchemy import ModelSchema

from app import db


class ExportLog(db.Model):
    __tablename__ = 'export_log'
    __no_export__ = True  # Don't export this logging information.
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=tzutc()))
    available_records = db.Column(db.Integer)
    alerts_sent = db.Column(db.Integer, default=0)
