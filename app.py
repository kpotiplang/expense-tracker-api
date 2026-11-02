from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///expenses.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    date = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }


# Create tables at import time so this also works under a production server
# like gunicorn, not only when running `python app.py`.
with app.app_context():
    db.create_all()


def validate_expense(data, partial=False):
    """Return an error message if the payload is invalid, otherwise None.

    partial=True is used for updates, where every field is optional.
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    if not partial:
        for field in ("title", "amount"):
            if field not in data:
                return f"Missing required field: {field}"

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return "title must be a non-empty string"
        if len(data["title"]) > 100:
            return "title must be 100 characters or fewer"

    if "amount" in data:
        # bool is a subclass of int in Python, so exclude it explicitly
        if isinstance(data["amount"], bool) or not isinstance(data["amount"], (int, float)):
            return "amount must be a number"
        if data["amount"] <= 0:
            return "amount must be greater than 0"

    return None


@app.route("/")
def home():
    return "Expense Tracker API is running"


@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([expense.to_dict() for expense in expenses])


@app.route("/expenses/<int:id>", methods=["GET"])
def get_expense(id):
    expense = db.session.get(Expense, id)

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify(expense.to_dict())


@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json(silent=True)
    error = validate_expense(data)
    if error:
        return jsonify({"error": error}), 400

    new_expense = Expense(
        title=data["title"].strip(),
        amount=data["amount"],
        category=data.get("category"),
        date=data.get("date")
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify(new_expense.to_dict()), 201


@app.route("/expenses/<int:id>", methods=["PUT"])
def update_expense(id):
    expense = db.session.get(Expense, id)

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    data = request.get_json(silent=True)
    error = validate_expense(data, partial=True)
    if error:
        return jsonify({"error": error}), 400

    expense.title = data.get("title", expense.title).strip()
    expense.amount = data.get("amount", expense.amount)
    expense.category = data.get("category", expense.category)
    expense.date = data.get("date", expense.date)

    db.session.commit()
    return jsonify(expense.to_dict())


@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    expense = db.session.get(Expense, id)

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Expense deleted"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
