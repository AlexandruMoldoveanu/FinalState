import re
import sys
project_name = sys.argv[1]
check = sys.argv[2]

def parse_log_file(file_path):
    errors = []
    warnings = []

    error_pattern = re.compile(r'\berror\b', re.IGNORECASE)
    warning_pattern = re.compile(r'\bwarning\b', re.IGNORECASE)

    with open(file_path, 'r') as file:
        for line in file:
            if error_pattern.search(line):
                errors.append(line.strip())
            elif warning_pattern.search(line):
                warnings.append(line.strip())
    
    return errors, warnings

def save_errors_and_warnings(errors, warnings, output_file):
    with open(output_file, 'w') as file:
        file.write("Errors ({}):\n".format(len(errors)))
        for error in errors:
            file.write(error + '\n')
        
        file.write("\nWarnings ({}):\n".format(len(warnings)))
        for warning in warnings:
            file.write(warning + '\n')

def print_file_contents(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
        print(contents)

if __name__ == "__main__":
    input_file_path = project_name + '\\result.txt'
    output_file_path = project_name + '\\parsed_results.txt'

    errors, warnings = parse_log_file(input_file_path)
    save_errors_and_warnings(errors, warnings, output_file_path)
    if sys.argv[2] == 'y':
        print_file_contents(output_file_path)