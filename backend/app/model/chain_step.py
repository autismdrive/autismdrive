from sqlalchemy import func

from app import db


class ChainStep(db.Model):
    __tablename__ = 'chain_step'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    instruction = db.Column(db.String)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
