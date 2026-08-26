from sqlalchemy import Column, Integer, String, Text

from .database import Base


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(Integer, primary_key=True, index=True)

    goal = Column(Text, nullable=False)

    skill_level = Column(String(50), nullable=False)

    skills = Column(Text, nullable=False)

    study_hours = Column(Integer, nullable=False)

    duration = Column(String(50), nullable=False)


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)

    learner_id = Column(Integer, nullable=False, index=True)

    skill = Column(String(100), nullable=False)

    completed = Column(Integer, default=1)
