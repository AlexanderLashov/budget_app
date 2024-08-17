from flask import Flask, request, jsonify, render_template
import json
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

app = Flask(__name__)

def load_json(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    transactions = load_json('data/transactions.json')
    transactions.append(data)
    save_json(transactions, 'data/transactions.json')
    return jsonify(success=True)

@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions = load_json('data/transactions.json')
    return render_template('transactions.html', transactions=reversed(transactions))

@app.route('/get_transactions', methods=['POST'])
def get_transactions():
    data = request.json
    transactions = load_json('data/transactions.json')

    if 'from' in data and 'to' in data:
        from_date = datetime.strptime(data['from'], '%Y-%m-%d').date()
        to_date = datetime.strptime(data['to'], '%Y-%m-%d').date()
        transactions = [t for t in transactions if 'date' in t and from_date <= datetime.strptime(t['date'], '%Y-%m-%d').date() <= to_date]

    return jsonify(transactions=transactions)

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    transactions = load_json('data/transactions.json')

    if request.method == 'POST':
        data = request.get_json()
        if 'from' in data and 'to' in data:
            from_date = datetime.strptime(data['from'], '%Y-%m-%d').date()
            to_date = datetime.strptime(data['to'], '%Y-%m-%d').date()
            transactions = [t for t in transactions if 'date' in t and from_date <= datetime.strptime(t['date'], '%Y-%m-%d').date() <= to_date]

    if not transactions:
        fig = px.bar(title="No data available for the selected date range")
        fig.write_html('static/budget_report.html')

        return jsonify({})

    df = pd.DataFrame(transactions)

    df['amount'] = pd.to_numeric(df['amount'])

    budgets = df.groupby('category')['amount'].sum().reset_index()
    budgets.columns = ['category', 'total_amount']

    fig = px.bar(budgets, x='category', y='total_amount')
    fig.write_html('static/budget_report.html')

    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
