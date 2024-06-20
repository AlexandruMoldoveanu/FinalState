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
    if os.path.exists(output_file):
        old_output_file = output_file.replace(".txt", "_old.txt")

        if os.path.exists(old_output_file):
            os.remove(old_output_file)

        os.rename(output_file, old_output_file)
        
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

if __name__ == "__main__":
    input_file_path = project_name + '\\result.txt'
    current_directory = os.getcwd()
    target_dir = os.path.abspath(os.path.join(current_directory, 'Result'))
    output_file_path = target_dir + '\\'+ project_name + '_parsed_results.txt'

    errors, warnings, information, style, notes = parse_log_file(input_file_path)
    save_results(errors, warnings, information, style, notes, output_file_path)
    subprocess.run(['python', 'Validate.py', output_file_path])
