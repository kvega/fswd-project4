#!/usr/bin/env python2

# Imports for connecting to SQLite DB
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

# Connect to DB
DBNAME = "sqlite:///itemcatalogwithusers.db"

engine = create_engine(DBNAME)

Base.metadata.bind = engine

# Create DB session instance
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create list of categories
CATEGORIES = [
        "Soccer",
        "Basketball",
        "Baseball",
        "Frisbee",
        "Snowboarding",
        "Rock Climbing",
        "Foosball",
        "Skating",
        "Hockey"
        ]

# List of items
ITEMS = [
        Item(category_id=1, title="Soccer Cleats", description="The shoes"),
        Item(category_id=1, title="Jersey", description="The shirt"),
        Item(category_id=2, title="Jersey", description="The shirt"),
        Item(category_id=3, title="Bat", description="The bat"),
        Item(category_id=5, title="Snowboard", description="The board")
        ]

# Add Categories to DB
def add_categories(categories):
    for category in categories:
        new_category = Category(title=category)
        try:
            session.add(new_category)
            session.commit()
        except exc.IntegrityError:
            session.rollback()

# Add Items to DB
def add_items(items):
    for item in items:
        try:
            session.add(item)
            session.commit()
        except exc.IntegrityError:
            session.rollback()


add_categories(CATEGORIES)
# add_items(ITEMS)
