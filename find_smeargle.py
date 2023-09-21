import csv
import re
import os

def replace_text_in_file(filepath, start_line_no, original_lines, new_lines):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Insert the new lines immediately after the original segment
    insert_pos = start_line_no + len(original_lines) - 1
    for idx, new_line in enumerate(new_lines):
        lines.insert(insert_pos + idx, new_line)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    return True


def replace_smeargle_with_mimileech(match):
    word = match.group()
    if word == 'SMEARGLE':
        return 'MIMILEECH'
    elif word == 'Smeargle':
        return 'Mimileech'
    else:
        return 'mimileech'

def get_lines_until_next_brace(filepath, start_line_no,brace_count):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    segment = [lines[start_line_no-1]]  # Start with the first line
    for line in lines[start_line_no:]:
        segment.append(line)
        brace_count += line.count('{') - line.count('}')
        if brace_count == 0:
            break
    return segment





def process_csv(csv_file):
    unsuccessful_replacements = []
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filepath, line_no, line_text = row['Filepath'], int(row['Line Number']), row['Line Text']
            was_replaced = False

            if line_text.endswith(",") or line_text.endswith(";"):
                new_text = re.sub(r'(smeargle|Smeargle|SMEARGLE)', replace_smeargle_with_mimileech, line_text)
                new_line_text = new_text + '\n'  # directly append newline to the processed line
                was_replaced = replace_text_in_file(filepath, line_no, [line_text], [new_line_text])

            elif line_text.strip().endswith('{'):
                segment = get_lines_until_next_brace(filepath, line_no,line_text.strip().count("{"))
                modified_segment = [re.sub(r'(smeargle|Smeargle|SMEARGLE)', replace_smeargle_with_mimileech, line) for line in segment]
                was_replaced = replace_text_in_file(filepath, line_no, segment, modified_segment)
            elif line_text.strip().endswith('='):
                segment = get_lines_until_next_brace(filepath, line_no,line_text.strip().count("{"))
                modified_segment = [re.sub(r'(smeargle|Smeargle|SMEARGLE)', replace_smeargle_with_mimileech, line) for line in segment]
                was_replaced = replace_text_in_file(filepath, line_no, segment, modified_segment)


            if not was_replaced:
                unsuccessful_replacements.append(row)

    # Overwrite results.csv with unsuccessful replacements
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Filepath', 'Line Number', 'Line Text'])
        writer.writeheader()
        for row in unsuccessful_replacements:
            writer.writerow(row)

if __name__ == '__main__':
    process_csv('results.csv')
