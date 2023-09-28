from flask_marshmallow import Schema
from flask_marshmallow.fields import Hyperlinks, URLFor
from marshmallow import fields as ma_fields
from marshmallow.fields import Nested, List, Integer as MaInteger
from sqlalchemy import func, ForeignKey, Column, Integer, DateTime, String, Boolean, TEXT
from sqlalchemy.orm import relationship

from app.database import Base
from app.schema.model_schema import ModelSchema


class DataTransferLog(Base):
    """Records the action of a data transfer - So long as the number of records to be
    transferred is 0, this log is updated with a last_attempt rather than creating a new log."""

    __tablename__ = "data_transfer_log"
    __no_export__ = True  # Don't export this logging information.
    id = Column(Integer, primary_key=True)
    type = Column(String)  # Either importing or exporting
    date_started = Column(DateTime(timezone=True), default=func.now())
    last_updated = Column(DateTime(timezone=True), default=func.now())
    total_records = Column(Integer)
    alerts_sent = Column(Integer, default=0)
    details = relationship("DataTransferLogDetail")

    def successful(self):
        return next((x for x in self.details if not x.successful), None) is None


class DataTransferLogDetail(Base):
    """When data is successfully transfered it is recorded in the detail log which contains
    one record per class that is transfered."""

    __tablename__ = "data_transfer_log_detail"
    __no_export__ = True  # Don't export this logging information.
    id = Column(Integer, primary_key=True)
    data_transfer_log_id = Column(Integer, ForeignKey("data_transfer_log.id"))
    date_started = Column(DateTime(timezone=True), default=func.now())
    last_updated = Column(DateTime(timezone=True), default=func.now())
    class_name = Column(String)
    successful = Column(Boolean)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    errors = Column(TEXT, default="")

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
        fields = ("id", "type", "date_started", "last_updated", "total_records", "alerts_sent", "details", "_links")

    details = Nested(DataTransferLogDetailSchema, dump_only=True, many=True)
    _links = Hyperlinks({"self": URLFor("api.datatransferlogendpoint", id="<id>")})


class DataTransferLogPageSchema(Schema):
    pages = ma_fields.Integer()
    total = ma_fields.Integer()
    items = List(Nested(DataTransferLogSchema))
