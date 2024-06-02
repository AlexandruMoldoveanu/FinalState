import sys
import subprocess
import re
import os
import shutil
project_path = ''
project_name = ''

def menu():
    while True:
        print("What do you wanna do?")
        print("1. Clone a repository")
        print("2. Clone and generate a new report")
        print("3. Open last report")
        print("4. Exit")

        choice = input("Please choose an option (1-4): ")

        if choice == '1':
            link_for_clone()
        elif choice == '2':
            link_for_clone()
            generate_report(project_path)
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
    
def link_for_clone():
    print("Provide a link for a github repository")
    link = input("Please enter a link: ")
    global project_path
    global project_name
    project_path = os.getcwd()
    match = re.search(r'/([^/]+)\.git$', link)
    if match:
        project_name = match.group(1)
        project_path = project_path + '\\' + project_name
    else:
        print("Your repo name was wrong")
    print(f"You entered: {link}")
    
    if os.path.exists(project_path):
        try:
            shutil.rmtree(project_path, onerror=remove_readonly)
            print(f"Deleted directory: {project_path}")
        except PermissionError as e:
            print(f"PermissionError: {e}")
    else:
        print(f"Directory does not exist: {project_path}")
    
    subprocess.run(['git', 'clone', link], check=True)

def generate_report(project_path):
    cppcheck_cmd = [
        'cppcheck',
        '--enable=all',
        '--inconclusive',
        '--std=c++11',
        project_path
    ]
    
    output_file = project_path + '\\result.txt'
    
    with open(output_file, 'w') as file:
        subprocess.run(cppcheck_cmd, stderr=file)

def print_results():
    choice = input("Do you wanna see the result? Please respons with 'y' or 'n'. ")
    if choice == 'y':
        subprocess.run(['python', 'Parser.py', project_name ,'y'])
    if choice == 'n':
        subprocess.run(['python', 'Parser.py', project_name ,'n'])
    
def open_test_report():
    choice = input("Please provide name of repo: ")
    subprocess.run(['python', 'Parser.py', choice ,'y'])

if __name__ == "__main__":
    menu()

