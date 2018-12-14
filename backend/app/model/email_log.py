from app import db


class EmailLog(db.Model):
    __tablename__ = 'email_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    type = db.Column(db.String)
    tracking_code = db.Column(db.String)
    viewed = db.Column(db.Boolean)
    date_viewed = db.Column(db.DateTime)
