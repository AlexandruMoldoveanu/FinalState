import sys
import subprocess
import re
import os
import shutil
project_path = ''

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
        elif choice == '3':
            open_test_report()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please choose again.")

def link_for_clone():
    print("Provide a link for a github repository")
    link = input("Please enter a link: ")
    global project_path
    project_path = os.getcwd()
    project_name = project_path
    match = re.search(r'/([^/]+)\.git$', link)
    if match:
        project_path = project_path + '\\' + match.group(1)
        if os.path.exists(match.group(1)):
            shutil.rmtree(match.group(1))
            print(f"Folder '{match.group(1)}' deleted.")
        else:
            print(f"Folder '{match.group(1)}' does not exist.")
    else:
        print("Your repo name was wrong")
    print(f"You entered: {link}")
    print({project_path})
    subprocess.run(['git', 'clone', link], check=True)
    print("your repository was cloned")

def generate_report(project_path):
    print("AICI2")
    cppcheck_cmd = [
        'cppcheck',
        '--enable=all',
        '--inconclusive',
        '--std=c++11',
        project_path
    ]
    
    output_file = 'result.txt'
    
    with open(output_file, 'w') as file:
        subprocess.run(cppcheck_cmd, stderr=file)

def open_test_report():
    choice = input("Please provide name of repo")

if __name__ == "__main__":
    menu()

