import os
import sys
import argparse
from modules.prompt_loader import PromptLoader
from modules.postgres import Postgres
from modules.sql_generator import SQLQueryGenerator
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set the root directory to import own modules
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

model_dir = "./models/llama-3-sqlcoder-8b"

db_config = {
    "host": "localhost",
    "port": 5432,
    "database": "sandoz",
    "user": "postgres",
    "password": "postgres"
}


def main(user_input, instructions=None, database_schema=None):
    if not database_schema:
        print("Fetching table definitions from the database...")
        postgres_db = Postgres(db_config)
        database_schema = postgres_db.get_db_schema_and_relationships()
        print(database_schema)

    # Load the model and tokenizer from the local directory
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(model_dir)

    # Prompt loader
    prompt_loader = PromptLoader(prompt_dir="./prompts")
    prompt_file = "prompt_generate_sql.txt"
    retry_prompt_file = "prompt_generate_sql_error.txt"

    # SQL Query Generator
    sql_generator = SQLQueryGenerator(
        model=model,
        tokenizer=tokenizer,
        db_config=db_config,
        prompt_loader=prompt_loader,
        max_attempts=3)

    # Generate SQL query
    sql_query = sql_generator.generate_sql_query(
        prompt_file=prompt_file,
        retry_prompt_file=retry_prompt_file,
        user_input=user_input,
        instructions=instructions,
        database_schema=database_schema
    )

    print(sql_query)
    return sql_query


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some inputs.")
    parser.add_argument("user_input", type=str, help="The user input")
    parser.add_argument("--instructions", type=str, help="(Optional) - Extra instructions")
    parser.add_argument("--database_schema", type=str, help="(Optional) - Database schema. If it is not provided it will be fetched from the database.")

    args = parser.parse_args()
    main(args.user_input, args.instructions, args.database_schema)
