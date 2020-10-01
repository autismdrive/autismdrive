from marshmallow import fields, EXCLUDE
from sqlalchemy import func, ForeignKey

from app import db, ma
from app.schema.model_schema import ModelSchema


class DataTransferLog(db.Model):
    """ Records the action of a data transfer - So long as the number of records to be
    transferred is 0, this log is updated with a last_attempt rather than creating a new log."""
    __tablename__ = 'data_transfer_log'
    __no_export__ = True  # Don't export this logging information.
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)  # Either importing or exporting
    date_started = db.Column(db.DateTime(timezone=True), default=func.now())
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    total_records = db.Column(db.Integer)
    alerts_sent = db.Column(db.Integer, default=0)
    details = db.relationship('DataTransferLogDetail')

    def successful(self):
        return next((x for x in self.details if not x.successful), None) is None


class DataTransferLogDetail(db.Model):
    '''When data is successfully transfered it is recorded in the detail log which contains
    one record per class that is transfered. '''
    __tablename__ = 'data_transfer_log_detail'
    __no_export__ = True  # Don't export this logging information.
    id = db.Column(db.Integer, primary_key=True)
    data_transfer_log_id = db.Column(db.Integer, ForeignKey('data_transfer_log.id'))
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


class DataTransferLogDetailSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = DataTransferLogDetail


class DataTransferLogSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = DataTransferLog
        fields = ('id', 'type', 'date_started', 'last_updated', 'total_records',
                  'alerts_sent', 'details', '_links')
    details = ma.Nested(DataTransferLogDetailSchema, dump_only=True, many=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.datatransferlogendpoint', id='<id>')
    })


class DataTransferLogPageSchema(ma.Schema):
    pages = fields.Integer()
    total = fields.Integer()
    items = ma.List(ma.Nested(DataTransferLogSchema))
