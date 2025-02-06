## Usage


1. Clone the project
```bash
  git clone https://github.com/barkai36/finubit-observ-lab.git
```
3. Go to project directory
```bash
cd finubit-observ-lab
```
4. Run project
```bash
docker-compose up --build 
```

## Testing
The project will run two services: 'deposit' and 'core'.


The 'deposit' service represent a front-end service to customers.

The 'core' service represent a back-end that is not reached to customer.

The following API requests are available with 'deposit':

http://localhost:5000/deposit
Deposit ammount of money into the account.

Example:
```bash
curl --location 'http://localhost:5000/deposit' \
--header 'Content-Type: application/json' \
--data '{
    "amount":100
}'
```

http://localhost:5000/withdraw
Withdraw amount of money from the account
Example:
```bash
curl --location 'http://localhost:5000/withdraw' \
--header 'Content-Type: application/json' \
--data '{
    "amount":100
}'
```

## Testing Prometheus and Grafana 
1. Added the prometheus and grafana services in docker-compose.yml for monitoring.

2. Added a prometheus.yml Configuration File for prometheus which defines how Prometheus scrapes metrics from different targets

3. docker-compose up -d --build to build the new docker images

4. Access Prometheus & Grafana
Prometheus UI: http://localhost:9090
Grafana UI: http://localhost:3000
Default username: admin
Default password: admin

5. Configure Grafana to Use Prometheus
Open Grafana at http://localhost:3000
Log in with admin/admin
Go to Configuration → Data Sources
Add a Prometheus data source
Set the URL to http://prometheus:9090
Save & test the connection

6. Front Service (Flask)
expose the necessary metrics, such as request counts, response times, error rates, and processing times
Metrics in the Front Service:
http_requests_total: Tracks the total number of HTTP requests received.
http_responses_total: Tracks HTTP response statuses, such as 2xx, 4xx, and 5xx.
http_request_latency_seconds: Measures the time taken to process each HTTP request (useful for tracking response times).
http_processing_time_seconds: Specifically tracks the processing time for the withdraw route since it's intentionally slow.

7.  Core Service (Flask)
The core service should also expose Prometheus metrics. added similar instrumentation for the core service’s endpoints.
Metrics in the Core Service:
core_http_requests_total: Tracks the total number of HTTP requests received by the core service.
core_http_responses_total: Tracks the response status codes for the core service (e.g., 2xx, 4xx, 5xx).
core_http_request_latency_seconds: Measures the time taken to process each HTTP request in the core service.

8.  Prometheus Configuration
setup Prometheus is configured to scrape these metrics.
configure Prometheus to scrape metrics from both services in prometheus.yml

9. Ensuring Metrics Are Scraped
Verify Prometheus is able to scrape both the front and core services by navigating to http://localhost:9090/targets