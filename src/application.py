#!/usr/bin/env python2

# Imports for Flask app
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

#TODO: Imports for SQLite DB connection

#TODO: Imports for login_session setup

#TODO: Imports for OAuth setup

app = Flask(__name__)

#TODO: Connect to DB and create DB session

# URL routes

# Route to show the catalog
@app.route('/')
@app.route("/catalog")
def showCatalog():
    return "Catalog: This is where the Categories will be displayed."

# Route to show a category
@app.route("/catalog/<string:category_title>")
@app.route("/catalog/<string:category_title>/items")
def showCategory(category_title):
    return "Category: This is where the Item List will be displayed."

# Route to show an item
@app.route("/catalog/<string:category_title>/<string:item_title>")
def showItem(category_title, item_title):
    return "Item: This is where the Item Info will be displayed."

# Route to create an item
@app.route("/catalog/<string:category_title>/new")
def createItem(category_title):
    return "New Item: This is where a user will be able to create an item."

# Route to update an item
@app.route("/catalog/<string:category_title>/<string:item_title>/edit")
def editItem(category_title, item_title):
    return "Edit Item: This is where a user will be able to update an item."

# Route to delete an item
@app.route("/catalog/<string:category_title>/<string:item_title>/delete")
def deleteItem(category_title, item_title):
    return "Delete Item: This is where a user will be able to delete an item."

# Route to access Catalog JSON API
@app.route("/catalog.json")
def catalogJSON():
    return "Catalog JSON: JSON API endpoint to view Catalog information."


# Initialize Flask app
if __name__ == "__main__":
    app.secret_key = "super_duper_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)


