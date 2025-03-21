import requests
from bs4 import BeautifulSoup
import json
import os

def main(req, res):
    try:
        # Parse input JSON
        body = json.loads(req.body)
        district = body.get("district")
        case_no = body.get("case_no")

        if not district or not case_no:
            return res.json({"error": "Missing district or case_no"}, status=400)

        # URL for the case search (Modify if needed)
        base_url = "https://dsj.punjab.gov.pk/case-details"
        params = {"district": district, "case_no": case_no}

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code != 200:
            return res.json({"error": "Failed to fetch data"}, status=500)

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract case details (Modify selectors based on actual HTML structure)
        case_details = {}
        labels = soup.find_all("td", class_="case-label")  # Modify selector
        values = soup.find_all("td", class_="case-value")  # Modify selector

        if not labels or not values:
            return res.json({"error": "No case details found"}, status=404)

        for label, value in zip(labels, values):
            case_details[label.text.strip()] = value.text.strip()

        return res.json(case_details)

    except Exception as e:
        return res.json({"error": str(e)}, status=500)
