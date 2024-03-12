from typing import Literal

from flask import g

from app.database import session
from app.models import ResourceChangeLog, StudyChangeLog


class LogService:
    @classmethod
    def log_study_change(cls, study_id: int, study_title: str, change_type: Literal["create", "edit", "delete"]):
        log = StudyChangeLog(
            study_id=study_id,
            study_title=study_title,
            user_id=g.user.id,
            user_email=g.user.email,
            type=change_type,
        )
        session.add(log)
        session.commit()

    @classmethod
    def log_resource_change(
        cls, resource_id: int, resource_title: str, change_type: Literal["create", "edit", "delete"]
    ):
        log = ResourceChangeLog(
            resource_id=resource_id,
            resource_title=resource_title,
            user_id=g.user.id,
            user_email=g.user.email,
            type=change_type,
        )
        session.add(log)
        session.commit()
