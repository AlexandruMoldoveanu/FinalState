import sys
import subprocess
import re
import os
import shutil
import argparse
import glob

project_path = ''
project_name = ''

def menu():
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('param1', nargs='?', help='First parameter')
    args = parser.parse_args()
    if args.param1:
        link_for_clone(args.param1)
        generate_report()
    else:
        while True:
            print("What do you wanna do?")
            print("1. Clone a repository")
            print("2. Clone and generate a new report")
            print("3. Open last report")
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

def remove_readonly(func, path, excinfo):
    os.chmod(path, 0o777)
    func(path)

def link_for_clone(link):
    global project_path
    global project_name
    project_path = os.getcwd()
    match = re.search(r'^https://github\.com/[^/]+/[^/]+\.git$', link)
    if match:
        project_name_match = re.search(r'/([^/]+)\.git$', link)
        if project_name_match:
            project_name = project_name_match.group(1)
            project_path = os.path.join(project_path, project_name)
            if os.path.exists(project_path):
                try:
                    shutil.rmtree(project_path, onerror=remove_readonly)
                    print(f"Deleted directory: {project_path}")
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
    old_files = glob.glob(os.path.join(directory, '*_old.txt'))
    for file in old_files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except OSError as e:
            print(f"Error deleting file {file}: {e}")
            
def rename_old_reports():
    old_result = os.path.join(project_path, 'result.txt')
    old_parsed_result = os.path.join(project_path, 'parsed_results.txt')
    delete_old_files(project_path)
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
    rename_old_reports()
    
    cppcheck_cmd = [
        'cppcheck',
        '--enable=all',
        '--inconclusive',
        '--std=c++11',
        project_path
    ]
    
    output_file = project_path + '\\result.txt'
    output_file_parsed = project_path + '\\parsed_results.txt'
    
    with open(output_file, 'w') as file:
        subprocess.run(cppcheck_cmd, stderr=file)
        
    with open(output_file_parsed, 'w') as file:
        subprocess.run(['python', 'Parser.py', project_name, 'n'])

def print_results():
    choice = input("Do you wanna see the result? Please respond with 'y' or 'n'. ")
    if choice == 'y':
        subprocess.run(['python', 'Parser.py', project_name, 'y'])
    else
    if choice == 'n':
        subprocess.run(['python', 'Parser.py', project_name, 'n'])
    else
        print("Invalid choice, please choose again.")
        print_results()

def open_test_report():
    choice = input("Please provide name of repo: ")
    subprocess.run(['python', 'Parser.py', choice, 'y'])

if __name__ == "__main__":
    menu()
