-- Nessie branching demo for isolated development and promotion to main.
-- Assumes catalog name `local` and default branch `main`.
-- Run statements in order.

-- 1) Inspect current references.
SHOW REFERENCES IN local;

-- 2) Create an isolated development branch from main.
CREATE BRANCH IF NOT EXISTS dev IN local FROM main;

-- 3) Switch context to the dev branch.
USE REFERENCE dev IN local;

-- 4) Create or update data in isolation on dev.
CREATE NAMESPACE IF NOT EXISTS local.demo;

CREATE TABLE IF NOT EXISTS local.demo.orders_branching (
    order_id BIGINT,
    status STRING,
    amount DECIMAL(12, 2),
    currency STRING
) USING iceberg;

INSERT OVERWRITE local.demo.orders_branching VALUES
    (1000, 'created', 15.00, 'EUR'),
    (1001, 'created', 25.00, 'EUR');

UPDATE local.demo.orders_branching
SET status = 'updated', amount = 27.00
WHERE order_id = 1001;

SELECT *
FROM local.demo.orders_branching
ORDER BY order_id;

-- 5) Confirm main still does not include dev changes.
USE REFERENCE main IN local;

SELECT *
FROM local.demo.orders_branching
ORDER BY order_id;

-- 6) Promote validated dev changes into main.
MERGE BRANCH dev INTO main IN local;

-- 7) Validate merged state in main.
USE REFERENCE main IN local;

SELECT *
FROM local.demo.orders_branching
ORDER BY order_id;

-- 8) Optional cleanup once branch is no longer needed.
DROP BRANCH IF EXISTS dev IN local;
