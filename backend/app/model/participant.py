from sqlalchemy import func

from app import db
from app.model.step_log import StepLog
from app.model.flows import Flows
from app.model.participant_relationship import Relationship


# Describes the relationship between the User model and the participant
from app.model.questionnaires.identification_questionnaire import IdentificationQuestionnaire

# Provides contact information for the participant
from app.model.questionnaires.contact_questionnaire import ContactQuestionnaire
from app.model.random_id_generator import random_integer


class Participant(db.Model):
    # The participant model is used to track enrollment and participation in studies. Participants are associated
    # with a user account; sometimes that of themselves and sometimes that of their guardian.
    __tablename__ = 'stardrive_participant'
    id = db.Column(db.Integer, primary_key=True, default=random_integer)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('stardrive_user.id'))
    user = db.relationship("User", back_populates="participants")
    identification = db.relationship(IdentificationQuestionnaire, uselist=False)
    contact = db.relationship(ContactQuestionnaire, uselist=False)
    relationship = db.Column(db.Enum(Relationship))
    avatar_icon = db.Column(db.String)
    avatar_color = db.Column(db.String)
    has_consented = db.Column(db.Boolean)

    def get_name(self):
        if self.identification:
            return self.identification.get_name()
        else:
            return ""

    def get_percent_complete(self):
        flow = Flows.get_flow_by_relationship(self.relationship)
        step_logs = db.session.query(StepLog).filter_by(participant_id=self.id, flow=flow.name)
        complete_steps = 0
        for log in step_logs:
            flow.update_step_progress(log)

        for step in flow.steps:
            if step.status is 'COMPLETE':
                complete_steps += 1

        return complete_steps / len(flow.steps)
