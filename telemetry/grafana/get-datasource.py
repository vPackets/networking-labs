import requests
from requests.auth import HTTPBasicAuth

# Your Grafana instance details
url = "http://localhost:3000/api/datasources"
username = "netadmin"
password = "C1sco12345!"

# Make the GET request with HTTP Basic Authentication
response = requests.get(
    url,
    auth=HTTPBasicAuth(username, password),
    headers={"Accept": "application/json", "Content-Type": "application/json"}
)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data_sources = response.json()
    print("Data Sources:", data_sources)
else:
    print("Failed to fetch data sources. Status code:", response.status_code)
