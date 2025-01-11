import yaml
import requests
import time
import logging
import sys
from collections import defaultdict

def configure_logging(file_name):
    """Set up logging to a file."""
    logging.getLogger().handlers.clear()
    file_handler = logging.FileHandler(f'{file_name}_health_check.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger

def validate_file_extension(file_path):
    """Ensure the provided file has a .yaml or .yml extension."""
    if not file_path.lower().endswith(('.yaml', '.yml')):
        raise ValueError("Provided file must be a .yaml or .yml file.")

def read_config(file_path):
    """Read and load configuration from a YAML file."""
    logger.info(f"Reading configuration from {file_path}")
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logger.error(f"Failed to read the configuration file: {e}")
        raise

def send_request(method, url, headers=None, body=None):
    """Send an HTTP request and return the response."""
    request_methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
        'PATCH': requests.patch,
        'OPTIONS': requests.options,
        'HEAD': requests.head,
        'TRACE': lambda url, **kwargs: requests.request('TRACE', url, **kwargs)
    }

    try:
        response = request_methods[method](url, headers=headers, json=body, timeout=5)
        return response
    except requests.RequestException as e:
        logger.error(f"Request to {url} failed: {e}")
        return None

def check_health(endpoint):
    """Check the health status of a given endpoint."""
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)
    
    logger.info(f"Checking health for endpoint {url} with method {method}")
    
    if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE']:
        logger.warning(f"Unsupported HTTP method {method} for endpoint {url}")
        return 'DOWN'

    response = send_request(method, url, headers, body)
    if response and 200 <= response.status_code < 300 and response.elapsed.total_seconds() < 0.5:
        logger.info(f"Endpoint {url} is UP with status {response.status_code}")
        return 'UP'
    else:
        logger.warning(f"Endpoint {url} is DOWN with status {response.status_code if response else 'N/A'} and response time {response.elapsed.total_seconds() if response else 'N/A'} seconds")
        return 'DOWN'

def log_availability(availability):
    """Log the availability results."""
    print("\nLogging availability results:")
    for domain, data in availability.items():
        total = data['total']
        up = data['up']
        percentage = (up / total) * 100
        print(f"{domain} has {round(percentage)}% availability percentage")
        logger.info(f"{domain} has {round(percentage)}% availability percentage")

def monitor_endpoints(config):
    """Continuously monitor the health of endpoints."""
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
        logger.info("Program exited by user.")
        print("\nProgram exited by user.")

def main():
    """Main function to run the health check program."""
    if len(sys.argv) < 2:
        print("Error: Missing file name in the command line arguments.")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        validate_file_extension(file_path)
        global logger
        logger = configure_logging(file_path.split('.')[0])
        logger.info("Starting health check program.")
        config = read_config(file_path)
        monitor_endpoints(config)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()