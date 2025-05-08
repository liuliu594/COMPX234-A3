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