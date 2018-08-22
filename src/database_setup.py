#!/usr/bin/env python2

# Imports for setup of SQLite DB
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# ==============================================================================
# Create Classes
# ==============================================================================


# User Class
class User(Base):
    __tablename__ = "user"

    _id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

# Category class


class Category(Base):
    __tablename__ = "category"

    _id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True, nullable=False)

    @property
    def serialize(self):
        """
        Return object data in serializeable format.
        """
        return {
            "_id": self._id,
            "title": self.title
        }


# Item class
class Item(Base):
    __tablename__ = "item"

    _id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey("category._id"), nullable=False)
    category = relationship(Category)
    __table_args = (
        UniqueConstraint(
            "title",
            "category_id",
            name="item_category_uc"))
    user_id = Column(Integer, ForeignKey("user._id"), nullable=False)
    user = relationship(User)

    @property
    def serialize(self):
        """
        Return object data in serializeable format.
        """
        return {
            "cat_id": self.category_id,
            "_id": self._id,
            "title": self.title,
            "description": self.description
        }


engine = create_engine("sqlite:///itemcatalogwithusers.db")

Base.metadata.create_all(engine)
