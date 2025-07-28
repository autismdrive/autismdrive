from typing import Literal
from icecream import ic, IceCreamDebugger

ic.configureOutput(includeContext=True, contextAbsPath=True)


class LogService:
    print: IceCreamDebugger = ic

    @classmethod
    def test_print(cls, message: str):
        cls.print(message)

    @classmethod
    def log_study_change(cls, study_id: int, study_title: str, change_type: Literal["create", "edit", "delete"]):
        from flask import g

        from app.database import session
        from app.models import StudyChangeLog

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
        from flask import g

        from app.database import session
        from app.models import ResourceChangeLog

        log = ResourceChangeLog(
            resource_id=resource_id,
            resource_title=resource_title,
            user_id=g.user.id,
            user_email=g.user.email,
            type=change_type,
        )
        session.add(log)
        session.commit()
