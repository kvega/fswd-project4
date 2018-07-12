#!/usr/bin/env python2

# Imports for setup of SQLite DB
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#==============================================================================
# Create Classes
#==============================================================================

# Category class
class Category(Base):
    __tablename__ = "category"

    _id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True)

    @property
    def serialize(self):
        """
        Return object data in serializeable format.
        """
        return {
                "_id"  : self._id,
                "title" : self.title 
            }


# Item class
class Item(Base):
    __tablename__ = "item"

    _id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey("category._id"), unique=True)
    category = relationship(Category)

    @property
    def serialize(self):
        """
        Return object data in serializeable format.
        """
        return {
                "cat_id": self.category_id,
                "_id" : self._id,
                "title" : self.title,
                "description" : self.description
            }


engine = create_engine("sqlite:///itemcatalog.db")

Base.metadata.create_all(engine)
