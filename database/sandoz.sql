-- Crear la base de datos si no existe
CREATE DATABASE sandoz;

-- Conectar a la base de datos
\c sandoz;

-- Crear tablas si no existen
-- Continets
CREATE TABLE IF NOT EXISTS continents (
    code CHAR(2) NOT NULL,
    name VARCHAR(255),
    PRIMARY KEY (code)
);

-- Countries ISO 3166-1 alpha-2 codes and names
CREATE TABLE countries (
    code CHAR(2) NOT NULL,
    continent_code CHAR(2) NOT NULL,
    name VARCHAR(255) NOT NULL,
    iso3 CHAR(3) NOT NULL,
    number CHAR(3) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (code),
    CONSTRAINT fk_countries_continents FOREIGN KEY (continent_code)
    REFERENCES continents (code)
);

-- Create table for month calendar
CREATE TABLE month_calendar (
	yyyymm INT NOT NULL,
	month_number INT NOT NULL,
	month_name VARCHAR(9) NOT NULL,
	month_name_abbr CHAR(3) NOT NULL,
	quarter_number INT NOT NULL,
	quarter_name VARCHAR(9) NOT NULL,
	"year" VARCHAR
);

ALTER TABLE month_calendar ADD CONSTRAINT month_calendar_pk PRIMARY KEY (yyyymm);

-- Contains historical data about volumes and net sales
CREATE TABLE IF NOT EXISTS monthly_balance (
    month INTEGER,
    market VARCHAR(2),
    bu VARCHAR(5),
    volume NUMERIC(10, 2),
    value NUMERIC(18, 2),
    CONSTRAINT fk_market FOREIGN KEY (market) REFERENCES countries (code)
);

ALTER TABLE monthly_balance ADD CONSTRAINT fk_month FOREIGN KEY (month) REFERENCES month_calendar (yyyymm);

COMMENT ON COLUMN monthly_balance.month IS 'The month of the sales data, formatted as YYYYMM';
COMMENT ON COLUMN monthly_balance.market IS 'The id of the country representing the market (e.g., US, DE, IT)';
COMMENT ON COLUMN monthly_balance.bu IS 'The bussiness unit identifier (GN_BP for biosimilars, GN_RE for retail)';
COMMENT ON COLUMN monthly_balance.volume IS 'The volume of sales in the specified month, region, market, and business unit';
COMMENT ON COLUMN monthly_balance.value IS 'The monetary value of sales (net) in the specified month, region, market, and business unit';

-- Contains planning data about net sales
CREATE TABLE IF NOT EXISTS monthly_lo (
    month INTEGER,
    market VARCHAR(2),
    bu VARCHAR(5),
    value DECIMAL(18, 2),
    CONSTRAINT fk_market FOREIGN KEY (market) REFERENCES countries (code)
);

ALTER TABLE monthly_lo ADD CONSTRAINT fk_month FOREIGN KEY (month) REFERENCES month_calendar (yyyymm);

COMMENT ON COLUMN monthly_lo.month IS 'The month of the sales data, formatted as YYYYMM';
COMMENT ON COLUMN monthly_lo.market IS 'The id of the country representing the market (e.g., US, DE, IT)';
COMMENT ON COLUMN monthly_lo.bu IS 'The bussiness unit identifier (GN_BP for biosimilars, GN_RE for retail)';
COMMENT ON COLUMN monthly_lo.value IS 'The planned monetary value of sales (net) in the specified month, region, market, and business unit';

-- Market mapping
CREATE TABLE IF NOT EXISTS market_mapping (
    market VARCHAR(10),
    market_des VARCHAR(50),
    cluster VARCHAR(50),
    region VARCHAR(50)
);

-- Cargar datos desde archivos CSV
COPY continents FROM '/app/sql/data/continents.csv' DELIMITER ',' CSV HEADER;
COPY countries FROM '/app/sql/data/countries.csv' DELIMITER ',' CSV HEADER;
COPY month_calendar FROM '/app/sql/data/sample-month_calendar.csv' DELIMITER ',' CSV HEADER;
COPY monthly_balance FROM '/app/sql/data/sample-monthly_balance.csv' DELIMITER ',' CSV HEADER;
COPY monthly_lo FROM '/app/sql/data/sample-monthly_lo.csv' DELIMITER ',' CSV HEADER;
COPY market_mapping FROM '/app/sql/data/sample-market_mapping.csv' DELIMITER ',' CSV HEADER;

