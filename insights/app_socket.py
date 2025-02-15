import socket
import json
from insights_generator import InsightGenerator

# Initialize the InsightGenerator singleton
insight_gen = InsightGenerator()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8000))
server.listen(5)

print("Server listening on port 8000...")

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")

    data = client_socket.recv(1024)
    if not data:
        break

    try:
        request = json.loads(data.decode())
        response = insight_gen.generate_response(
            request["user_question"], request["sql_result"]
        )
        client_socket.send(json.dumps({"response": response}).encode())
    except Exception as e:
        client_socket.send(json.dumps({"error": str(e)}).encode())

    client_socket.close()