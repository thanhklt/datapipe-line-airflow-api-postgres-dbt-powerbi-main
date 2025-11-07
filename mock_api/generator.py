import uuid, random
from datetime import datetime, timedelta, timezone

# Setup
COUNTRIES = ["US","GB","DE","FR","CA","AU","NL","SE","IT","ES"]
COUNTRY_W = [0.35,0.15,0.12,0.07,0.08,0.06,0.06,0.04,0.04,0.03]
INDUSTRIES = ["E-commerce","SaaS","Consulting","Education","Health","Finance"]
IND_W = [0.35,0.25,0.12,0.1,0.1,0.08]
PRODUCTS = ["Basic","Pro","Enterprise","Addon-Analytics","Addon-Support"]
PRICES = {"Basic":29,"Pro":99,"Enterprise":499,"Addon-Analytics":49,"Addon-Support":99}
PAYMENT_METHODS=["card","bank_transfer","paypal","apple_pay","google_pay"]
PM_W=[0.6,0.15,0.15,0.05,0.05]
STATUSES=["succeeded","failed","refunded"]
STAT_W=[0.9,0.06,0.04]
SOURCES=["google","direct","facebook","linkedin","newsletter","referral","bing"]
SRC_W=[0.45,0.18,0.12,0.08,0.07,0.06,0.04]
MEDIUMS=["organic","cpc","email","social","none","referral"]
MED_W=[0.5,0.18,0.1,0.12,0.06,0.04]
DEVICES=["desktop","mobile","tablet"]
DEV_W=[0.55,0.4,0.05]

TZ = timezone.utc

random.seed(42)

def _rand_date(days_back=180):
    '''Trả về datetime trong khoangr days_back đến now'''
    now = datetime.now(TZ)
    start = now - timedelta(days=days_back)
    dt = start + timedelta(
        seconds=random.randint(0, days_back*24*3600)
    )
    return dt

class DataStore:
    def __init__(self):
        self.customers = []
        self.payments = []
        self.sessions = []
        self._generate()

    def _generate(self):
        # customers
        for i in range(1000):
            cid = str(uuid.uuid4())
            signup = _rand_date(360)
            country = random.choices(COUNTRIES, COUNTRY_W)
            industry = random.choices(INDUSTRIES, IND_W)
            size = random.choices(["1-10","11-50","51-200","201-500","500+"],[0.35,0.3,0.2,0.1,0.05])[0]
            churn = random.random() < 0.18
            self.customers.append({
                "customer_id": cid,
                "company_name": f"Company {i:04d}",
                "country": country,
                "industry": industry,
                "company_size": size,
                "signup_date": signup.isoformat(),
                "updated_at": signup.isoformat(),
                "is_churn": churn,
            })

        # Payments:
        for _ in range(10_000):
            c = random.choice(self.customers)
            product=random.choices(PRODUCTS, weights={
                "E-commerce":[0.4,0.35,0.05,0.1,0.1],
                "SaaS":[0.25,0.4,0.15,0.1,0.1],
                "Consulting":[0.35,0.35,0.1,0.1,0.1],
                "Education":[0.45,0.3,0.05,0.1,0.1],
                "Health":[0.3,0.35,0.15,0.1,0.1],
                "Finance":[0.25,0.4,0.2,0.075,0.075]
            }[c["industry"]])[0]

if __name__ == "__main__":
    store = DataStore()
    print(store.customers)