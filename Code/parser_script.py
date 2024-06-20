"""This module parses log files, saves results, and manages project files."""

import re
import sys
import os
import subprocess


def parse_log_file(file_path):
    """Parses the log file and extracts errors, warnings, information, style issues, and notes."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            errors_list = []
            warnings_list = []
            info_list = []
            style_list = []
            notes_list = []
            error_pattern = re.compile(r'\berror\b', re.IGNORECASE)
            warning_pattern = re.compile(r'\bwarning\b', re.IGNORECASE)
            info_pattern = re.compile(r'\binformation\b', re.IGNORECASE)
            style_pattern = re.compile(r'\bstyle\b', re.IGNORECASE)
            note_pattern = re.compile(r'\bnote\b', re.IGNORECASE)

            for line in file:
                if error_pattern.search(line):
                    errors_list.append(line.strip())
                elif warning_pattern.search(line):
                    warnings_list.append(line.strip())
                elif info_pattern.search(line):
                    info_list.append(line.strip())
                elif style_pattern.search(line):
                    style_list.append(line.strip())
                elif note_pattern.search(line):
                    notes_list.append(line.strip())

            return errors_list, warnings_list, info_list, style_list, notes_list
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
        return [], [], [], [], []
    except OSError as e:
        print(f"An OS error occurred: {e}")
        return [], [], [], [], []


def save_results(errors_list, warnings_list, info_list, style_list, notes_list, output_file):
    """Saves the parsed results to an output file."""
    if os.path.exists(output_file):
        old_output_file = output_file.replace(".txt", "_old.txt")

        if os.path.exists(old_output_file):
            os.remove(old_output_file)

        os.rename(output_file, old_output_file)

    if not errors_list and not warnings_list and not info_list and not style_list and not notes_list:
        print(f"No results to save in {output_file}")
        return

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"Errors ({len(errors_list)}):\n")
        for error in errors_list:
            file.write(error + '\n')

        file.write(f"\nWarnings ({len(warnings_list)}):\n")
        for warning in warnings_list:
            file.write(warning + '\n')

        file.write(f"\nInformation ({len(info_list)}):\n")
        for info in info_list:
            file.write(info + '\n')

        file.write(f"\nStyle ({len(style_list)}):\n")
        for style in style_list:
            file.write(style + '\n')

        file.write(f"\nNotes ({len(notes_list)}):\n")
        for note in notes_list:
            file.write(note + '\n')


def print_file_contents(file_path):
    """Prints the contents of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
    except OSError as e:
        print(f"An OS error occurred: {e}")


if __name__ == "__main__":
    """Main entry point of the script."""
    project_name = sys.argv[1]
    check = sys.argv[2]

    input_file_path = os.path.join(project_name, 'result.txt')
    current_directory = os.getcwd()
    target_dir = os.path.abspath(os.path.join(current_directory, 'Result'))
    output_file_path = os.path.join(target_dir, f'{project_name}_parsed_results.txt')

    errors, warnings, information, style, notes = parse_log_file(input_file_path)
    save_results(errors, warnings, information, style, notes, output_file_path)
    
    subprocess.run(['python', 'influx_script.py'], check=True)
    
    if os.path.exists(output_file_path):
        try:
            subprocess.run(['python', 'validate_script.py', output_file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running Validate.py: {e}")
    else:
        print(f"Error: The file {output_file_path} does not exist.")
