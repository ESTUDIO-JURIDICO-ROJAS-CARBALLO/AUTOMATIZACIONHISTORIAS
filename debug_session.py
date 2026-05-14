from instagrapi import Client
import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

cl = Client()
sid = os.getenv('IG_SESSIONID')
print(f"Testing SessionID: {sid[:10]}...")

try:
    cl.login_by_sessionid(sid)
    print(f"Logged in as: {cl.username} (ID: {cl.user_id})")
    info = cl.account_info()
    print("Account info retrieved successfully.")
except Exception as e:
    print(f"Error: {e}")
