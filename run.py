#! /bank/bin/python
import os
import models.database as db
import models.resetPassword as sms
from models.User import User
from models.Transaction import Transaction
from flask import Flask, render_template, request, redirect, session
from flask_wtf.csrf import CSRFProtect
from functools import wraps

csrf = CSRFProtect()
user_accounts = db.client["bank"]["accounts"]
template_dir = os.path.abspath("ui/templates")
app = Flask(__name__, template_folder=template_dir)
CSRFProtect(app)
app.secret_key = b"\xc4\xf8\x9d\xa8\xf7\xbc\t \x8f\xb6l\xea\xc5H\xfet"
app.static_url_path = "/ui/static"
app.static_folder = app.root_path + app.static_url_path
csrf.init_app(app)


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return redirect("/dashboard")
        else:
            return f(*args, **kwargs)

    return wrap

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")

    return wrap

@app.route("/")
@is_logged_in
def index():
    return render_template("index.html")


@app.route("/transfers/send", methods=["GET", "POST"])
def transaction_send():
    return Transaction.transfer()


@app.route("/transactions/<page_id>", methods=["GET"])
def overview_details(page_id):
    output = []
    current_user = user_accounts.find_one({"_id":session["user"]["_id"]})
    transaction = current_user["transactions"][page_id]
    target_user = (
        transaction["receiver_id"]
        if current_user["_id"]
        == transaction["sender_id"]
        else transaction["sender_id"]
    )
    for _, details in current_user["transactions"].items():
        if details == transaction:
            continue
        if (details["receiver_id"] == target_user and details["sender_id"] == current_user["_id"]) or (details["receiver_id"] == current_user["_id"] and details["sender_id"] == target_user):
            output.append(details)
    return render_template(
        "transaction.html", transaction=transaction, transactions=output
    )


@app.route("/user/login", methods=["GET", "POST"])
@is_logged_in
def user_login():
    if request.method == "POST":
        return User().login()
    return render_template("login.html")


@app.route("/user/register", methods=["GET", "POST"])
@is_logged_in
def user_register():
    if request.method == "POST":
        return User().signup()
    return render_template("register.html")


@app.route("/user/signout")
def user_signout():
    return User().signout()


@app.route("/user/reset", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        return sms.sendSMS(request.form.get("email"))
    return render_template("reset.html")

@app.route("/user/changepassword", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        return User().change_password(session["user"]["_id"], request.form.get("password"), request.form.get("password_confirmation"))
    return render_template("changePassword.html")

@app.route("/dashboard/")
@login_required
def display_dashboard():
    transactions = user_accounts.aggregate([{ "$match": { "_id": session["user"]["_id"] }}, {"$project": { "subDocument": { "$objectToArray": "$transactions" } }},{"$unwind":'$subDocument'}, {"$sort":{"subDocument.v.date":-1}},{"$limit":5 }, 
    {"$project": {"id": "$subDocument.k","type":"$subDocument.v.type","sender":"$subDocument.v.sender", "receiver":"$subDocument.v.receiver", "date":"$subDocument.v.date", "amount":"$subDocument.v.amount"}}])
    overview_details = User().get_overview(session["user"]["_id"])
    return render_template(
        "dashboard.html",
        user_id=session["user"]["first_name"] + " " + session["user"]["last_name"],
        balance=user_accounts.find_one({"_id": str(session["user"]["_id"])})["balance"],
        income=overview_details[1],
        expenses=overview_details[2],
        transactions=list(transactions)
    )