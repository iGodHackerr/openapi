import requests
import json

# Replace with your ZeroTier API token
API_TOKEN = "mxWV03A3aCZOiLBgkRTZ9dUtaXGOqx3t"
BASE_URL = "https://my.zerotier.com/api/network"

def create_network():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "name": "MyNetwork",
        "private": True
    }
    response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        network_info = response.json()
        print("Network created successfully:")
        print(f"Network ID: {network_info['id']}")
        return network_info['id']
    else:
        print("Error creating network:", response.json())
        return None

def main():
    network_id = create_network()
    if network_id:
        print(f"Join the network using this command:\nzerotier-cli join {network_id}")

if __name__ == "__main__":
    main()
