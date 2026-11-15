CREATE DATABASE IF NOT EXISTS game_store;
USE game_store;

CREATE TABLE IF NOT EXISTS games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    genre VARCHAR(80) NOT NULL,
    platform VARCHAR(80) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    CONSTRAINT chk_games_price CHECK (price >= 0),
    CONSTRAINT chk_games_stock CHECK (stock >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(40) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    game_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL,
    sale_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_sales_game
        FOREIGN KEY (game_id) REFERENCES games(game_id),
    CONSTRAINT chk_sales_quantity CHECK (quantity > 0),
    CONSTRAINT chk_sales_total CHECK (total_price >= 0)
) ENGINE=InnoDB;

-- Optional sample data. The inserts only add a game if its name is absent.
INSERT INTO games (name, genre, platform, price, stock)
SELECT 'The Witcher 3', 'RPG', 'PC', 999.00, 12
WHERE NOT EXISTS (SELECT 1 FROM games WHERE name = 'The Witcher 3');

INSERT INTO games (name, genre, platform, price, stock)
SELECT 'Red Dead Redemption 2', 'Action Adventure', 'PC', 1499.00, 8
WHERE NOT EXISTS (SELECT 1 FROM games WHERE name = 'Red Dead Redemption 2');

INSERT INTO games (name, genre, platform, price, stock)
SELECT 'FIFA 25', 'Sports', 'PC', 2999.00, 10
WHERE NOT EXISTS (SELECT 1 FROM games WHERE name = 'FIFA 25');
