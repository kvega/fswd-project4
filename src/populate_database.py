#!/usr/bin/env python2

# Imports for connecting to SQLite DB
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# Connect to DB
DBNAME = "postgresql://catalog:catalog@localhost/catalog"

engine = create_engine(DBNAME)

Base.metadata.bind = engine

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
    Item(
        category_id=1,
        title="Soccer Cleats",
        description="The shoes",
        user_id=1),
    Item(category_id=1, title="Jersey", description="The shirt", user_id=1),
    Item(category_id=2, title="Jersey", description="The shirt", user_id=1),
    Item(category_id=3, title="Bat", description="The bat", user_id=1),
    Item(category_id=5, title="Snowboard", description="The board", user_id=1)
]

# List of users
USERS = [
    User(name="John Doe", email="johndoe@example.com")
]

# Add Categories to DB


def add_categories(categories):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for category in categories:
        new_category = Category(title=category)
        try:
            session.add(new_category)
            session.commit()
        except exc.IntegrityError:
            session.rollback()

# Add Items to DB


def add_items(items):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for item in items:
        try:
            session.add(item)
            session.commit()
        except exc.IntegrityError:
            session.rollback()

# Add Users to DB


def add_users(users):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for user in users:
        try:
            session.add(user)
            session.commit()
        except exc.IntegrityError:
            session.rollback()


add_categories(CATEGORIES)
add_items(ITEMS)
add_users(USERS)
