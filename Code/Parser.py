import re
import sys
import os
import subprocess

project_name = sys.argv[1]
check = sys.argv[2]

def parse_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            errors = []
            warnings = []
            information = []
            style = []
            notes = []
            error_pattern = re.compile(r'\berror\b', re.IGNORECASE)
            warning_pattern = re.compile(r'\bwarning\b', re.IGNORECASE)
            information_pattern = re.compile(r'\binformation\b', re.IGNORECASE)
            style_pattern = re.compile(r'\bstyle\b', re.IGNORECASE)
            note_pattern = re.compile(r'\bnote\b', re.IGNORECASE)
            
            with open(file_path, 'r') as file:
                for line in file:
                    if error_pattern.search(line):
                        errors.append(line.strip())
                    elif warning_pattern.search(line):
                        warnings.append(line.strip())
                    elif information_pattern.search(line):
                        information.append(line.strip())
                    elif style_pattern.search(line):
                        style.append(line.strip())
                    elif note_pattern.search(line):
                        notes.append(line.strip())
            
            return errors, warnings, information, style, notes
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
        return [], [], [], [], []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [], [], [], [], []

def save_results(errors, warnings, information, style, notes, output_file):
    if not errors and not warnings and not information and not style and not notes:
        print(f"No results to save in {output_file}")
        return

    with open(output_file, 'w') as file:
        file.write("Errors ({}):\n".format(len(errors)))
        for error in errors:
            file.write(error + '\n')

        file.write("\nWarnings ({}):\n".format(len(warnings)))
        for warning in warnings:
            file.write(warning + '\n')

        file.write("\nInformation ({}):\n".format(len(information)))
        for info in information:
            file.write(info + '\n')

        file.write("\nStyle ({}):\n".format(len(style)))
        for st in style:
            file.write(st + '\n')

        file.write("\nNotes ({}):\n".format(len(notes)))
        for note in notes:
            file.write(note + '\n')

def print_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def compare_results(new_counts, old_counts):
    diff_threshold = 0.1
    for key in new_counts:
        if key in old_counts:
            diff = new_counts[key] - old_counts[key]
            if old_counts[key] > 0 and diff / old_counts[key] > diff_threshold:
                raise ValueError(f"{key.capitalize()} increased by more than 10%")

def get_counts(file_path):
    counts = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('Errors'):
                    counts['errors'] = int(re.search(r'\((\d+)\)', line).group(1))
                elif line.startswith('Warnings'):
                    counts['warnings'] = int(re.search(r'\((\d+)\)', line).group(1))
                elif line.startswith('Information'):
                    counts['information'] = int(re.search(r'\((\d+)\)', line).group(1))
                elif line.startswith('Style'):
                    counts['style'] = int(re.search(r'\((\d+)\)', line).group(1))
                elif line.startswith('Notes'):
                    counts['notes'] = int(re.search(r'\((\d+)\)', line).group(1))
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return counts

if __name__ == "__main__":
    input_file_path = project_name + '\\result.txt'
    output_file_path = project_name + '\\parsed_results.txt'
    old_file_path = project_name + '\\parsed_results_old.txt'

    errors, warnings, information, style, notes = parse_log_file(input_file_path)
    save_results(errors, warnings, information, style, notes, output_file_path)

    if check == 'y':
        print_file_contents(output_file_path)

    if os.path.exists(old_file_path):
        new_counts = get_counts(output_file_path)
        old_counts = get_counts(old_file_path)
        compare_results(new_counts, old_counts)

    subprocess.run(['python', 'Influx.py'])