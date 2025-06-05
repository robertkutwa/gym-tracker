from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from gym_tracker.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    workouts = relationship("Workout", back_populates="user")

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")

class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    workout = relationship("Workout", back_populates="exercises")