# Expense Tracker API

A RESTful API built with Flask and SQLite that allows users to manage expenses.

## Features
- Create, read, update, and delete expenses
- Persistent data using SQLite
JSON-bason API endpoint

## Endpoints

GET /expenses
POST /expenses
PUT /expenses/<id>

## Tech Stack
- Python
- Flask
- SQLite

## Example Request

'''json
{
    "title": "Rent",
    "amount": 1200
}