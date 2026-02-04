import requests

# The URL of your running server
url = "http://127.0.0.1:5000/update-progress"

# The data we want to send (simulating the Frontend)
payload = {
    "role": "frontend",
    "completed": ["html", "css"]
}

try:
    # Send the POST request
    response = requests.post(url, json=payload)

    # Print the result nicely
    print("✅ Status Code:", response.status_code)
    print("⬇️ Response from Server:")
    import json

    print(json.dumps(response.json(), indent=2))

except Exception as e:
    print("❌ Connection Failed. Is the server running?")
    print(e)