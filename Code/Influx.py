"""This module parses result files and sends metrics to InfluxDB."""

import time
import os
import logging
from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = "HlPHg1DNzy7WWijgwOjqvwVfDi74Be9M63LTe_hen3IGainaEbs5dpxcCIsmTjaU0IGP1M5FUH7DirtvxneW2w=="
ORG = "work"
BUCKET = "work"
URL = "http://localhost:8086"

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def parse_result_file(file_path):
    """Parses the result file and counts errors, warnings, information, style issues, and notes."""
    error_count = warning_count = info_count = style_count = note_count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if 'error' in line.lower():
                    error_count += 1
                elif 'warning' in line.lower():
                    warning_count += 1
                elif 'information' in line.lower():
                    info_count += 1
                elif 'style' in line.lower():
                    style_count += 1
                elif 'note' in line.lower():
                    note_count += 1
    except FileNotFoundError:
        logging.error("Error: The file at %s does not exist.", file_path)
    except OSError as e:
        logging.error("OS error occurred: %s", e)
    except Exception as e:  # pylint: disable=broad-except
        logging.error("An unexpected error occurred while reading the file: %s", e)
    return error_count, warning_count, info_count, style_count, note_count

def send_metrics_to_influxdb(file_name, error_count, warning_count, info_count, style_count, note_count):
    """Sends the parsed metrics to InfluxDB."""
    try:
        line_protocol = (
            f'cppcheck,host=host1,file={file_name} '
            f'errors={error_count},warnings={warning_count},information={info_count},'
            f'style={style_count},notes={note_count} {int(time.time())}000000000'
        )
        write_api.write(bucket=BUCKET, org=ORG, record=line_protocol)
        logging.info(
            "Sent metrics to InfluxDB: File=%s, Errors=%d, Warnings=%d, Information=%d, Style=%d, Notes=%d",
            file_name, error_count, warning_count, info_count, style_count, note_count
        )
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Error writing to InfluxDB: %s", e)

if __name__ == '__main__':
    result_directory = 'Result'
    if not os.path.exists(result_directory):
        logging.error("Directory '%s' does not exist.", result_directory)
        os._exit(1)  # pylint: disable=protected-access

    for file_name in os.listdir(result_directory):
        if file_name.startswith('result_') and file_name.endswith('.txt'):
            file_path = os.path.join(result_directory, file_name)
            errors, warnings, information, style, notes = parse_result_file(file_path)
            logging.info(
                "Parsed metrics from %s: Errors=%d, Warnings=%d, Information=%d, Style=%d, Notes=%d",
                file_name, errors, warnings, information, style, notes
            )
            send_metrics_to_influxdb(file_name, errors, warnings, information, style, notes)
