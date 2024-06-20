import os
import sys

def check_old_file_exists(old_file_path):
    return os.path.exists(old_file_path)

def collect_results_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return None
    
    if not os.path.isfile(file_path):
        print(f"Path {file_path} is not a file.")
        return None

    with open(file_path, 'r') as file:
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

def compare_results(new_file_path, old_file_path):
    if check_old_file_exists(old_file_path):
        new_results = collect_results_from_file(new_file_path)
        old_results = collect_results_from_file(old_file_path)

        if new_results and old_results:
            for key in new_results:
                print(f"{key}: {new_results[key]} (new) vs {old_results[key]} (old)")

            # Verificări suplimentare
            error_increase = new_results['Errors'] - old_results['Errors']
            warning_increase = new_results['Warnings'] - old_results['Warnings']
            info_increase = new_results['Information'] - old_results['Information']
            style_increase = new_results['Style'] - old_results['Style']
            notes_increase = new_results['Notes'] - old_results['Notes']

            if error_increase >= 1:
                print(f"Error count increased by {error_increase}.")
                if warning_increase / old_results['Warnings'] >= 0.10:
                    print(f"Warning count increased by at least 10%.")
                    if info_increase > 5:
                        print(f"Information count increased by more than 5.")
                        if style_increase > 20:
                            print(f"Style issues count increased by more than 20.")
                            if notes_increase > 10:
                                print(f"Notes count increased by more than 10.")
                                sys.exit(1)
                            sys.exit(1)
                        sys.exit(1)
                    sys.exit(1)
                sys.exit(1)
                    
    else:
        print(f"Old file {old_file_path} does not exist.")
        sys.exit(1)

def extract_count(content, section_name):
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
    # Verifică dacă a fost primit un parametru din linia de comandă
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_parsed_results.txt>")
        sys.exit(1)

    new_file_path = sys.argv[1]

    # Afișează valoarea primită ca parametru
    print(f"Valoare este {new_file_path}")

    # Construiește calea absolută pentru fișierul nou
    new_file_path = os.path.abspath(new_file_path)

    # Verifică și afișează calea corectă pentru fișierul primit
    if not os.path.isfile(new_file_path):
        print(f"The provided path {new_file_path} is not a valid file.")
        sys.exit(1)

    # Construiește calea pentru fișierul vechi
    base_dir = os.path.dirname(new_file_path)
    new_file_name = os.path.basename(new_file_path)
    old_file_name = os.path.splitext(new_file_name)[0] + "_old.txt"
    old_file_path = os.path.join(base_dir, old_file_name)

    # Apelează funcția pentru a verifica și compara rezultatele
    compare_results(new_file_path, old_file_path)
