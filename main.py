import yaml
import requests
import time
from collections import defaultdict

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=0.5)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=body, timeout=5)
        else:
            response = requests.request(method, url, headers=headers, json=body, timeout=5)
        
        if response.status_code >= 200 and response.status_code < 300 and response.elapsed.total_seconds() < 0.5:
            return 'UP'
        else:
            return 'DOWN'
    except requests.RequestException:
        return 'DOWN'

def log_availability(availability):
    for domain, data in availability.items():
        total = data['total']
        up = data['up']
        percentage = (up / total) * 100
        print(f"{domain} has {round(percentage)}% availability percentage")

def main(file_path):
    config = read_config(file_path)
    availability = defaultdict(lambda: {'total': 0, 'up': 0})
    
    try:
        while True:
            for endpoint in config:
                domain = endpoint['url'].split('/')[2]  # Extract domain from URL
                result = check_health(endpoint)
                availability[domain]['total'] += 1
                if result == 'UP':
                    availability[domain]['up'] += 1
            log_availability(availability)
            time.sleep(15)
    except KeyboardInterrupt:
        print("Program exited by user.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Missing file name in the command line arguments.")
    else:
        main(sys.argv[1])