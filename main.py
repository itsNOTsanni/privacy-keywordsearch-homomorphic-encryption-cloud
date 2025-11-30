import os

os.system("Python client/generate_keys.py")
os.system("Python client/encrypt_data.py")
os.system("Python cloud/server.py")
os.system("Python client/search_client.py")
