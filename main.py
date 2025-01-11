import yaml
import requests
import time
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_config(file_path):
    logging.info(f"Reading configuration from {file_path}")
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logging.error(f"Failed to read the configuration file: {e}")
        raise

def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()  # Default to GET if no method is provided
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)
    
    logging.info(f"Checking health for endpoint {url} with method {method}")
    try:
        # Handle different HTTP methods
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=0.5)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=body, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=body, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, json=body, timeout=5)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=body, timeout=5)
        elif method == 'OPTIONS':
            response = requests.options(url, headers=headers, timeout=5)
        elif method == 'HEAD':
            response = requests.head(url, headers=headers, timeout=5)
        elif method == 'TRACE':
            response = requests.request('TRACE', url, headers=headers, timeout=5)
        else:
            logging.warning(f"Unsupported HTTP method {method} for endpoint {url}")
            return 'DOWN'
        
        # Check if the response status code is 2xx and response time is under 500ms
        if response.status_code >= 200 and response.status_code < 300 and response.elapsed.total_seconds() < 0.5:
            logging.info(f"Endpoint {url} is UP with status {response.status_code}")
            return 'UP'
        else:
            logging.warning(f"Endpoint {url} is DOWN with status {response.status_code} and response time {response.elapsed.total_seconds()} seconds")
            return 'DOWN'
    except requests.RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
        return 'DOWN'

def log_availability(availability):
    logging.info("Logging availability results:")
    for domain, data in availability.items():
        total = data['total']
        up = data['up']
        percentage = (up / total) * 100
        logging.info(f"{domain} has {round(percentage)}% availability percentage")
        print(f"{domain} has {round(percentage)}% availability percentage")

def main(file_path):
    logging.info("Starting health check program.")
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
        logging.info("Program exited by user.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logging.error("Missing file name in the command line arguments.")
    else:
        main(sys.argv[1])