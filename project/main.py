from modules.prompt_loader import PromptLoader
from modules.postgres import Postgres
from modules.sql_generator import SQLQueryGenerator
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download

model_dir = "./models/llama-3-sqlcoder-8b"
db_config = {                      # --> se podría pedir al usuario la configuración que quiera y dejar una preconfigurada
    "host": "localhost",
    "port": 5432,
    "database": "my_database",
    "user": "my_user",
    "password": "my_password"
}


#---------------------- USER INPUTS ----------------------#

user_input = "¿Cuáles son los cinco productos más vendidos este mes?"
instructions = "Include only orders from the last month."
database_schema = """
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    total_amount DECIMAL,
    status VARCHAR(20),
    order_date DATE
);
"""

if not database_schema:
    print("Fetching table definitions from the database...")
    postgres_db = Postgres(db_config)
    database_schema = postgres_db.get_db_schema_and_relationships()



#----------------------- MODEL LOAD ----------------------#

tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(model_dir)



#---------------------- PROMPT LOAD ----------------------#

prompt_loader = PromptLoader(prompt_dir="./prompts")
prompt_file = "prompt_generate_sql.txt"
retry_prompt_file = "prompt_generate_sql_error.txt"



#-------------------- MODEL EXECUTION --------------------#

sql_generator = SQLQueryGenerator(model, tokenizer, db_config, prompt_loader, 3)
sql_query = sql_generator.generate_sql_with_corrections(user_input, instructions, database_schema)
