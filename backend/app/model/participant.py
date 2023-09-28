from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

from app.database import session, Base
from app.model.flows import Flows
from app.model.participant_relationship import Relationship

# Provides contact information for the participant
from app.model.questionnaires.contact_questionnaire import ContactQuestionnaire

# Describes the relationship between the User model and the participant
from app.model.questionnaires.identification_questionnaire import IdentificationQuestionnaire
from app.model.random_id_generator import random_integer
from app.model.step_log import StepLog


class Participant(Base):
    # The participant model is used to track enrollment and participation in studies. Participants are associated
    # with a user account; sometimes that of themselves and sometimes that of their guardian.
    __tablename__ = "stardrive_participant"
    id = Column(Integer, primary_key=True, default=random_integer)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey("stardrive_user.id"))
    user = relationship("User", back_populates="participants")
    identification = relationship(IdentificationQuestionnaire, uselist=False)
    contact = relationship(ContactQuestionnaire, uselist=False)
    relationship = Column(Enum(Relationship))
    avatar_icon = Column(String)
    avatar_color = Column(String)
    has_consented = Column(Boolean)

    def get_name(self):
        if self.identification:
            return self.identification.get_name()
        else:
            return ""

    def get_percent_complete(self):
        flow = Flows.get_flow_by_relationship(self.relationship)
        step_logs = (
            session.query(StepLog).filter(StepLog.participant_id == self.id).filter(StepLog.flow == flow.name).all()
        )
        complete_steps = 0
        for log in step_logs:
            flow.update_step_progress(log)

        for step in flow.steps:
            if step.status == step.STATUS_COMPLETE:
                complete_steps += 1

        return complete_steps / len(flow.steps)
