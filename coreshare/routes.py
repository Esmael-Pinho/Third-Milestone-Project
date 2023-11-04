import datetime
from flask import flash, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from coreshare import app, db
from coreshare.model import User


@app.route("/")
def home():
    return render_template("base.html")

