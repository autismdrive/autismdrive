from app import db
from app.model.resource import StarResource


class Location(StarResource):
    __tablename__ = 'location'
    id = db.Column(db.Integer, db.ForeignKey('resource.id'), primary_key=True)
    primary_contact = db.Column(db.String)
    street_address1 = db.Column(db.String)
    street_address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    email = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }
