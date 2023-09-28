from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, BigInteger

from app.database import Base


class StepLog(Base):
    __tablename__ = "step_log"
    id = Column(Integer, primary_key=True)
    questionnaire_name = Column(String)
    questionnaire_id = Column(Integer)
    flow = Column(String)
    participant_id = Column("participant_id", Integer, ForeignKey("stardrive_participant.id"))
    user_id = Column("user_id", Integer, ForeignKey("stardrive_user.id"))
    date_completed = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger)
    last_updated = Column(DateTime(timezone=True), default=func.now())
