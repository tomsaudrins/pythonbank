#! /bank/bin/python
from . import database as db
from datetime import datetime
from uuid import uuid4
from flask import request, session, jsonify
import math
accounts = db.client["bank"]["accounts"]

class Transaction:
    def transfer():
        user_current = accounts.find_one({"_id": session["user"]["_id"]})
        user_target = accounts.find_one({"email": request.form.get("email")})
        amount = math.floor(float(request.form.get("amount")) * 100)/100.0

        if user_current == None or user_target == None or user_current == user_target:
            return jsonify({"error": "Could not find recipient"}), 400
        if amount < 0.01:
            return jsonify({"error": "Provide a positive number"}), 400
        if user_current["balance"] < amount:
            return jsonify({"error": "Insufficient balance"}), 400

        transaction_id = Transaction.create_id()
        transaction = {
            "type": "Transfer",
            "sender": f"{user_current['first_name']} {user_current['last_name']}",
            "sender_id": user_current["_id"],
            "receiver": f"{user_target['first_name']} {user_target['last_name']}",
            "receiver_id": user_target["_id"],
            "amount": amount,
            "date": str(datetime.now())[0:-7],
        }
        session.modified = True
        accounts.update_one(
            user_target,
            {
                "$set": {
                    f"transactions.{str(transaction_id)}": transaction
                    | {"end_balance": float(user_target["balance"] + amount)},
                    "balance": float(user_target["balance"] + amount),
                }
            },
        )
        accounts.update_one(
            user_current,
            {
                "$set": {
                    f"transactions.{str(transaction_id)}": transaction
                    | {"end_balance": float(user_current["balance"] - amount)},
                    "balance": float(user_current["balance"] - amount),
                }
            },
        )
        return (
            jsonify(
                {
                    "success": "Money has been transfered succesfully",
                    "transaction": transaction,
                    "id": transaction_id,
                    "new_balance": str(round(user_current["balance"] - amount, 2)),
                }
            ),
            200,
        )

    def calulate_interest(self):
        user = accounts.find_one({"_id": session["user"]["_id"]})
        if user["balance"] < 100:
            return "User does not qualify for interest on their savings"
        quarterly_interest_rate = user["interest_rate"] / 3
        accounts.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "balance": float(
                        user["balance"] + quarterly_interest_rate * user["balance"]
                    ),
                    "interest_earned": float(
                        user["interest_earned"]
                        + quarterly_interest_rate * user["balance"]
                    ),
                }
            },
        )

    @staticmethod
    def create_id():
        return datetime.now().strftime("%Y%m-%d%H-%M%S-") + str(uuid4())
