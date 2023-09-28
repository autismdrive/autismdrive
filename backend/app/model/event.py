from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.model.location import Location
from app.model.user import User


class Event(Location):
    __tablename__ = "event"
    __label__ = "Events and Training"
    id = Column(Integer, ForeignKey("location.id"), primary_key=True)
    date = Column(DateTime)
    time = Column(String)
    ticket_cost = Column(String)
    location_name = Column(String)
    includes_registration = Column(Boolean)
    webinar_link = Column(String)
    post_survey_link = Column(String)
    max_users = Column(Integer)
    registration_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    post_event_description = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "event",
    }

    def indexable_content(self):
        return " ".join(
            filter(
                None,
                (
                    self.title,
                    self.description,
                    self.post_event_description,
                    self.insurance,
                    self.category_names(),
                ),
            )
        )


class EventUser(Base):
    __tablename__ = "event_user"
    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    event_id = Column(Integer, ForeignKey(Event.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    event = relationship(Event, backref="event_users")
    user = relationship(User, backref="user_events")


Event.registered_users = relationship(EventUser, back_populates="event")
