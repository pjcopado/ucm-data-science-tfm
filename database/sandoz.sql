-- Crear la base de datos si no existe
CREATE DATABASE sandoz;

-- Conectar a la base de datos
\c sandoz;

-- Crear tablas si no existen
CREATE TABLE IF NOT EXISTS monthly_balance (
    month VARCHAR(6),
    market VARCHAR(10),
    bu VARCHAR(20),
    volume FLOAT,
    value FLOAT
);

CREATE TABLE IF NOT EXISTS monthly_lo (
    month VARCHAR(6),
    market VARCHAR(10),
    bu VARCHAR(20),
    value FLOAT
);

CREATE TABLE IF NOT EXISTS market_mapping (
    market VARCHAR(10),
    market_des VARCHAR(50),
    cluster VARCHAR(50),
    region VARCHAR(50)
);

-- Cargar datos desde archivos CSV
COPY monthly_balance FROM '/app/sql/data/sample-monthly_balance.csv' DELIMITER ',' CSV HEADER;
COPY monthly_lo FROM '/app/sql/data/sample-monthly_lo.csv' DELIMITER ',' CSV HEADER;
COPY market_mapping FROM '/app/sql/data/sample-market_mapping.csv' DELIMITER ',' CSV HEADER;

