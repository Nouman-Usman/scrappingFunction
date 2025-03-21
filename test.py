from appwrite.client import Client
from appwrite.services.functions import Functions
import json

client = Client()

(client
  .set_project('67a4b32f0037187e3aef') # Your project ID
)

functions = Functions(client)

result = functions.create_execution( 
    function_id = '67dd373000179bf564bb', 
    body = '{"district_id": "14","case_no": "145023"}',  # optional
    path = '<PATH>',  # optional
    method = 'GET',  # optional
    headers = {} # optional
)

# Extract and parse response body
response_body = json.loads(result['responseBody'])

# Print formatted response data
print(json.dumps(response_body, indent=2))