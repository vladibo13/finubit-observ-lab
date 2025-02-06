from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Summary, Counter, Gauge
import time
import threading

core = Flask("core_service")
account_balance = 0

# Prometheus Metrics
REQUESTS = Counter('core_http_requests_total', 'Total HTTP Requests')
RESPONSES = Counter('core_http_responses_total', 'HTTP Responses', ['status'])
REQUEST_LATENCY = Summary('core_http_request_latency_seconds', 'HTTP Request Latency')

@core.before_request
def before_request():
    request.start_time = time.time()

@core.after_request
def after_request(response):
    # Record metrics for requests
    REQUESTS.inc()  # Increment the total request counter
    
    # Record response status code
    RESPONSES.labels(status=response.status_code).inc()

    # Measure request latency
    latency = time.time() - request.start_time
    REQUEST_LATENCY.observe(latency)

    return response



@core.route("/coreAPI", methods=["POST"])
def core_api():
    global account_balance
    data = request.json
    action = data.get("action")
    amount = data.get("amount", 0)

    if action == "deposit":
        account_balance += amount
        return jsonify({"new_balance": account_balance}), 200

    elif action == "withdraw":
        time.sleep(5)  # Simulating slow response
        if amount <= account_balance:
            account_balance -= amount
            return jsonify({"message": "OK"}), 200
        return jsonify({"error": "Insufficient funds"}), 400

    return jsonify({"error": "Invalid action"}), 400

# Expose metrics at /metrics
@core.route('/metrics')
def metrics():
    from prometheus_client import generate_latest
    return generate_latest()

def run_prometheus_server():
    # Start the Prometheus metrics server on port 8000
    start_http_server(8001)

if __name__ == "__main__":
    threading.Thread(target=run_prometheus_server).start() # Start the Prometheus metrics server
    core.run(host="0.0.0.0", port=5001)
