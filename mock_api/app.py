from flask import Flask, request, jsonify
# from dateutil import parser
import os, time, random, uuid, threading
from generator import DataStore
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["API_KEY"]
RATE = int(os.environ.get("API_RATE_LIMIT_PER_MIN", "60"))
WINDOW = 6

app = Flask(__name__)
store = DataStore()


def require_auth():
    auth = request.headers.get("Authorization", "")
    if not auth.startwith("Bearer ")  or auth.split(" ",1)[1] != API_KEY:
        return False
    return True

# @app.get("/heath")
def health():
    return {"status": "ok"}
# @app.get("/customer")
# @app.get("/payments")
# @app.get("/sessions")




if __name__ == '__main__':
    print()