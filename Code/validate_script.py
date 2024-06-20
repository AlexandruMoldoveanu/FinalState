"""This module validates and compares results from log parsing."""

import os
import sys


def check_old_file_exists(path):
    """Checks if the old results file exists."""
    return os.path.exists(path)


def collect_results_from_file(path):
    """Collects and parses results from the specified file."""
    if not os.path.exists(path):
        print(f"File {path} does not exist.")
        return None

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


def compare_results(new_path, old_path):
    """Compares new results with old results and prints the differences."""
    if not check_old_file_exists(old_path):
        print(f"Old file {old_path} does not exist.")
        sys.exit(1)

    new_results = collect_results_from_file(new_path)
    old_results = collect_results_from_file(old_path)

    if new_results and old_results:
        for key in new_results:
            print(f"{key}: {new_results[key]} (new) vs {old_results[key]} (old)")

        error_increase = new_results['Errors'] - old_results['Errors']
        warning_increase = new_results['Warnings'] - old_results['Warnings']
        info_increase = new_results['Information'] - old_results['Information']
        style_increase = new_results['Style'] - old_results['Style']
        notes_increase = new_results['Notes'] - old_results['Notes']

        if (error_increase >= 1 or
                (warning_increase >= 1 and warning_increase / old_results['Warnings'] >= 0.10) or
                info_increase > 5 or
                style_increase > 20 or
                notes_increase > 10):
            sys.exit(1)


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


if __name__ == "__main__":
    """Main entry point of the script."""
    if len(sys.argv) != 2:
        print("Usage: python validate.py <path_to_parsed_results.txt>")
        sys.exit(1)

    new_file_path = sys.argv[1]

    new_file_path = os.path.abspath(new_file_path)

    if not os.path.isfile(new_file_path):
        print(f"The provided path {new_file_path} is not a valid file.")
        sys.exit(1)

    base_dir = os.path.dirname(new_file_path)
    new_file_name = os.path.basename(new_file_path)
    old_file_name = os.path.splitext(new_file_name)[0] + "_old.txt"
    old_file_path = os.path.join(base_dir, old_file_name)

    compare_results(new_file_path, old_file_path)
