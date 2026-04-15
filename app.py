from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount
        }


@app.route("/")
def home():
    return "Expense Tracker API is running"


@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([expense.to_dict() for expense in expenses])


@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()

    new_expense = Expense(
        title=data["title"],
        amount=data["amount"]
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify(new_expense.to_dict()), 201


@app.route("/expenses/<int:id>", methods=["PUT"])
def update_expense(id):
    expense = Expense.query.get(id)

    if not expense:
        return jsonify({"error": "Expense Expense not found"}), 404

    data = request.get_json()
    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)

    db.session.commit()
    return jsonify(expense.to_dict())


@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.get(id)

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Expense deleted"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
