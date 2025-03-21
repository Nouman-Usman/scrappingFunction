import requests

# Define API endpoint
url = "http://67dd307b93ef125d26df.appwrite.global/"

# Input case details
data = {
    "district": "Kasur",  # Change district
    "case_no": "145023"  # Change case number
}

# Set headers
headers = {
    "Content-Type": "application/json"
}

# Send request
response = requests.post(url, json=data, headers=headers)

# Print response
print(response)
