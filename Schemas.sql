-- Products table schema
CREATE TABLE Products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name text NOT NULL,
    cost REAL
);

-- Discounts table schema
CREATE TABLE Discounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coupon_code text NOT NULL,
    discount_percentage REAL NOT NULL
);