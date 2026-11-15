# Game Store Management System

A command-line game store application built with Python and MySQL. It supports browsing and searching a game catalogue, recording purchases, updating inventory, and viewing customer and sales records.

## Features

- View available games, prices and stock
- Search games by name
- Record a purchase and customer details
- Calculate purchase totals
- Decrease inventory after a successful purchase
- View customer and sales records
- Parameterized SQL queries
- A database transaction for each purchase, so customer creation, stock update and sale recording commit or roll back together

## Tech stack

- Python 3
- MySQL
- mysql-connector-python

## Project files

- game_store.py — application entry point and menu
- schema.sql — database and table definitions, plus optional sample games
- .env.example — example database environment variables
- requirements.txt — Python dependency

## Setup

### 1. Create the database

Open MySQL Workbench or the MySQL command line and run the statements in schema.sql.

If you already have a game_store database, compare its tables with the schema before running the script. The application expects these columns:

- games(game_id, name, genre, platform, price, stock)
- customers(customer_id, name, email, phone)
- sales(sale_id, customer_id, game_id, quantity, total_price, sale_date)

The schema uses InnoDB so purchase transactions and row locking are supported. It also defines customer_id and sale_id as AUTO_INCREMENT primary keys; the application relies on MySQL generating these IDs. If you already created the tables with different definitions, migrate or recreate them to match before running this version.

### 2. Install the dependency

    python -m pip install -r requirements.txt

### 3. Configure database credentials

.env.example is a reference template only; the application reads environment variables and does not load a .env file automatically. Set the variables in your terminal before running.

Windows PowerShell:

    $env:DB_HOST="localhost"
    $env:DB_PORT="3306"
    $env:DB_USER="root"
    $env:DB_PASSWORD="your_mysql_password"
    $env:DB_NAME="game_store"
    python game_store.py

macOS / Linux:

    export DB_HOST="localhost"
    export DB_PORT="3306"
    export DB_USER="root"
    export DB_PASSWORD="your_mysql_password"
    export DB_NAME="game_store"
    python game_store.py

## Purchase workflow

1. Choose View games to find a game ID.
2. Choose Buy a game.
3. Enter customer details, game ID and quantity.
4. The application locks the selected game row, checks stock, records the customer and sale, and updates inventory in one transaction.
5. If a database operation fails, the purchase is rolled back.

## Scope and limitations

This is a local, terminal-based learning project. It does not include a graphical interface, user authentication, payment processing, an online storefront, or production deployment. Use test data during demonstrations.

The originally uploaded scripts contained a hard-coded database password and a variable-name error in one file. This version removes embedded credentials and consolidates the flow into one maintainable application.
