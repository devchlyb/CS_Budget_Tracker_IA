import requests
import datetime

try:
    from config import  GUS_API_KEY
except ImportError:
    GUS_API_KEY = "PUT_KEY_HERE"

BASE_URL = "https://api-dbw.stat.gov.pl/api/1.1.0"
HEADERS = {
    "X-ClientId": GUS_API_KEY,
    "Accept": "application/json",
}

# html stats
ZMIENNA_ID = 305 # variable: CPI
PRZEKROJ_ID = 739 # cross section
OVERALL_POSITION = 6656078 # confirm label in DBW metadata
YOY_MEASURE = 5 # 5 = same month prev. year = 100

def _extract_yoy(payload):
    for rec in payload.get("data", []):
        if (rec.get("id-pozycja-2") == OVERALL_POSITION
                and rec.get("id-sposob-prezentacji-miara") == YOY_MEASURE):
            return rec["wartosc"]
    return None

def get_latest_inflation():
    now = datetime.datetime.now()
    rok = now.year
    miesiac = now.month
    url = f"{BASE_URL}/variable/variable-data-section"

    for _ in range(18):
        okres_id = 246 + miesiac
        params = {
            "id-zmienna": ZMIENNA_ID,
            "id-przekroj": PRZEKROJ_ID,
            "id-rok": rok,
            "id-okres": okres_id,
        }
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=15)
            if response.status_code == 200:
                index_value = _extract_yoy(response.json())
                if index_value is not None:
                    return round(index_value - 100, 1) 
        except requests.exeptrions.RequestException:
            return None
        
        miesiac -= 1
        if miesiac == 0:
            miesiac = 12
            rok -= 1
    return None