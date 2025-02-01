import os
import sys
from flask import Flask, request, jsonify
from modules.prompt_loader import PromptLoader
from modules.postgres import Postgres
from modules.sql_generator import SQLQueryGenerator
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set the root directory to import own modules
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

app = Flask(__name__)

# Load the model and tokenizer once
model_dir = "./models/llama-3-sqlcoder-8b"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(model_dir)

# Database configuration
db_config = {
    "host": "localhost",
    "port": 5432,
    "database": "sandoz",
    "user": "postgres",
    "password": "postgres"
}

# Prompt loader
prompt_dir = os.path.join(root_dir, "project", "prompts")
prompt_loader = PromptLoader(prompt_dir=prompt_dir)
prompt_file = "prompt_generate_sql.txt"
retry_prompt_file = "prompt_generate_sql_error.txt"

# Database schema
postgres_db = Postgres(db_config)

# SQL Query Generator
sql_generator = SQLQueryGenerator(
    model=model,
    tokenizer=tokenizer,
    postgres_db=postgres_db,
    prompt_loader=prompt_loader,
    max_attempts=3
)

@app.route('/generate_sql', methods=['GET'])
def generate_sql():
    data = request.json
    user_input = data.get('user_input')
    instructions = data.get('instructions', None)

    sql_query = sql_generator.generate_sql_query(
        prompt_file=prompt_file,
        retry_prompt_file=retry_prompt_file,
        user_input=user_input,
        instructions=instructions
    )

    return jsonify({"sql_query": sql_query})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
