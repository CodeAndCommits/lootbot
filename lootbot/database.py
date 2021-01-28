import os
import logging

from sqlalchemy import create_engine, Column, Integer, String, select, delete, update, Index
from sqlalchemy.orm import Session, declarative_base

logger = logging.getLogger(__name__)

connection = os.getenv('connection')
print(connection)

logger.debug(f'Using connection: {connection}')

engine = create_engine(connection, future=True)
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

    Index('idx_guild_id_member_id', 'guild_id', 'member_id')


def add_item(item: Loot):
    session.add(item)
    session.commit()


def get_items(guild_id: str):
    return session.execute(select(Loot).where(Loot.guild_id == guild_id))


def get_member_items(guild_id: str, member_id: str):
    return session.execute(
        select(Loot)
            .where(Loot.guild_id == guild_id)
            .where(Loot.belongs_to == member_id)
    )


def remove_item(guild_id: str, loot: str):
    session.execute(
        delete(Loot)
            .where(Loot.guild_id == guild_id)
            .where(Loot.item == loot)
            .execution_options(synchronize_session="fetch")
    )
    session.commit()


def rename_item(guild_id: str, old_name: str, new_name: str):
    session.execute(
        update(Loot)
            .where(Loot.guild_id == guild_id)
            .where(Loot.item == old_name)
            .values(item=new_name)
            .execution_options(synchronize_session="fetch")

    )
    session.commit()


def assign_item(guild_id: str, item: str, member_id: str):
    session.execute(
        update(Loot)
            .where(Loot.guild_id == guild_id)
            .where(Loot.item == item)
            .values(belongs_to=member_id)
            .execution_options(synchronize_session="fetch")

    )

    session.commit()
