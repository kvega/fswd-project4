#!/usr/bin/env python2

# Imports for Flask app
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

# Imports for SQLite DB connection
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

#TODO: Imports for login_session setup

#TODO: Imports for OAuth setup

app = Flask(__name__)

# Connect to DB and create DB session
engine = create_engine("sqlite:///itemcatalog.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# URL routes

# Route to show the catalog
@app.route('/')
@app.route("/catalog")
def showCatalog():
    categories = session.query(Category).order_by(asc(Category._id)).all()
    recent_items = session.query(Item).order_by(desc(Item._id)).limit(10).all()
    return render_template("catalog.html", categories=categories,
        recent_items=recent_items)

# Route to show a category
@app.route("/catalog/<string:category_title>")
@app.route("/catalog/<string:category_title>/items")
def showCategory(category_title):
    categories = session.query(Category).order_by(asc(Category._id)).all()
    category = session.query(Category).filter_by(title=category_title).one()
    items = session.query(Item).filter_by(category_id=category._id).all()
    return render_template("categoryloggedin.html", categories=categories,
        category=category, items=items)

# Route to show an item
@app.route("/catalog/<string:category_title>/<string:item_title>")
def showItem(category_title, item_title):
    category = session.query(Category).filter_by(title=category_title).one()
    item = session.query(Item).filter_by(category_id=category._id, title=item_title).one()
    return render_template("itemloggedin.html", category=category, item=item)

# Route to create an item
@app.route("/catalog/new", methods=['GET', 'POST'])
def createItem():
    categories = session.query(Category).order_by(asc(Category._id)).all()
    if request.method == 'POST':
        new_item = Item(title=request.form['title'], description=request.form['description'],
            category_id=request.form['category'])
        session.add(new_item)
        session.commit()
        flash("New item %s successfully created" % new_item.title)
        return redirect(url_for('showCategory', category_title=categories[new_item.category_id-1].title))
    else: 
        return render_template("newitem.html", categories=categories)

# Route to update an item
@app.route("/catalog/<string:category_title>/<string:item_title>/edit")
def editItem(category_title, item_title):
    categories = session.query(Category).order_by(asc(Category._id)).all()
    category = session.query(Category).filter_by(title=category_title).one()
    edited_item = session.query(Item).filter_by(category_id=category._id, title=item_title).one()
    if request.method == 'POST':
        if request.form['title']:
            edited_item.title = request.form['title']
        if request.form['description']:
            edited_item.description = request.form['description']
        if request.form['category']:
            edited_item.category_id = request.form['category']
        session.add(edited_item)
        session.commit()
        flash("Item successfully updated")
        return redirect(url_for("showCategory", category_title=category_title))
    else:
        return render_template("edititem.html", categories=categories, category=category, item=item)

# Route to delete an item
@app.route("/catalog/<string:category_title>/<string:item_title>/delete")
def deleteItem(category_title, item_title):
    category = session.query(Category).filter_by(title=category_title).one()
    item = session.query(Item).filter_by(category_id=category._id, title=item_title).one()
    return render_template("deleteitem.html", item=item)

# Route to access Catalog JSON API
@app.route("/catalog.json")
def catalogJSON():
    return "Catalog JSON: JSON API endpoint to view Catalog information."


# Initialize Flask app
if __name__ == "__main__":
    app.secret_key = "super_duper_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
