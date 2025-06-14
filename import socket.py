import socket
import sys
def validate_line(line):
    parts = line.strip().split(' ', 2) 
    if len(parts) < 1:
        return False, "Invalid operation"
    op = parts[0]
    if op not in ['PUT', 'GET', 'READ']:
        return False, "Invalid operation"

    if op == 'PUT':
        if len(parts) < 3:
            return False, "PUT requires key and value"
        key = parts[1]
        value = parts[2]
        collated = f"{key} {value}"
        if len(collated) > 970:
            return False, "Collated size exceeds 970"
        return True, (op, key, value)
    else:
        if len(parts) < 2:
            return False, f"{op} requires key"
        key = parts[1]
        return True, (op, key)
def main():
    if len(sys.argv) != 4:
        print("Usage: client.py <host> <port> <request_file>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Connection refused")
        return
    for line in lines:
        valid, data = validate_line(line)
        if not valid:
            print(f"Invalid line: {line.strip()} - {data}")
            continue
        if data[0] == 'PUT':
            _, key, value = data
            msg_body = f"P {key} {value}"
        else:
            op, key = data
            msg_body = f"{'R' if op == 'READ' else 'G'} {key}"
        msg_length = len(msg_body)
        if msg_length > 999:
            print(f"Message too long: {line.strip()}")
            continue    
        full_msg = f"{msg_length:03d}{msg_body}".encode()
        client_socket.sendall(full_msg)
        header = client_socket.recv(3)
        if not header:
            print("Server closed connection")
            break
        resp_length = int(header.decode())
        response = client_socket.recv(resp_length).decode()
        print(f"{line.strip()}: {response}")
    client_socket.close()
if __name__ == "__main__":
    main()