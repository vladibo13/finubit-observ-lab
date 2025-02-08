from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Summary, Counter, Gauge,Histogram
import time
import requests
import threading

front = Flask("front_service")
CORE_URL = "http://core:5001/coreAPI"

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['endpoint'])
ERROR_COUNT = Counter('http_request_errors_total', 'Total HTTP errors', ['endpoint', 'http_status'])
WITHDRAW_PROCESSING_TIME = Histogram('withdraw_processing_time_seconds', 'Time taken to process withdrawals')

@front.before_request
def start_timer():
    request.start_time = time.time()

@front.after_request
def track_metrics(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.path).observe(request_latency)
    if response.status_code >= 400:
        ERROR_COUNT.labels(request.path, response.status_code).inc()
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

# @PROCESSING_TIME.time() # Record the time for this specific route
@front.route("/withdraw", methods=["POST"])
def withdraw():
    start_time = time.time()
    amount = request.json.get("amount", 0)
    response = requests.post(CORE_URL, json={"action": "withdraw", "amount": amount})
    processing_time = time.time() - start_time
    WITHDRAW_PROCESSING_TIME.observe(processing_time)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    threading.Thread(target=run_prometheus_server).start()  # Start the Prometheus metrics server
    front.run(host="0.0.0.0", port=5000)
