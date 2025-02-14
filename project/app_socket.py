import socket
import json
from modules.sql_generator_v2 import SQLQueryGenerator

# Model name
model_name = "llama-3-sqlcoder-8b-Q8_0"

# Database configuration
db_config = {
    "host": "192.168.1.141",
    "port": 5433,
    "database": "sandoz",
    "user": "postgres",
    "password": "postgres",
}


# Initialize the SQLQueryGenerator class
sql_generator = SQLQueryGenerator(
    model_name=model_name, db_config=db_config, max_attempts=3
)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5000))
server.listen(5)

print("Server listening on port 5000...")

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")

    data = client_socket.recv(1024)
    if not data:
        break

    try:
        request = json.loads(data.decode())
        user_question = request["user_question"]
        user_instruction = request.get("user_instruction", None)
        db_schema = request.get("db_schema", None)

        response = sql_generator.generate_sql_query(
            user_question, user_instruction, db_schema
        )
        client_socket.send(json.dumps({"response": response}).encode())
    except Exception as e:
        client_socket.send(json.dumps({"error": str(e)}).encode())

    client_socket.close()