from sqlalchemy import Column, Integer, String, ForeignKey, Float

from app.model.resource import Resource


class Location(Resource):
    __tablename__ = "location"
    __label__ = "Local Services"
    id = Column(Integer, ForeignKey("resource.id"), primary_key=True)
    primary_contact = Column(String)
    street_address1 = Column(String)
    street_address2 = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    email = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "location",
    }
