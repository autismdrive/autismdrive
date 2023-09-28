from sqlalchemy import func, Column, String, Integer, DateTime

from app.database import Base


class ChainStep(Base):
    __tablename__ = "chain_step"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    instruction = Column(String)
    last_updated = Column(DateTime(timezone=True), default=func.now())
