SELECT
    customer_id,
    SUM(amount) AS total_spending
FROM public.transactions
WHERE transaction_type = 'Debit'
GROUP BY customer_id