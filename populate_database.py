#!/usr/bin/env python2

# Imports for connecting to SQLite DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

# Connect to DB
DBNAME = "sqlite:///itemcatalog.db"

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

# Add Categories to DB
def add_categories(categories):
    for category in categories:
        new_category = Category(title=category)
        try:
            session.add(new_category)
            session.commit()
        #TODO: implement error handling to catch IntegrityError

