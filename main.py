import requests
import csv
import json

# API URL base and authorization header
url_base = "https://api.radar-staging.com"
headers = {
    "Authorization": "prj_test_pk_f9f8d237e74a54a12eca835199b111cc2c11e148"
}

# Counters to keep track of speed and speed_limit
speed_count = 0
speed_limit_count = 0

# Read from input.csv
with open('input.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        request_data = json.loads(row['request'])

        # Set roadAttributes to "speedLimit" if not found
        if 'roadAttributes' not in request_data["query"]:
            request_data["query"]["roadAttributes"] = "speedLimit"

        url_path = request_data["path"]
        query = request_data["query"]

        response = requests.get(f"{url_base}{url_path}", headers=headers, params=query)
        response_data = response.json()

        if 'edges' in response_data:
            for edge in response_data['edges']:
                if 'speed' in edge:
                    speed_count += 1
                elif 'speedLimit' in edge:
                    speed_limit_count += 1

        # Print the response data
        print("Response:", response_data)

# Calculate and print the percentages
total_count = speed_count + speed_limit_count
print(f"Speed Count: {speed_count} ({(speed_count / total_count) * 100}%)")
print(f"Speed Limit Count: {speed_limit_count} ({(speed_limit_count / total_count) * 100}%)")
