import socket
import sys
def validate_line(line):
    parts = line.strip().split(' ', 2) 
    if len(parts) < 1:
        return False, "Invalid operation"