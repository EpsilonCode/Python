import requests
import time
from datetime import datetime

# Meraki API key and network ID
MERAKI_API_KEY = "your_api_key_here"
NETWORK_ID = "your_network_id_here"

# API endpoint to get clients for a network
CLIENTS_ENDPOINT = f"https://api.meraki.com/api/v0/networks/{NETWORK_ID}/clients"

# Function to get new clients on the network
def get_new_clients():
    # Make API request to get clients
    headers = {
        "X-Cisco-Meraki-API-Key": MERAKI_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(CLIENTS_ENDPOINT, headers=headers)

    # Check for errors and parse response
    if response.status_code != 200:
        print("Error retrieving clients:", response.text)
        return []
    else:
        clients = response.json()

    # Filter out clients that have been seen before
    new_clients = []
    for client in clients:
        if client["status"] == "Online" and client["dhcpHostname"] not in seen_clients:
            new_clients.append(client)
            seen_clients.add(client["dhcpHostname"])

    # Assign new clients to group policy
    headers = {
        "X-Cisco-Meraki-API-Key": MERAKI_API_KEY,
        "Content-Type": "application/json"
    }
    for client in new_clients:
        payload = {
            "devicePolicy": "group",
            "devicePolicyType": "GroupPolicy",
            "groupPolicyId": "A POLICY"
        }
        response = requests.put(f"https://api.meraki.com/api/v0/networks/{NETWORK_ID}/clients/{client['id']}/policy", json=payload, headers=headers)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Assigned {client['description']} ({client['ip']}) to group policy 'A POLICY'")
        else:
            print("Error assigning group policy:", response.text)

# Set up a set to keep track of seen clients
seen_clients = set()

# Continuously check for new clients every two hours
while True:
    get_new_clients()
    time.sleep(7200)  # Sleep for two hours
