# Tracking
# *****************************
import datetime

from flask import Blueprint, send_file

from app.database import session
from app.model.email_log import EmailLog

tracking_blueprint = Blueprint("track", __name__, url_prefix="/api/track")


@tracking_blueprint.route("/<string:user_id>/<string:code>/UVA_STAR-logo.png")
def logo(user_id, code):
    email_log = session.query(EmailLog).filter_by(user_id=user_id, tracking_code=code).first()
    if email_log:
        email_log.viewed = True
        email_log.date_viewed = datetime.datetime.utcnow()
        session.add(email_log)
        session.commit()
    return send_file("static/UVA_STAR-logo.png", mimetype="image/png")
