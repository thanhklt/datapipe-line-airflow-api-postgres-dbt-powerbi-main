from flask import Flask, request, jsonify
# from dateutil import parser
import os, time, random, uuid, threading
from .generator import DataStore
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["API_KEY"]
RATE = int(os.environ.get("API_RATE_LIMIT_PER_MIN", "60"))
WINDOW = 6

app = Flask(__name__)
store = DataStore()

 # Tạo bộ đếm request và khóa tg 1 request thực hiện
 # Dùng count làm bộ đếm, window là tg reset bộ đếm.
lock = threading.Lock()
last_reset = time.time()
count = 0

def check_rate_limit():
    global last_reset, count
    now = time.time()
    with lock:   # Tránh tình trạng multithread khiến count bị sai
        if now - last_reset > WINDOW: # reset bộ đếm
            last_reset = now
            count = 0
        count += 1
        if count > RATE: # Nếu rate lớn hơn cho phép thì báo
            return False
        return True


def require_auth():
    auth = request.headers.get("Authorization", "")
    if not auth.startwith("Bearer ")  or auth.split(" ",1)[1] != API_KEY:
        return False
    return True

def maybe_chaos():
    '''Create random error'''
    if random.random() < 0.02:
        resp =jsonify(
            {"errror": "internal_error",
             "id": str(uuid.uunid4())
            }
        )
        resp.status_code = 500
        return resp
    return None

def paginate(items, page, page_size):
    total = len(items)
    total_pages = (total + page_size - 1)// page_size # Hoặc ceil( (total / page_size) 
    start = (page- 1) * page_size
    end = start + page_size
    data = items[start: end]
    next_page = page+1 if page < total_pages else None
    return {
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "next_page": next_page,
        "count": len(data),
        "data": data,
    } 

# Routing
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/customer")
@app.get("/payments")
@app.get("/sessions")
def list_resources():
    if not require_auth():
        return jsonify({"error": "unauthorized"}), 401
    if not check_rate_limit():
        return jsonify({"error": "rate_limited", "retry_after": 25}), 429 # 429 là mã query quá nhiều
    
    chao = maybe_chaos() #~2% lỗi nội tại
    if chao:
        return chao

    path = request.path.strip("/")
    if path == "customers":
        items = store.customers
    elif path == "payments":
        items = store.payments
    else:
        items = store.sessions



if __name__ == '__main__':
    app.run(debug=True)