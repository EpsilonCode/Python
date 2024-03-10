import os
import secrets

# Generates a 32-character hexadecimal string
secret_key = secrets.token_hex(16)
print(secret_key)
