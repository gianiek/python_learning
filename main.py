import requests
import csv
import json
from tqdm import tqdm

speed_count = 0
speedLimit_count = 0
error_count = 0

with open('input_with_response.csv', mode='w', newline='') as output_csv_file:
    fieldnames = ['request', 'response', 'speedCount', 'speedLimitCount']
    csv_writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    with open('input.csv', mode='r') as input_csv_file:
        csv_reader = csv.DictReader(input_csv_file)

        for row in tqdm(csv_reader, desc='Processing API calls'):
            request_data = json.loads(row['request'])

            road_attributes = []

            url = "https://api.radar-staging.com/v1/route/match"
            response = requests.get(url, params=request_data['query'], headers={"Authorization": "prj_test_pk_f9f8d237e74a54a12eca835199b111cc2c11e148"})

            local_speed_count = 0
            local_speedLimit_count = 0

            if response.status_code == 200:
                # New: Look in the 'edges' array for 'speed'
                edges = response.json().get('edges', [])
                for edge in edges:
                    if 'speed' in edge:
                        local_speed_count += 1

                # New: Look in 'roadAttributes' for 'speedLimit'
                road_attributes = response.json().get('roadAttributes', {})
                if 'speedLimit' in road_attributes:
                    local_speedLimit_count += 1

                speed_count += local_speed_count
                speedLimit_count += local_speedLimit_count
            else:
                error_count += 1

            row['response'] = response.json()
            row['speedCount'] = local_speed_count
            row['speedLimitCount'] = local_speedLimit_count
            csv_writer.writerow(row)

            print(f"Speed: {speed_count}, Speed Limit: {speedLimit_count}, Errors: {error_count}", end='\r')

print(f"\nTotal Speed Count: {speed_count}")
print(f"Total Speed Limit Count: {speedLimit_count}")
print(f"Total Error Count: {error_count}")
