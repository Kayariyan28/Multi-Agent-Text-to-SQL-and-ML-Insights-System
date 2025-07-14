from prometheus_client import Counter, start_http_server
from langsmith import Client

ls_client = Client()

request_counter = Counter('requests_total', 'Total requests')

def log_drift(result_df):
    # Use Evidently for drift
    from evidently.report import Report
    report = Report(metrics=[...])
    # ...
