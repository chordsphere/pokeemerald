import os
import re
import csv

def search_for_text(root_dir, text_to_search, output_csv):
    # Create a regular expression pattern for the text (case insensitive)
    pattern = re.compile(text_to_search, re.IGNORECASE)

    # List of file extensions to skip
    skip_extensions = ['.mid','.aif','.png','index','.json','frontier_trainer_mons.h','frontier_mons.h','trainer_hill.h']

    # Prepare to write results to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filepath', 'Line Number', 'Line Text'])

        # Walk through the root directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                # Skip files with extensions in the skip list
                if any(filename.endswith(ext) for ext in skip_extensions):
                    continue
                
                filepath = os.path.join(dirpath, filename)
                try:
                    # Open each file and check each line for the text
                    with open(filepath, 'r', encoding='utf-8') as file:
                        for line_no, line in enumerate(file, 1):
                            if pattern.search(line):
                                csvwriter.writerow([filepath, line_no, line.rstrip('\n')])
                except UnicodeDecodeError:
                    # If the file isn't UTF-8 encoded, try reading it with ISO-8859-1 (Latin-1) encoding
                    try:
                        with open(filepath, 'r', encoding='ISO-8859-1') as file:
                            for line_no, line in enumerate(file, 1):
                                if pattern.search(line):
                                    csvwriter.writerow([filepath, line_no, line.rstrip('\n')])
                    except Exception as e:
                        print(f"Error reading {filepath}. Reason: {e}")
                except Exception as e:
                    # Handle other possible exceptions
                    print(f"Error reading {filepath}. Reason: {e}")

if __name__ == '__main__':
    root_directory = './pokeemerald'  # Start from current directory
    text_to_find = 'Smeargle'
    output_csv_file = 'results.csv'  # Name of the CSV file to write the results to
    search_for_text(root_directory, text_to_find, output_csv_file)
