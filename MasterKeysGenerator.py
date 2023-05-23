import secrets
import binascii


for i in range(2):
    master_key = secrets.token_bytes(16)
    master_key_hex = binascii.hexlify(master_key).decode()

    print("Generated Master Key:", master_key)
    print("Hexadecimal Representation:", master_key_hex)