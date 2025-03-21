import requests
from bs4 import BeautifulSoup
import json

def main(context):
    try:
        # Parse input JSON
        body = json.loads(context.req.body)
        district = body.get("district")
        case_no = body.get("case_no")

        if not district or not case_no:
            return context.res.json({"error": "Missing district or case_no"}, 400)

        # Logging input data
        context.log(f"Searching case in: {district}, Case No: {case_no}")

        # Base URL for the case search
        base_url = "https://dsj.punjab.gov.pk/case-details"
        params = {"district": district, "case_no": case_no}

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Using session for better efficiency
        with requests.Session() as session:
            response = session.get(base_url, params=params, headers=headers)

        # Logging response status
        context.log(f"Response Code: {response.status_code}")

        if response.status_code != 200:
            return context.res.json({"error": f"Failed to fetch data, Status: {response.status_code}"}, 500)

        soup = BeautifulSoup(response.text, "html.parser")

        # Extracting case details
        case_details = {}

        # Attempting multiple selectors for robustness
        labels = soup.find_all("td", class_="case-label") or soup.find_all("th")
        values = soup.find_all("td", class_="case-value") or soup.find_all("td")

        if not labels or not values or len(labels) != len(values):
            context.log("No case details found or structure mismatch")
            return context.res.json({"error": "No case details found"}, 404)

        for label, value in zip(labels, values):
            case_details[label.get_text(strip=True)] = value.get_text(strip=True)

        context.log(f"Case Details Fetched: {case_details}")

        return context.res.json({"success": True, "data": case_details})

    except Exception as e:
        context.log(f"Error: {str(e)}")
        return context.res.json({"error": str(e)}, 500)
