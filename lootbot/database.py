from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, declarative_base

engine = create_engine('sqlite:///loot.sqlite3', future=True)
session = Session(engine)

Base = declarative_base()


def get_session():
    return session


class Loot(Base):
    __tablename__ = 'loot'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(String, nullable=False)
    item = Column(String, nullable=False)
    belongs_to = Column(String, nullable=True)
