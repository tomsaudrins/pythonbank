from twilio.rest import Client
from flask import jsonify, session
from . import database as db
from datetime import datetime
from uuid import uuid4
import argon2

userAccounts = db.client["bank"]["accounts"]
oneTimePasswordCollection = db.client["bank"]["oneTimePasswords"]
oneTimePasswordCollection.create_index("expires", expireAfterSeconds=300)

client = Client("public_key", "private_key")


def createOneTimePassword(userID):
    """
    Will create a new one time password, update existing one in the database or create a new one if it does not exist already.
    One time password will be valid for 5 minutes (300 seconds).
    Return: Generated one time password for the user (string).
    """
    token = str(uuid4())[:8]
    oneTimePassword = {
        "_id": str(userID),
        "oneTimePassword": argon2.PasswordHasher().hash(token),
        "expires": datetime.now().utcnow(),
    }
    oneTimePasswordCollection.update_one(
        {"_id": str(userID)}, {"$set": oneTimePassword}, upsert=True
    )
    return token


def sendSMS(email):
    """
    Locate user account by email, if the account if found, an SMS containing one time password is sent.
    Return: a JSON object regardless of the status of the user account (found or not).
    """
    userAccount = userAccounts.find_one({"email": email})
    if userAccount:
        oneTimePassword = createOneTimePassword(userAccount["_id"])
        client.messages.create(
            to=f"+45{userAccount['phone_number']}",
            from_="twilio_phone_number",
            body=f'Hi, {userAccount["first_name"]}!\nYou have requested a password reset. Your One Time Password: {oneTimePassword}.',
        )
    return jsonify({"success": "SMS message will be send to your mobile phone number."})
