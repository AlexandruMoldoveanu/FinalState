from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

token = "HlPHg1DNzy7WWijgwOjqvwVfDi74Be9M63LTe_hen3IGainaEbs5dpxcCIsmTjaU0IGP1M5FUH7DirtvxneW2w=="
org = "work"
bucket = "work"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
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
        logging.error(f"Error: The file at {file_path} does not exist.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the file: {e}")
    return errors, warnings, information, style, notes

def send_metrics_to_influxdb(file_name, errors, warnings, information, style, notes):
    try:
        line_protocol = f'cppcheck,host=host1,file={file_name} errors={errors},warnings={warnings},information={information},style={style},notes={notes} {int(time.time())}000000000'
        write_api.write(bucket=bucket, org=org, record=line_protocol)
        logging.info(f"Sent metrics to InfluxDB: File={file_name}, Errors={errors}, Warnings={warnings}, Information={information}, Style={style}, Notes={notes}")
    except Exception as e:
        logging.error(f"Error writing to InfluxDB: {e}")

if __name__ == '__main__':
    result_directory = 'Result'
    if not os.path.exists(result_directory):
        logging.error(f"Directory '{result_directory}' does not exist.")
        exit(1)

    for file_name in os.listdir(result_directory):
        if file_name.startswith('result_') and file_name.endswith('.txt'):
            file_path = os.path.join(result_directory, file_name)
            errors, warnings, information, style, notes = parse_result_file(file_path)
            logging.info(f"Parsed metrics from {file_name}: Errors={errors}, Warnings={warnings}, Information={information}, Style={style}, Notes={notes}")
            send_metrics_to_influxdb(file_name, errors, warnings, information, style, notes)
