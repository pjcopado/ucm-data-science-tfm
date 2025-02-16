import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Set the root directory to import own modules
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

from project.modules.postgres import Postgres  # noqa: E402


@pytest.fixture
def db_config():
    return {
        "dbname": "test_db",
        "user": "test_user",
        "password": "test_password",
        "host": "localhost",
    }


@pytest.fixture
def postgres(db_config):
    return Postgres(db_config)


def test_get_db_schema(postgres):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("continents", "code"),
        ("continents", "name"),
        ("countries", "code"),
        ("countries", "name"),
        ("countries", "full_name"),
        ("countries", "iso3"),
        ("countries", "number"),
        ("countries", "continent_code"),
        ("monthly_lo", "month"),
        ("monthly_lo", "market"),
        ("monthly_lo", "bu"),
        ("monthly_lo", "value"),
        ("monthly_sales", "month"),
        ("monthly_sales", "market"),
        ("monthly_sales", "bu"),
        ("monthly_sales", "volume"),
        ("monthly_sales", "value"),
    ]

    with patch("psycopg2.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        schema = postgres.get_db_schema()

    expected_schema = {
        "continents": ["code", "name"],
        "countries": ["code", "name", "full_name", "iso3", "number", "continent_code"],
        "monthly_lo": ["month", "market", "bu", "value"],
        "monthly_sales": ["month", "market", "bu", "volume", "value"],
    }

    assert schema == expected_schema


@pytest.mark.skip(reason="Ignoring this test")
def test_get_db_schema_and_relationships(postgres):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.side_effect = [
        [
            ("continents", "code", "character", ""),
            ("continents", "name", "character varying", ""),
            ("countries", "code", "character", ""),
            ("countries", "name", "character varying", ""),
            ("countries", "full_name", "character varying", ""),
            ("countries", "iso3", "character", ""),
            ("countries", "number", "character", ""),
            ("countries", "continent_code", "character", ""),
            ("monthly_lo", "month", "integer", "The month of the sales data, formatted as YYYYMM"),
            ("monthly_lo", "market", "character varying", "The id of the country representing the market (e.g., US, DE, IT)"),
            ("monthly_lo", "bu", "character varying", "The bussiness unit identifier (GN_BP for biosimilars, GN_RE for retail)"),
            ("monthly_lo", "value", "numeric", "The planned monetary value of sales (net) in the specified month, region, market, and business unit"),
            ("monthly_sales", "month", "integer", "The month of the sales data, formatted as YYYYMM"),
            ("monthly_sales", "market", "character varying", "The id of the country representing the market (e.g., US, DE, IT)"),
            ("monthly_sales", "bu", "character varying", "The bussiness unit identifier (GN_BP for biosimilars, GN_RE for retail)"),
            ("monthly_sales", "volume", "numeric", "The volume of sales in the specified month, region, market, and business unit"),
            ("monthly_sales", "value", "numeric", "The monetary value of sales (net) in the specified month, region, market, and business unit"),
        ],
        [
            ("fk_countries_continents", "countries", "continent_code", "continents", "code"),
            ("fk_market", "monthly_lo", "market", "countries", "code"),
            ("fk_market", "monthly_lo", "market", "countries", "code"),
            ("fk_market", "monthly_lo", "market", "countries", "code"),
            ("fk_market", "monthly_lo", "market", "countries", "code"),
            ("fk_market", "monthly_sales", "market", "countries", "code"),
            ("fk_market", "monthly_sales", "market", "countries", "code"),
            ("fk_market", "monthly_sales", "market", "countries", "code"),
            ("fk_market", "monthly_sales", "market", "countries", "code"),
        ]
    ]

    with patch("psycopg2.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        db_schema_and_relationships = postgres.get_db_schema_and_relationships()

    print(db_schema_and_relationships)
    expected_db_schema_and_relationships = (
        "Table: continents\n"
        "  - code: character - Column description:\n"
        "  - name: character varying - Column description:\n"
        "Table: countries\n"
        "  - code: character - Column description:\n"
        "  - name: character varying - Column description:\n"
        "  - full_name: character varying - Column description:\n"
        "  - iso3: character - Column description:\n"
        "  - number: character - Column description:\n"
        "  - continent_code: character - Column description:\n"
        "Table: monthly_lo\n"
        "  - month: integer - Column description: The month of the sales data, formatted as YYYYMM\n"
        "  - market: character varying - Column description: The id of the country representing the market (e.g., US, DE, IT)\n"
        "  - bu: character varying - Column description: The bussiness unit identifier (GN_BP for biosimilars, GN_RE for retail)\n"
        "  - value: numeric - Column description: The planned monetary value of sales (net) in the specified month, region, market, and business unit\n"
        "Table: monthly_sales\n"
        "  - month: integer - Column description: The month of the sales data, formatted as YYYYMM\n"
        "  - market: character varying - Column description: The id of the country representing the market (e.g., US, DE, IT)\n"
        "  - bu: character varying - Column description: The bussiness unit identifier (GN_BP for biosimilars, GN_RE for retail)\n"
        "  - volume: numeric - Column description: The volume of sales in the specified month, region, market, and business unit\n"
        "  - value: numeric - Column description: The monetary value of sales (net) in the specified month, region, market, and business unit\n\n"
        "Table relationships (Foreign Keys):\n"
        "  - fk_countries_continents: countries(continent_code) -> continents(code)\n"
        "  - fk_market: monthly_lo(market) -> countries(code)\n"
        "  - fk_market: monthly_lo(market) -> countries(code)\n"
        "  - fk_market: monthly_lo(market) -> countries(code)\n"
        "  - fk_market: monthly_lo(market) -> countries(code)\n"
        "  - fk_market: monthly_sales(market) -> countries(code)\n"
        "  - fk_market: monthly_sales(market) -> countries(code)\n"
        "  - fk_market: monthly_sales(market) -> countries(code)\n"
        "  - fk_market: monthly_sales(market) -> countries(code)\n"
    )

    print(expected_db_schema_and_relationships)
    assert db_schema_and_relationships == expected_db_schema_and_relationships