"""Command-line game store backed by MySQL.

Configure DB_HOST, DB_USER, DB_PASSWORD, DB_NAME and DB_PORT
as environment variables before running this application.
"""

from __future__ import annotations

import os

import mysql.connector
from mysql.connector import Error


def get_connection():
    """Create a MySQL connection using environment-based credentials."""
    required = ("DB_USER", "DB_PASSWORD", "DB_NAME")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "Missing database environment variable(s): " + ", ".join(missing)
        )

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )


def print_games(cursor) -> None:
    cursor.execute(
        "SELECT game_id, name, genre, platform, price, stock "
        "FROM games ORDER BY name"
    )
    rows = cursor.fetchall()

    print("\n--- AVAILABLE GAMES ---")
    if not rows:
        print("No games found.")
        return

    for game in rows:
        print(
            f'ID: {game["game_id"]} | {game["name"]} | '
            f'{game["genre"]} | {game["platform"]} | '
            f'₹{game["price"]} | Stock: {game["stock"]}'
        )


def search_game(cursor) -> None:
    term = input("Enter a game name to search: ").strip()
    if not term:
        print("Search term cannot be empty.")
        return

    cursor.execute(
        "SELECT game_id, name, genre, platform, price, stock "
        "FROM games WHERE name LIKE %s ORDER BY name",
        (f"%{term}%",),
    )
    rows = cursor.fetchall()

    if not rows:
        print("No matching games found.")
        return

    for game in rows:
        print(
            f'ID: {game["game_id"]} | {game["name"]} | '
            f'{game["genre"]} | {game["platform"]} | '
            f'₹{game["price"]} | Stock: {game["stock"]}'
        )


def read_positive_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Enter a whole number.")
            continue
        if value <= 0:
            print("Value must be greater than zero.")
            continue
        return value


def buy_game(connection) -> None:
    """Create a customer and sale, and decrement stock atomically."""
    name = input("Customer name: ").strip()
    email = input("Customer email: ").strip()
    phone = input("Customer phone: ").strip()

    if not name or not email or not phone:
        print("Name, email and phone are required.")
        return

    game_id = read_positive_int("Game ID: ")
    quantity = read_positive_int("Quantity: ")

    cursor = connection.cursor(dictionary=True)
    try:
        # Lock the game row so concurrent purchases cannot oversell it.
        connection.start_transaction()
        cursor.execute(
            "SELECT game_id, name, price, stock FROM games "
            "WHERE game_id = %s FOR UPDATE",
            (game_id,),
        )
        game = cursor.fetchone()

        if game is None:
            connection.rollback()
            print("Game not found.")
            return

        if quantity > game["stock"]:
            connection.rollback()
            print(f'Only {game["stock"]} unit(s) are currently in stock.')
            return

        total_price = game["price"] * quantity

        cursor.execute(
            "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone),
        )
        customer_id = cursor.lastrowid

        cursor.execute(
            "UPDATE games SET stock = stock - %s "
            "WHERE game_id = %s AND stock >= %s",
            (quantity, game_id, quantity),
        )
        if cursor.rowcount != 1:
            raise RuntimeError("Stock changed before the purchase could complete.")

        cursor.execute(
            "INSERT INTO sales "
            "(customer_id, game_id, quantity, total_price, sale_date) "
            "VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)",
            (customer_id, game_id, quantity, total_price),
        )
        sale_id = cursor.lastrowid

        connection.commit()
        print("\nPurchase completed.")
        print(f'Game: {game["name"]}')
        print(f"Quantity: {quantity}")
        print(f"Unit price: ₹{game['price']}")
        print(f"Total: ₹{total_price:.2f}")
        print(f"Customer ID: {customer_id}")
        print(f"Sale ID: {sale_id}")

    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


def view_customers(cursor) -> None:
    cursor.execute(
        "SELECT customer_id, name, email, phone "
        "FROM customers ORDER BY customer_id DESC"
    )
    rows = cursor.fetchall()

    print("\n--- CUSTOMERS ---")
    if not rows:
        print("No customers found.")
        return

    for row in rows:
        print(
            f'{row["customer_id"]} | {row["name"]} | '
            f'{row["email"]} | {row["phone"]}'
        )


def view_sales(cursor) -> None:
    cursor.execute(
        """
        SELECT s.sale_id, c.name AS customer_name, g.name AS game_name,
               s.quantity, s.total_price, s.sale_date
        FROM sales AS s
        JOIN customers AS c ON c.customer_id = s.customer_id
        JOIN games AS g ON g.game_id = s.game_id
        ORDER BY s.sale_date DESC, s.sale_id DESC
        """
    )
    rows = cursor.fetchall()

    print("\n--- SALES ---")
    if not rows:
        print("No sales found.")
        return

    for row in rows:
        print(
            f'{row["sale_id"]} | {row["customer_name"]} | '
            f'{row["game_name"]} | Qty: {row["quantity"]} | '
            f'Total: ₹{row["total_price"]} | {row["sale_date"]}'
        )


def run() -> None:
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        print("Connected to the Game Store database.")

        while True:
            print("\n===== GAME STORE =====")
            print("1. View games")
            print("2. Search games")
            print("3. Buy a game")
            print("4. View customers")
            print("5. View sales")
            print("6. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                print_games(cursor)
            elif choice == "2":
                search_game(cursor)
            elif choice == "3":
                buy_game(connection)
            elif choice == "4":
                view_customers(cursor)
            elif choice == "5":
                view_sales(cursor)
            elif choice == "6":
                print("Thank you for visiting the Game Store.")
                break
            else:
                print("Invalid option. Choose a number from 1 to 6.")

    except (Error, RuntimeError, ValueError) as exc:
        print(f"Application error: {exc}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    run()
