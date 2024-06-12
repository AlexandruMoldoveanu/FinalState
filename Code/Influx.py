from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time

token = "ot6jfAlHGEkz-9y9-J0jZwGaELSr9Ina2DknHZJFXRjs-5ZS80uE4aqRlJDS_HeA9x1AlsNispWAtWGASyXTcQ=="
org = "work"
bucket = "work"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

def parse_result_file(file_path):
    errors = warnings = information = style = notes = 0
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if 'error' in line.lower():
                    errors += 1
                elif 'warning' in line.lower():
                    warnings += 1
                elif 'information' in line.lower():
                    information += 1
                elif 'style' in line.lower():
                    style += 1
                elif 'note' in line.lower():
                    notes += 1
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
    return errors, warnings, information, style, notes

def send_metrics_to_influxdb(errors, warnings, information, style, notes, filename):
    try:
        point = Point("cppcheck")\
            .tag("file", filename)\
            .field("errors", errors)\
            .field("warnings", warnings)\
            .field("information", information)\
            .field("style", style)\
            .field("notes", notes)\
            .time(time.time(), WritePrecision.S)
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Sent metrics to InfluxDB: Errors={errors}, Warnings={warnings}, Information={information}, Style={style}, Notes={notes}")
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")

if __name__ == '__main__':
    result_dir = 'Result'
    while True:
        for filename in os.listdir(result_dir):
            if filename.startswith('result_') and filename.endswith('.txt'):
                file_path = os.path.join(result_dir, filename)
                errors, warnings, information, style, notes = parse_result_file(file_path)
                print(f"Parsed metrics from {filename}: Errors={errors}, Warnings={warnings}, Information={information}, Style={style}, Notes={notes}")
                send_metrics_to_influxdb(errors, warnings, information, style, notes, filename)
        time.sleep(30)
