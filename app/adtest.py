import json
from datetime import datetime
from typing import Dict,List

# Initialize the list of ads
ads = [
    {"id": 1, "name": "Ad 1", "image_url": "https://example.com/ad1.jpg", "targeting": {"age": [20, 30], "gender": "male"}},
    {"id": 2, "name": "Ad 2", "image_url": "https://example.com/ad2.jpg", "targeting": {"age": [25, 35], "gender": "female"}},
    {"id": 3, "name": "Ad 3", "image_url": "https://example.com/ad3.jpg", "targeting": {"age": [30, 40], "gender": "male"}}
]

# Initialize the list of ad_reports
ad_reports = []

# Define a function to retrieve an ad by ID
def get_ad_by_id(ad_id: int) -> Dict:
    for ad in ads:
        if ad["id"] == ad_id:
            return ad
    return None
# Define a function to serve an ad based on targeting criteria
def serve_ad(age: int, gender: str) -> Dict:
    for ad in ads:
        targeting = ad.get("targeting", {})
        if targeting.get("age")[0] <= age <= targeting.get("age")[1] and targeting.get("gender") == gender:
            return ad
    return None

# Define a function to track ad views
def track_ad_view(ad_id: int, user_id: int) -> None:
    ad_report = {"ad_id": ad_id, "user_id": user_id, "view_time": datetime.now()}
    ad_reports.append(ad_report)

# Define a function to retrieve ad reports
def get_ad_reports() -> List:
    return ad_reports

chosen_ad=get_ad_by_id(6)
print(chosen_ad)
