"""
Module for collecting and sending metrics to InfluxDB.
"""

import os
import time
import logging
import sys
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = "HlPHg1DNzy7WWijgwOjqvwVfDi74Be9M63LTe_hen3IGainaEbs5dpxcCIsmTjaU0IGP1M5FUH7DirtvxneW2w=="
ORG = "work"
BUCKET = "work"
URL = "http://localhost:8086"

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def check_file_exists(path):
    """Checks if the results file exists."""
    return os.path.exists(path)

def collect_results_from_file(path):
    """Collects and parses results from the specified file."""
    if not os.path.isfile(path):
        print(f"Path {path} is not a file.")
        return None

    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    errors_count = extract_count(content, 'Errors')
    warnings_count = extract_count(content, 'Warnings')
    information_count = extract_count(content, 'Information')
    style_count = extract_count(content, 'Style')
    notes_count = extract_count(content, 'Notes')

    return {
        'Errors': errors_count,
        'Warnings': warnings_count,
        'Information': information_count,
        'Style': style_count,
        'Notes': notes_count
    }

def extract_count(content, section_name):
    """Extracts the count of a specific section from the content."""
    section_header = f"{section_name} ("
    start_index = content.find(section_header)
    if start_index == -1:
        return 0

    start_index += len(section_header)
    end_index = content.find(')', start_index)
    if end_index == -1:
        return 0

    count_str = content[start_index:end_index]
    try:
        count = int(count_str)
    except ValueError:
        count = 0

    return count

def parse_result_file(file_path):
    """Compares new results with old results and prints the differences."""
    if not check_file_exists(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)
    
    results = collect_results_from_file(file_path)
    if results is None:
        return 0, 0, 0, 0, 0
    
    return (
        results['Errors'], 
        results['Warnings'], 
        results['Information'], 
        results['Style'], 
        results['Notes']
    )

def send_metrics_to_influxdb(file, errors, warnings, info, style, notes):
    """Sends the collected metrics to InfluxDB."""
    try:
        line_protocol = (
            f'cppcheck,host=host1,file={file} errors={errors},warnings={warnings},'
            f'information={info},style={style},notes={notes} {int(time.time())}000000000'
        )
        write_api.write(bucket=BUCKET, org=ORG, record=line_protocol)
        logging.info(
            "Sent metrics to InfluxDB: File=%s, Errors=%d, Warnings=%d, Information=%d, Style=%d, Notes=%d", 
            file, errors, warnings, info, style, notes
        )
    except Exception as e:
        logging.error("Error writing to InfluxDB: %s", e)

if __name__ == '__main__':
    RESULT_DIRECTORY = 'Result'
    if not os.path.exists(RESULT_DIRECTORY):
        logging.error("Directory '%s' does not exist.", RESULT_DIRECTORY)
        sys.exit(1)
    
    for result_file in os.listdir(RESULT_DIRECTORY):
        if result_file.endswith('parsed_results.txt'):
            file_path = os.path.join(RESULT_DIRECTORY, result_file)
            errors, warnings, info, style, notes = parse_result_file(file_path)
            logging.info(
                "Parsed metrics from %s: Errors=%d, Warnings=%d, Information=%d, Style=%d, Notes=%d", 
                result_file, errors, warnings, info, style, notes
            )
            send_metrics_to_influxdb(result_file, errors, warnings, info, style, notes)
