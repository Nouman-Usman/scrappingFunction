import requests
from bs4 import BeautifulSoup
import json
import os
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException

# This Appwrite function will be executed every time your function is triggered
def main(context):
    # Initialize Appwrite client
    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(context.req.headers.get("x-appwrite-key", ""))
    )
    
    users = Users(client)

    try:
        response = users.list()
        context.log(f"Total users: {response['total']}")
    except AppwriteException as err:
        context.error(f"Could not list users: {repr(err)}")

    # Handle `/ping` path for health check
    if context.req.path == "/ping":
        return context.res.text("Pong")

    # Parse input JSON
    try:
        body = json.loads(context.req.body)
        district = body.get("district")
        case_no = body.get("case_no")

        if not district or not case_no:
            return context.res.json({"error": "Missing district or case_no"}, 400)

        context.log(f"Fetching case details for District: {district}, Case No: {case_no}")

        # Case search URL
        base_url = "https://dsj.punjab.gov.pk/case-details"
        params = {"district": district, "case_no": case_no}

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Send request
        response = requests.get(base_url, params=params, headers=headers)

        context.log(f"Response Code: {response.status_code}")

        if response.status_code != 200:
            return context.res.json({"error": f"Failed to fetch data, Status: {response.status_code}"}, 500)

        # Parse response
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract case details (Adjust selectors based on actual HTML)
        case_details = {}
        labels = soup.find_all("td", class_="case-label") or soup.find_all("th")
        values = soup.find_all("td", class_="case-value") or soup.find_all("td")

        if not labels or not values or len(labels) != len(values):
            return context.res.json({"error": "No case details found"}, 404)

        for label, value in zip(labels, values):
            case_details[label.get_text(strip=True)] = value.get_text(strip=True)

        context.log(f"Case Details Retrieved: {case_details}")

        return context.res.json({"success": True, "data": case_details})

    except Exception as e:
        context.error(f"Error: {str(e)}")
        return context.res.json({"error": str(e)}, 500)
