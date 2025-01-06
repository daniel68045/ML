import os

# GENERATE SECRET KEY
secret_key = os.urandom(24).hex()
print(secret_key)
