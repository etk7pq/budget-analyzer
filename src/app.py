from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

#Configure logging
logging.basicConfig(level=logging.INFO)

#In-memory storage
expenses_data = []

@app.route("/health", methods=["GET"])
def health():
	return jsonify({"status": "ok"}), 200

@app.route("/upload", methods=["POST"])
def upload():
	data = request.get_json()
	if not data or "income" not in data:
		return jsonify({"error": "Invalid input"}), 400

	expenses_data.append(data)
	logging.info(f"Uploaded expenses: {data}")
	return jsonify({"message": "Expenses uploaded successfully"}), 201

@app.route("/summary", methods=["GET"])
def summary():
	if not expenses_data:
		return jsonify({"error": "No data uploaded"}), 400

	latest = expenses_data[-1]
	income = latest.get("income", 0)
	total_expenses = sum(v for k, v in latest.items() if k != "income")
	savings = income - total_expenses
	savings_rate = round((savings / income) * 100, 2) if income > 0 else 0
	largest_expense = max(
		((k,v) for k, v in latest.items() if k != "income"),
		key=lambda x: x[1],
		default=("none", 0)
	)

	return jsonify({
		"income": income,
		"total_expenses": total_expenses,
		"savings": savings,
		"savings_rate": savings_rage,
		"largest_expense": largest_expense[0]
	})

@app.route("/forecast", methods=["GET"])
def forecast():
	if not expenses_data:
		return jsonify({"error": "No data uploaded"}), 400

	latest = expenses_data[-1]
	total+expenses = sum(v for k, v in latest.items() if k != "income")

	#Current inflation rate: 3% per year
	inflation_rate = 0.03
	forecast = {}
	year = 2026
	for i in range(5):
		total_expenses *= (1 + inflation_rate)
		forecast[year + i] = round(total_expenses, 2)

	return jsonify({"inflation_forecast": forecast})

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8080))
	app.run(host="0.0.0.0", port=port)
