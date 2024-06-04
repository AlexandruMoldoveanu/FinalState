from prometheus_client import start_http_server, Gauge
import time

# Define Prometheus metrics
cppcheck_errors = Gauge('cppcheck_errors', 'Number of Cppcheck errors')
cppcheck_warnings = Gauge('cppcheck_warnings', 'Number of Cppcheck warnings')
cppcheck_performance = Gauge('cppcheck_performance', 'Number of Cppcheck performance issues')
cppcheck_style = Gauge('cppcheck_style', 'Number of Cppcheck style issues')

def parse_cppcheck_results(file_path):
    errors = warnings = performance_issues = style_issues = 0
    with open(file_path, 'r') as file:
        for line in file:
            if 'error' in line:
                errors += 1
            elif 'warning' in line:
                warnings += 1
            elif 'performance' in line:
                performance_issues += 1
            elif 'style' in line:
                style_issues += 1
    return errors, warnings, performance_issues, style_issues

def update_metrics():
    errors, warnings, performance_issues, style_issues = parse_cppcheck_results('Result/result_Adaptive-AUTOSAR.txt')
    cppcheck_errors.set(errors)
    cppcheck_warnings.set(warnings)
    cppcheck_performance.set(performance_issues)
    cppcheck_style.set(style_issues)

if __name__ == '__main__':
    try:
        # Start up the server to expose the metrics
        start_http_server(9090)
        print("Prometheus metrics server started on port 9090")
    except Exception as e:
        print(f"Error starting Prometheus server: {e}")
    while True:
        update_metrics()
        time.sleep(30)