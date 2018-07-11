#!/usr/bin/env python2

# Imports for Flask app
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

#TODO: Imports for SQLite DB connection

#TODO: Imports for login_session setup

#TODO: Imports for OAuth setup

app = Flask(__name__)

#TODO: Connect to DB and create DB session

#TODO: Routing for URLs

# Initialize Flask app
if __name__ == "__main__":
    app.secret_key = "super_duper_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)


