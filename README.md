# Budget App

This is a simple budget recording application. It allows users to keep track of their spendings by adding transactions with details such as category, date, amount, and description.

## Features

- **Add Transactions**: Users can add their spendings with details like category, date, amount, and description.
- **View Transactions**: Users can view a table of all their transactions. This table can be filtered by date.
- **Reports**: Users can view a bar graph report of their transactions grouped by category. This report can also be filtered by date.
- **Local Storage**: All data is stored locally in a JSON file. This makes the app easily scalable to a database if needed.

## Usage

To run the app, execute the `run.sh` script. Once the app is running, it can be accessed via a web browser at `http://127.0.0.1:5000`.

## Default View

By default, before any filtering, the transactions table and the report display the full record of transactions.

## Scalability

The app is designed with scalability in mind. The data is currently stored in a JSON file, but the structure allows for easy transition to a database if needed in the future.