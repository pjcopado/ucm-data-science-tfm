import os
import sys
import pytest
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set the root directory to import own modules
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

from project.modules.prompt_loader import PromptLoader  # noqa
from project.modules.sql_generator import SQLQueryGenerator  # noqa
from project.modules.postgres import Postgres  # noqa


class TestSQLQueryGenerator:
    @pytest.fixture(autouse=True)
    def setup_class(self):

        # Setup the database connection
        self.db_config = {
            "host": "localhost",
            "port": 5432,
            "database": "sandoz",
            "user": "postgres",
            "password": "postgres"
        }
        postgres_db = Postgres(self.db_config)
        self.database_schema = postgres_db.get_db_schema_and_relationships()

        # Load the model and tokenizer from the local directory
        model_dir = os.path.join(
            root_dir,
            "project",
            "models",
            "llama-3-sqlcoder-8b")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir)

        # Prompt loader
        prompt_dir = os.path.join(root_dir, "project", "prompts")
        self.prompt_loader = PromptLoader(prompt_dir=prompt_dir)
        self.prompt_file = "prompt_generate_sql.txt"
        self.retry_prompt_file = "prompt_generate_sql_error.txt"

        # SQL Query Generator
        self.sql_generator = SQLQueryGenerator(
            model=self.model,
            tokenizer=self.tokenizer,
            prompt_loader=self.prompt_loader,
            max_attempts=3
        )

    def test_generate_sql_query_1(self):
        user_input = "How many years of historical data do we have available for Spain?"
        instructions = None
        expected_result = "SELECT COUNT(*) FROM monthly_sales WHERE country = 'Spain';"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_2(self):
        user_input = "How many years of historical data do we have available for the south cluster of Europe?"
        instructions = None
        expected_result = "SELECT COUNT(*) FROM monthly_sales WHERE region = 'south cluster of Europe';"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_3(self):
        user_input = "What is the oldest data for which we have sales in Spain?"
        instructions = None
        expected_result = "SELECT MIN(month) FROM monthly_sales WHERE country = 'Spain';"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_4(self):
        user_input = "In which countries did we sell products in 2023?"
        instructions = None
        expected_result = "SELECT DISTINCT country FROM monthly_sales WHERE year = 2023;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_5(self):
        user_input = "What were the sales in Germany in August 2021?"
        instructions = None
        expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE country = 'Germany' AND month = 'August' AND year = 2021;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_6(self):
        user_input = "What were the sales in Europe in 2023?"
        instructions = None
        expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE region = 'Europe' AND year = 2023;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_7(self):
        user_input = "What were the sales in North America in 2023?"
        instructions = None
        expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE region = 'North America' AND year = 2023;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_8(self):
        user_input = "What was the demand in Italy in 2022?"
        instructions = None
        expected_result = "SELECT SUM(demand) FROM monthly_sales WHERE country = 'Italy' AND year = 2022;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_9(self):
        user_input = "What was the demand in bio in Germany in August 2021?"
        instructions = None
        expected_result = "SELECT SUM(demand) FROM monthly_sales WHERE category = 'bio' AND country = 'Germany' AND month = 'August' AND year = 2021;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_10(self):
        user_input = "How many units were sold in bio in Germany in August 2021?"
        instructions = None
        expected_result = "SELECT SUM(units_sold) FROM monthly_sales WHERE category = 'bio' AND country = 'Germany' AND month = 'August' AND year = 2021;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_11(self):
        user_input = "What was the month with higher demand in North America in 2022?"
        instructions = None
        expected_result = "SELECT month FROM monthly_sales WHERE region = 'North America' AND year = 2022 ORDER BY demand DESC LIMIT 1;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_12(self):
        user_input = "What were the total bio sales in 2022?"
        instructions = None
        expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE category = 'bio' AND year = 2022;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_13(self):
        user_input = "And the total retail sales that same year?"
        instructions = None
        expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE category = 'retail' AND year = 2022;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_14(self):
        user_input = "What were the sales in Spain in 2022?"
        instructions = None
        expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE country = 'Spain' AND year = 2022;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_15(self):
        user_input = "What were the sales in the spanish market in 2022?"
        instructions = None
        expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE market = 'spanish' AND year = 2022;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_16(self):
        user_input = "What were the sales in the spanish market 2 years ago?"
        instructions = None
        expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE market = 'spanish' AND year = (CURRENT_YEAR - 2);"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_17(self):
        user_input = "What was the total growth in sales Canada in 2023?"
        instructions = None
        expected_result = "SELECT SUM(growth) FROM monthly_sales WHERE country = 'Canada' AND year = 2023;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_18(self):
        user_input = "And the growth per business unit in 2023?"
        instructions = None
        expected_result = "SELECT business_unit, SUM(growth) FROM monthly_sales WHERE year = 2023 GROUP BY business_unit;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_19(self):
        user_input = "And the growth per business unit that same year?"
        instructions = None
        expected_result = "SELECT business_unit, SUM(growth) FROM monthly_sales WHERE year = 2023 GROUP BY business_unit;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_20(self):
        user_input = "Which european market had a higher growth in sales 2023 in bio?"
        instructions = None
        expected_result = "SELECT market FROM monthly_sales WHERE region = 'Europe' AND category = 'bio' AND year = 2023 ORDER BY growth DESC LIMIT 1;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_21(self):
        user_input = "And in north america?"
        instructions = None
        expected_result = "SELECT market FROM monthly_sales WHERE region = 'North America' AND year = 2023 ORDER BY growth DESC LIMIT 1;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_22(self):
        user_input = "What about retail? Which was the market with higher growth in 2022 in bio?"
        instructions = None
        expected_result = "SELECT market FROM monthly_sales WHERE category = 'bio' AND year = 2022 ORDER BY growth DESC LIMIT 1;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_23(self):
        user_input = "In which months from 2023 did we see a positive growth in demand versus the previous year?"
        instructions = None
        expected_result = "SELECT month FROM monthly_sales WHERE year = 2023 AND growth > 0;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_24(self):
        user_input = "In which months from 2023 did we see a growth in demand versus the previous year?"
        instructions = None
        expected_result = "SELECT month FROM monthly_sales WHERE year = 2023 AND growth > 0;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_25(self):
        user_input = "How accurate was the LO for United States in April 2023?"
        instructions = None
        expected_result = "SELECT accuracy FROM monthly_lo WHERE country = 'United States' AND month = 'April' AND year = 2023;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_26(self):
        user_input = "What is the LO for total Spain 2024?"
        instructions = None
        expected_result = "SELECT lo FROM monthly_lo WHERE country = 'Spain' AND year = 2024;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_27(self):
        user_input = "What is the number of the planned sales for total Spain 2024?"
        instructions = None
        expected_result = "SELECT planned_sales FROM monthly_lo WHERE country = 'Spain' AND year = 2024;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_28(self):
        user_input = "How good was the LO vs the sales last month?"
        instructions = None
        expected_result = ""

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_29(self):
        user_input = "What was the percentage of accuracy of the LO in may 2023 in the US?"
        instructions = None
        expected_result = ""

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_30(self):
        user_input = "What was the percentage of accuracy of the LO in 2023 in the US?"
        instructions = None
        expected_result = ""

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result

    def test_generate_sql_query_31(self):
        user_input = "Which market had the greatest sales in 2022?"
        instructions = None
        expected_result = "SELECT market FROM monthly_sales WHERE year = 2022 ORDER BY sales DESC LIMIT 1;"

        result = self.sql_generator.generate_sql_query(
            self.prompt_file,
            self.retry_prompt_file,
            self.database_schema,
            user_input,
            instructions)

        assert result == expected_result