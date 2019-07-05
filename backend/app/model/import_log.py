import datetime

from dateutil.tz import tzutc
from marshmallow_sqlalchemy import ModelSchema

from app import db


class ImportLog(db.Model):
    __tablename__ = 'import_log'
    __no_export__ = True  # Don't export the import log
    id = db.Column(db.Integer, primary_key=True)
    date_started = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=tzutc()))
    last_updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=tzutc()))
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
