"""This module provides functions to clone repositories, generate reports, and manage project files."""

import sys
import subprocess
import re
import os
import shutil
import argparse
import glob

PROJECT_PATH = ''
PROJECT_NAME = ''

def menu():
    """Displays the main menu and handles user choices."""
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('param1', nargs='?', help='First parameter')
    args = parser.parse_args()
    if args.param1:
        link_for_clone(args.param1)
        generate_report()
    else:
        while True:
            print("What do you want to do?")
            print("1. Clone a repository")
            print("2. Clone a repository and generate a new report for all listed projects")
            print("3. Open last report for all listed projects")
            print("4. Exit")

            choice = input("Please choose an option (1-4): ")

            if choice == '1':
                link = input("Please enter a link: ")
                link_for_clone(link)
            elif choice == '2':
                link = input("Please enter a link: ")
                link_for_clone(link)
                generate_report()
                print_results()
            elif choice == '3':
                open_test_report()
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice, please choose again.")

def remove_readonly(func, path, _excinfo):
    """Removes readonly attribute from files."""
    os.chmod(path, 0o777)
    func(path)

def link_for_clone(link):
    """Clones the repository from the given link."""
    global PROJECT_PATH
    global PROJECT_NAME
    PROJECT_PATH = os.getcwd()
    match = re.search(r'^https://github\.com/[^/]+/[^/]+\.git$', link)
    if match:
        project_name_match = re.search(r'/([^/]+)\.git$', link)
        if project_name_match:
            PROJECT_NAME = project_name_match.group(1)
            PROJECT_PATH = os.path.join(PROJECT_PATH, PROJECT_NAME)
            if os.path.exists(PROJECT_PATH):
                try:
                    shutil.rmtree(PROJECT_PATH, onerror=remove_readonly)
                    print(f"Deleted directory: {PROJECT_PATH}")
                except PermissionError as e:
                    print(f"PermissionError: {e}")
            subprocess.run(['git', 'clone', link], check=True)
        else:
            print("Failed to extract project name from link")
            sys.exit(1)
    else:
        print("Your repo link was wrong")
        sys.exit(0)
    print(f"You entered: {link}")

def delete_old_files(directory):
    """Deletes old files with '_old.txt' suffix in the given directory."""
    old_files = glob.glob(os.path.join(directory, '*_old.txt'))
    for file in old_files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except OSError as e:
            print(f"Error deleting file {file}: {e}")

def rename_old_reports():
    """Renames old reports to include '_old.txt' suffix."""
    old_result = os.path.join(PROJECT_PATH, 'result.txt')
    old_parsed_result = os.path.join(PROJECT_PATH, 'parsed_results.txt')
    delete_old_files(PROJECT_PATH)
    if os.path.exists(old_result):
        new_result_name = old_result.replace('.txt', '_old.txt')
        if os.path.exists(new_result_name):
            os.remove(new_result_name)
        shutil.move(old_result, new_result_name)
        print(f"Renamed {old_result} to {new_result_name}")
        
    if os.path.exists(old_parsed_result):
        new_parsed_result_name = old_parsed_result.replace('.txt', '_old.txt')
        if os.path.exists(new_parsed_result_name):
            os.remove(new_parsed_result_name)
        shutil.move(old_parsed_result, new_parsed_result_name)
        print(f"Renamed {old_parsed_result} to {new_parsed_result_name}")

def generate_report():
    """Generates a new report for the project."""
    rename_old_reports()
    
    cppcheck_cmd = [
        'cppcheck',
        '--enable=all',
        '--inconclusive',
        '--std=c++11',
        PROJECT_PATH
    ]
    
    output_file = os.path.join(PROJECT_PATH, 'result.txt')
    output_file_parsed = os.path.join(PROJECT_PATH, 'parsed_results.txt')
    
    with open(output_file, 'w', encoding='utf-8') as file:
        subprocess.run(cppcheck_cmd, stderr=file, check=True)
        
    with open(output_file_parsed, 'w', encoding='utf-8') as file:
        subprocess.run(['python', 'Parser.py', PROJECT_NAME, 'n'], check=True)

def print_results():
    """Prompts the user to see the results and prints them."""
    choice = input("Do you wanna see the result? Please respond with 'y' or 'n'. ")
    if choice == 'y':
        subprocess.run(['python', 'Parser.py', PROJECT_NAME, 'y'], check=True)
    elif choice == 'n':
        subprocess.run(['python', 'Parser.py', PROJECT_NAME, 'n'], check=True)
    else:
        print("Invalid choice, please choose again.")
        print_results()

def open_test_report():
    """Opens the test report for a specified repository."""
    choice = input("Please provide name of repo: ")
    subprocess.run(['python', 'Parser.py', choice, 'y'], check=True)

if __name__ == "__main__":
    menu()
