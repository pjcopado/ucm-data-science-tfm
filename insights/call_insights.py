import socket
import json

def call_insights(user_question, sql_result):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8000))

    request = json.dumps({
        'user_question': user_question,
        'sql_result': sql_result
    })
    client.sendall(request.encode())

    response = client.recv(4096).decode()
    print(f"Insights: {response}")

    client.close()


# Example Usage
call_insights("What were the sales in Germany in August 2021?", "40000")
