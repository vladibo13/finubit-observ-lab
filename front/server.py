from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Summary, Counter, Gauge
import time
import requests
import threading

front = Flask("front_service")
CORE_URL = "http://core:5001/coreAPI"

# Prometheus Metrics
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')
RESPONSES = Counter('http_responses_total', 'HTTP Responses', ['status'])
REQUEST_LATENCY = Summary('http_request_latency_seconds', 'HTTP Request Latency')
PROCESSING_TIME = Summary('http_processing_time_seconds', 'Time taken to process requests')

@front.before_request
def before_request():
    request.start_time = time.time()

@front.after_request
def after_request(response):
    # Record metrics for requests
    REQUESTS.inc()  # Increment the total request counter
    
    # Record response status code
    RESPONSES.labels(status=response.status_code).inc()

    # Measure request latency
    latency = time.time() - request.start_time
    REQUEST_LATENCY.observe(latency)

    return response

# Expose metrics at /metrics
@front.route('/metrics')
def metrics():
    from prometheus_client import generate_latest
    return generate_latest()

def run_prometheus_server():
    # Start the Prometheus metrics server on port 8000
    start_http_server(8000)

@front.route("/deposit", methods=["POST"])
def deposit():
    amount = request.json.get("amount", 0)
    response = requests.post(CORE_URL, json={"action": "deposit", "amount": amount})
    return jsonify(response.json()), response.status_code

@PROCESSING_TIME.time() # Record the time for this specific route
@front.route("/withdraw", methods=["POST"])
def withdraw():
    amount = request.json.get("amount", 0)
    response = requests.post(CORE_URL, json={"action": "withdraw", "amount": amount})
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    threading.Thread(target=run_prometheus_server).start()  # Start the Prometheus metrics server
    front.run(host="0.0.0.0", port=5000)
