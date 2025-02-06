##  Detecting Slow APIs (Latency > 2000ms)

#### Question 
Explain how you would use the dashboard to detect APIs that take longer than
2000ms.
Describe which chart or metric would indicate the issue.

#### Answer 
- I will focus on the P90 and P99 response times on the API Response Times chart.
- Set up alerts to trigger when response times exceed 2000ms.
- If response times exceed 2000ms consistently, it indicates potential performance bottlenecks or underperformance that should be investigated further.

## Detecting High Error Rates (>30%)

#### Question 
 Explain how you would use the dashboard to detect when an API has an error rate
exceeding 30%.
 Describe which metric(s) and visualizations would highlight this issue.

#### Answer 
- I will monitor the Error Rate panel that shows the percentage of error responses (4xx and 5xx) out of total requests.
- Set an alert in Grafana to notify when the error rate exceeds 30%.
- If the error rate exceeds 30%, investigate the issue, as this could indicate system instability, misconfigurations, or failures in the API.

## Define 5 Alerts for Service Monitoring

#### Question 
 Write down 5 theoretical alerts to monitor service health. Examples:
 Choose one of the alerts and describe a runbook to NOC, how to investigate and
troubleshoot the issue.

#### Answer 
1. Slow Database Queries Alert:
Condition: Trigger an alert if database query response times exceed 1000ms.

2. Failed Login Attempts Alert:
Condition: Trigger an alert if failed login attempts exceed 100 in the last 10 minutes.

3. Service Down Alert:
Condition: Trigger an alert if the service is unavailable (e.g., 500 or 503 status codes returned ).

4. API Rate Limiting Alert:
Condition: Trigger an alert if API rate limit is reached (e.g., 1000 requests per minute).

5. Resource Utilization Alert:
Condition: Trigger an alert if CPU or memory usage exceeds 90% for a given service over a 5-minute period.



Runbook for Service Down Alert
Alert Name: Service Down
Condition: Trigger an alert if the service is unresponsive (e.g., HTTP status code 5xx, no response, or constant 5xx for 5 minutes).

1. Initial Response
Alert Notification: A notification is received by the NOC team.
Message Content: Include the service name, timestamp, and specific metrics that triggered the alert.

2. Verification of the Alert
NOC will first verify if the service is indeed down.

Action Steps:

Check the Alert Dashboard: Open the service monitoring dashboard (e.g., Grafana, Prometheus) and verify the status of the service. 
Ping the Service Endpoint:
Use curl or http to send a request to the service’s endpoint (e.g., curl -I http://your-service-url).
Check the HTTP response code:
5xx error: Indicates server-side issues.


3. Gather More Contextual Data
Collect additional data to understand the scope and potential cause of the service downtime.

4. Investigate Common Causes of Downtime
Action Steps:
Look for logs indicating that the service crashed or restarted unexpectedly.

5. Troubleshooting Actions
Action Steps:

Restart the Service:
If possible, restart the service to see if it resolves the issue.

6. Post-Restoration
After resolving the issue, ensure the service is stable and operational.
Action Steps:
Confirm Service is Back Online:
Verify that the service is up and running by checking the monitoring dashboard and sending requests to the API.

7. Root Cause Analysis (RCA) and Post-Incident Review
After resolving the issue, conduct a root cause analysis to prevent future downtime.
8. Documentation and Reporting
Document all actions taken during the investigation and resolution. 
