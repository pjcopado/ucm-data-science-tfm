import os
import sys
import pytest

# Set the root directory to import own modules
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

from project.app import main  # noqa: E402

def test_main_1():
    user_input = "How many years of historical data do we have available for Spain?"
    instructions = None
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT COUNT(*) FROM monthly_sales WHERE country = 'Spain';"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_2():
    user_input = "How many years of historical data do we have available for the south cluster of Europe?"
    instructions = None
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT COUNT(*) FROM monthly_sales WHERE region = 'south cluster of Europe';"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_3():
    user_input = "What is the oldest data for which we have sales in Spain?"
    instructions = None
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT MIN(month) FROM monthly_sales WHERE country = 'Spain';"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_4():
    user_input = "In which countries did we sell products in 2023?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT DISTINCT country FROM monthly_sales WHERE year = 2023;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_5():
    user_input = "What were the sales in Germany in August 2021?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE country = 'Germany' AND month = 'August' AND year = 2021;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_6():
    user_input = "What were the sales in Europe in 2023?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE region = 'Europe' AND year = 2023;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_7():
    user_input = "What were the sales in North America in 2023?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE region = 'North America' AND year = 2023;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_8():
    user_input = "What was the demand in Italy in 2022?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(demand) FROM monthly_sales WHERE country = 'Italy' AND year = 2022;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_9():
    user_input = "What was the demand in bio in Germany in August 2021?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(demand) FROM monthly_sales WHERE category = 'bio' AND country = 'Germany' AND month = 'August' AND year = 2021;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_10():
    user_input = "How many units were sold in bio in Germany in August 2021?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(units_sold) FROM monthly_sales WHERE category = 'bio' AND country = 'Germany' AND month = 'August' AND year = 2021;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_11():
    user_input = "What was the month with higher demand in North America in 2022?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT month FROM monthly_sales WHERE region = 'North America' AND year = 2022 ORDER BY demand DESC LIMIT 1;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_12():
    user_input = "What were the total bio sales in 2022?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE category = 'bio' AND year = 2022;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_13():
    user_input = "And the total retail sales that same year?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE category = 'retail' AND year = 2022;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_14():
    user_input = "What were the sales in Spain in 2022?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE country = 'Spain' AND year = 2022;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_15():
    user_input = "What were the sales in the spanish market in 2022?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE market = 'spanish' AND year = 2022;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_16():
    user_input = "What were the sales in the spanish market 2 years ago?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(sales) FROM monthly_sales WHERE market = 'spanish' AND year = (CURRENT_YEAR - 2);"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_17():
    user_input = "What was the total growth in sales Canada in 2023?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT SUM(growth) FROM monthly_sales WHERE country = 'Canada' AND year = 2023;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_18():
    user_input = "And the growth per business unit in 2023?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT business_unit, SUM(growth) FROM monthly_sales WHERE year = 2023 GROUP BY business_unit;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_19():
    user_input = "And the growth per business unit that same year?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT business_unit, SUM(growth) FROM monthly_sales WHERE year = 2023 GROUP BY business_unit;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_20():
    user_input = "Which european market had a higher growth in sales 2023 in bio?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT market FROM monthly_sales WHERE region = 'Europe' AND category = 'bio' AND year = 2023 ORDER BY growth DESC LIMIT 1;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_21():
    user_input = "And in north america?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT market FROM monthly_sales WHERE region = 'North America' AND year = 2023 ORDER BY growth DESC LIMIT 1;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_22():
    user_input = "What about retail? Which was the market with higher growth in 2022 in bio?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT market FROM monthly_sales WHERE category = 'bio' AND year = 2022 ORDER BY growth DESC LIMIT 1;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_23():
    user_input = "In which months from 2023 did we see a positive growth in demand versus the previous year?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT month FROM monthly_sales WHERE year = 2023 AND growth > 0;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_24():
    user_input = "In which months from 2023 did we see a growth in demand versus the previous year?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT month FROM monthly_sales WHERE year = 2023 AND growth > 0;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_25():
    user_input = "How accurate was the LO for United States in April 2023?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT accuracy FROM monthly_lo WHERE country = 'United States' AND month = 'April' AND year = 2023;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_26():
    user_input = "What is the LO for total Spain 2024?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT lo FROM monthly_lo WHERE country = 'Spain' AND year = 2024;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_27():
    user_input = "What is the number of the planned sales for total Spain 2024?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT planned_sales FROM monthly_lo WHERE country = 'Spain' AND year = 2024;"
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_28():
    user_input = "How good was the LO vs the sales last month?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = ""
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_29():
    user_input = "What was the percentage of accuracy of the LO in may 2023 in the US?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = ""
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_30():
    user_input = "What was the percentage of accuracy of the LO in 2023 in the US?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = ""
    result = main(user_input, instructions)
    assert result == expected_result

def test_main_31():
    user_input = "Which market had the greatest sales in 2022?"
    instructions = ""
    # TODO: Update the expected_result with the expected SQL query
    expected_result = "SELECT market FROM monthly_sales WHERE year = 2022 ORDER BY sales DESC LIMIT 1;"
    result = main(user_input, instructions)
    assert result == expected_result