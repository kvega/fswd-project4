#!/usr/bin/env python2

# Imports for Flask app
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

# Imports for SQLite DB connection
from sqlalchemy import create_engine, exc, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

# Imports for login_session setup
from flask import session as login_session
import random, string

#TODO: Imports for OAuth setup
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open("client_secrets.json", 'r').read())["web"]["client_id"]

app = Flask(__name__)

# Connect to DB and create DB session
engine = create_engine("sqlite:///itemcatalogwithusers.db", connect_args={"check_same_thread": False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create cache for categories to reduce redundant DB queries. Users are unable to modify categories
CATEGORIES_CACHE = session.query(Category).order_by(asc(Category._id)).all()

# User Helper Functions

def createUser(login_session):
    session = DBSession()
    new_user = User(name=login_session["username"], email=login_session["email"],
        picture=login_session["picture"])
    try:
        session.add(new_user)
        session.commit()
        user = session.query(User).filter_by(email=login_session["email"]).one()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        return user._id

def getUserInfo(user_id):
    session = DBSession()
    try:
        user = session.query(User).filter_by(_id=user_id).one()
    except:
        return None
    finally:
        session.close()
        return user


def getUserId(email):
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        session.close()
        return user._id
    except:
        return None
        
    

# URL routes

# Create state token and store for future validation
@app.route("/login")
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    print "The current state token is %s" % state
    return render_template("login.html", STATE=state)


# Connect to Google Login
@app.route("/gconnect", methods=['POST'])
def gconnect():
    if request.args.get("state") != login_session['state']:
        response = make_response(json.dumps("Invalid state parameter"), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets("client_secrets.json", scope='')
        oauth_flow.redirect_uri = "postmessage"
        credentials = oauth_flow.step2_exchange(code) # exchanges code for flow_exchange object
    except FlowExchangeError:
        response = make_response(json.dumps("Failed to upgrade the authorization code."), 401)
        response.headers['Content-Type'] = "application/json"
        return response

    # Check to ensure that the access token is valid
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s" % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort
    if result.get("error") is not None:
        response = make_response(json.dumps(result.get("error")), 500)
        response.headers['Content-Type'] = "application/json"
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token["sub"]
    if result["user_id"] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = "application/json"
        return response

    # Verify that the access token is valid for this app.
    if result["issued_to"] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's"), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    
    stored_access_token = login_session.get("access_token")
    stored_gplus_id = login_session.get("gplus_id")
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = "application/json"
        return response

    # Store the access token in the session for later use.
    login_session["access_token"] = credentials.access_token
    login_session["gplus_id"] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"access_token": credentials.access_token, "alt": "json"}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session["username"] = data["name"]
    login_session["picture"] = data["picture"]
    login_session["email"] = data["email"]

    # Verify if user exists, if it doesn't create a new one
    user_id = getUserId(login_session["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session["user_id"] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session["username"]
    output += '!</h1>'
    output += '<img src="'
    output += login_session["picture"]
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Disconnect from Google
@app.route("/gdisconnect")
def gdisconnect():
    access_token = login_session.get("access_token")
    if access_token is None:
        print "Access Token is None"
        response = make_response(json.dumps("Current user not connected"), 401)
        response.headers['Content-Type'] = "application/json"
        print response
        return redirect(url_for('showCatalog'))
    print "In gdisconnect access token is %s" % access_token
    print "User name is: " 
    print login_session["username"]
    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
    print url
    h = httplib2.Http()
    print h
    result = h.request(url, 'GET')[0]
    print "result is " 
    print result
    if result["status"] == '200':
        del login_session["access_token"]
        del login_session["gplus_id"]
        del login_session["username"]
        del login_session["email"]
        del login_session["picture"]
        response = make_response(json.dumps("Successfully disconnected."), 200)
        response.headers['Content-type'] = "application/json"
        print response
        return redirect(url_for('showCatalog'))
    else:
        response = make_response(json.dumps("Failed to revoke token for given user."), 400)
        response.headers['Content-Type'] = "application/json"
        print response
        return redirect(url_for('showCatalog'))


# Route to show the catalog
@app.route('/')
@app.route("/catalog")
def showCatalog():
    recent_items = session.query(Item).order_by(desc(Item._id)).limit(10).all()
    return render_template("catalog.html", categories=CATEGORIES_CACHE,
        recent_items=recent_items, session=login_session)
    


# Route to show a category
@app.route("/catalog/<string:category_title>")
@app.route("/catalog/<string:category_title>/items")
def showCategory(category_title):
    category = session.query(Category).filter_by(title=category_title).one()
    items = session.query(Item).filter_by(category_id=category._id).all()
    if "username" not in login_session:
        return render_template("publiccategory.html", categories=CATEGORIES_CACHE, category=category, items=items, session=login_session)
    else:
        return render_template("category.html", categories=CATEGORIES_CACHE, category=category, items=items, session=login_session)


# Route to show an item
@app.route("/catalog/<string:category_title>/<string:item_title>")
def showItem(category_title, item_title):
    category = session.query(Category).filter_by(title=category_title).one()
    item = session.query(Item).filter_by(category_id=category._id, title=item_title).one()
    creator = getUserInfo(item.user_id)
    if "username" not in login_session or creator._id != login_session["user_id"]:
        return render_template("publicitem.html", categories=CATEGORIES_CACHE, category=category, item=item, session=login_session)
    else:
        return render_template("item.html", categories=CATEGORIES_CACHE, category=category, item=item, session=login_session)


# Route to create an item
@app.route("/catalog/new", methods=['GET', 'POST'])
def createItem():
    if "username" not in login_session:
        return redirect("/login")
    if request.method == 'POST':
        new_item = Item(title=request.form['title'], description=request.form['description'],
            category_id=request.form['category'], user_id=login_session["user_id"])
        try:
            session.add(new_item)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
        flash("New item %s successfully created" % new_item.title)
        return redirect(url_for('showCategory', category_title=CATEGORIES_CACHE[new_item.category_id-1].title))
    else: 
        return render_template("newitem.html", categories=CATEGORIES_CACHE, session=login_session)


# Route to update an item
@app.route("/catalog/<string:category_title>/<string:item_title>/edit", methods=['GET', 'POST'])
def editItem(category_title, item_title):
    if "username" not in login_session:
        return redirect("/login")
    category = session.query(Category).filter_by(title=category_title).one()
    edited_item = session.query(Item).filter_by(category_id=category._id, title=item_title).one()
    if edited_item.user_id != login_session["user_id"]:
        return "<script>function authFunction() {alert('You are not authorized to edit this item. Please create your own item in order to delete.');}</script><body onload='authFunction()'>"
    if request.method == 'POST':
        if request.form['title']:
            edited_item.title = request.form['title']
        if request.form['description']:
            edited_item.description = request.form['description']
        if request.form['category']:
            edited_item.category_id = request.form['category']
        try:
            session.add(edited_item)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
        flash("Item successfully updated")
        return redirect(url_for("showCategory", category_title=category_title))
    else:
        return render_template("edititem.html", categories=CATEGORIES_CACHE, category=category, item=edited_item, session=login_session)


# Route to delete an item
@app.route("/catalog/<string:category_title>/<string:item_title>/delete", methods=['GET', 'POST'])
def deleteItem(category_title, item_title):
    if "username" not in login_session:
        return redirect("/login")
    category = session.query(Category).filter_by(title=category_title).one()
    delete_item = session.query(Item).filter_by(category_id=category._id, title=item_title).one()
    if delete_item.user_id != login_session["user_id"]:
        return "<script>function authFunction() {alert('You are not authorized to edit this item. Please create your own item in order to delete.');}</script><body onload='authFunction()'>"
    if request.method == 'POST':
        session.delete(delete_item)
        session.commit()
        flash('Item successfully deleted')
        return redirect(url_for("showCategory", category_title=category_title))
    else: 
        return render_template("deleteitem.html", category_title=category_title, item=delete_item, session=login_session)


# Route to access Catalog JSON API
@app.route("/catalog.json")
def catalogJSON():
    cs = [c.serialize for c in CATEGORIES_CACHE]
    for c in cs:
        items = session.query(Item).filter_by(category_id=c["_id"]).all()
        if items:
            c["items"] = [i.serialize for i in items]
    return jsonify(Categories=cs)


@app.route("/test")
def showTest():
    recent_items = session.query(Item).order_by(desc(Item._id)).limit(10).all()
    return render_template("test.html", categories=CATEGORIES_CACHE, recent_items=recent_items)

# Initialize Flask app
if __name__ == "__main__":
    app.secret_key = "super_duper_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
