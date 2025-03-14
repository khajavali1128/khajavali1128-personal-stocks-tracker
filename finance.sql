#PRAGMA foreign_keys=OFF;
START TRANSACTION;

DROP TABLE IF EXISTS portfolio;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);

INSERT INTO users (id, username, hash, cash) VALUES
(32, 'khaja', 'scrypt:32768:8:1$AqGa63UZo7iY1K5n$296b1946089292708d0ea723c690371ad0fec95e3dc5a11cfd2d82556debd664cd4196b07122618c2a71dc830bb0ff6ffbe82db11712976eca8ed2a8655c4250', 3308.34),
(33, '343', 'scrypt:32768:8:1$0ktYQGm0G1I2uqld$370dbb7f1668eeebae850284be12438cd54acc71475ca0b3604929b421aed9706ab5c4f3a02fe7c1f8a73be78240c7f139923fa4d26dc4f15d701f34e56b24b9', 10000);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    total_price NUMERIC NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

INSERT INTO transactions (id, user_id, symbol, shares, price, total_price, timestamp, type) VALUES
(59, 32, 'AAPL', 10, 222.34, 2223.40, '2024-11-15 01:53:46', NULL),
(60, 32, 'NFLX', 10, 666.81, 6668.10, '2024-11-15 01:53:55', NULL),
(61, 32, 'GOOGL', 5, 151.61, 758.05, '2024-11-15 01:54:13', NULL),
(62, 32, 'AAPL', 1, 221.11, 221.11, '2024-11-15 01:54:23', NULL),
(63, 32, 'AAPL', 1, 220.64, 220.64, '2024-11-15 01:54:52', 'SELL'),
(64, 32, 'AAPL', 1, 220.65, 220.65, '2024-11-15 01:55:00', NULL),
(65, 32, 'FAMI', 100, 0.2, 20, '2024-11-15 01:55:17', NULL),
(66, 32, 'AAPL', 3, 221.74, 665.22, '2024-11-15 01:56:38', 'SELL'),
(67, 32, 'NFLX', 10, 668.40, 6684, '2024-11-15 01:56:49', 'SELL'),
(68, 32, 'AAPL', 8, 221.38, 1771.04, '2024-11-15 01:57:01', 'SELL'),
(69, 32, 'GOOGL', 5, 151.77, 758.85, '2024-11-15 01:57:08', 'SELL'),
(70, 32, 'FAMI', 100, 0.2, 20, '2024-11-15 01:57:14', 'SELL'),
(71, 32, 'NFLX', 10, 666.52, 6665.20, '2024-11-15 02:43:40', 'BUY'),
(72, 32, 'NFLX', 3, 670.96, 2012.88, '2024-11-15 02:46:13', 'BUY'),
(73, 32, 'NFLX', 13, 665.36, 8649.68, '2024-11-15 02:54:57', 'SELL'),
(74, 32, 'NFLX', 10, 667.17, 6671.70, '2024-11-15 05:13:36', 'BUY');

CREATE TABLE portfolio (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    company_name TEXT NOT NULL,
    shares INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

INSERT INTO portfolio (id, user_id, symbol, company_name, shares) VALUES
(29, 32, 'NFLX', 'Netflix Inc. Common Stock', 10);

COMMIT;
