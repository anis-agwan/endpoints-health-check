# Health Check Script

This script monitors the availability and response time of various endpoints. It checks the status of the endpoints and logs their availability percentage, based on whether they respond with status codes in the range 200-299 and if their response time is under 0.5 seconds. The script supports multiple HTTP methods, including `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`, `HEAD`, and `TRACE`.

## Features

- **Health Check**: Periodically checks the health of configured URLs.
- **Custom Headers**: Supports custom headers as configured in the YAML file.
- **Multiple HTTP Methods**: Handles various HTTP methods (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`, `HEAD`, `TRACE`).
- **Response Validation**: Checks if the HTTP status code is in the 2xx range and ensures the response time is under 0.5 seconds.
- **Logging**: Logs the availability percentage for each domain based on the number of successful responses.
  
## Requirements

- Python 3.x
- `requests` library
- `PyYAML` library

You can install the required dependencies using `pip`:

```bash
pip install requests pyyaml
```
or
```bash
pip3 install requests pyyaml
```


## Configuration
The configuration is stored in a YAML file, where each endpoint is defined with:
- url: The URL to monitor.
- method: The HTTP method to use (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, TRACE).
- headers: (Optional) Custom headers for the request.
- body: (Optional) Request body (used for POST, PUT, PATCH).
- name: (Optional) A human-readable name for the endpoint (for logging purposes).

You can find the sample inputs in the "sample_input.yml" file.

## How to Run
1.	Clone the repository or download the script and the configuration YAML file.
2.	Install the required libraries using the pip command above.
3.	Run the script from the command line:
```bash
    python main.py sample_input.yml
```
Where sample_input.yml is the path to your configuration file.

The script will continue running indefinitely, checking the endpoints every 15 seconds. Press Ctrl+C to stop the script.

You can also find additional test cases in files:
1. additional_methods_test.yml
2. additional_endpoints_tests.yml