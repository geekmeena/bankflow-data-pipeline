CREATE TABLE transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    date DATE,
    amount NUMERIC(12,2),
    currency VARCHAR(3),
    transaction_type VARCHAR(10),
    category VARCHAR(50)
);

SELECT COUNT(*) FROM transactions;

SELECT * FROM transactions;

SELECT customer_id, SUM(amount) AS total_spending
FROM transactions
WHERE transaction_type = 'Debit'
GROUP BY customer_id;

SELECT customer_id, SUM(amount) AS total_spending
FROM transactions
WHERE transaction_type = 'Debit'
GROUP BY customer_id
ORDER BY total_spending DESC;

SELECT category, SUM(amount) AS total_spending
FROM transactions
WHERE transaction_type = 'Debit'
GROUP BY category
ORDER BY total_spending DESC;

SELECT category, COUNT(*) AS total_transactions
FROM transactions
WHERE transaction_type = 'Debit'
GROUP BY category
ORDER BY total_transactions DESC;

SELECT ROUND(AVG(amount), 2) AS average_spending
FROM transactions
WHERE transaction_type = 'Debit';