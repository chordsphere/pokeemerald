import os
import re
import collections

def search_for_text(root_dir, text_to_search, context_lines=3):
    # Create a regular expression pattern for the text (case insensitive)
    pattern = re.compile(text_to_search, re.IGNORECASE)

    # List of file extensions to skip
    skip_extensions = ['.mid','.aif','.png','index']

    # Walk through the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Skip files with extensions in the skip list
            if any(filename.endswith(ext) for ext in skip_extensions):
                continue

            filepath = os.path.join(dirpath, filename)

            # We'll use a deque to maintain a buffer of the last few lines
            line_buffer = collections.deque(maxlen=context_lines)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    for line_no, line in enumerate(file, 1):
                        if pattern.search(line):
                            print(f"{filepath}: Line {line_no-context_lines} to {line_no + context_lines}")
                            # Print the previous lines from the buffer
                            for prev_line in line_buffer:
                                print(prev_line.strip())
                            # Print the current matched line
                            print(line.strip())
                            # Print the subsequent lines for context
                            for _ in range(context_lines):
                                print(next(file).strip())
                            print("-----")
                        # Append the current line to the buffer
                        line_buffer.append(line)
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='ISO-8859-1') as file:
                        for line_no, line in enumerate(file, 1):
                            if pattern.search(line):
                                print(f"{filepath}: Line {line_no-context_lines} to {line_no + context_lines}")
                                for prev_line in line_buffer:
                                    print(prev_line.strip())
                                print(line.strip())
                                for _ in range(context_lines):
                                    print(next(file).strip())
                                print("-----")
                            line_buffer.append(line)
                except Exception as e:
                    print(f"Error reading {filepath}. Reason: {e}")
            except Exception as e:
                print(f"Error reading {filepath}. Reason: {e}")

if __name__ == '__main__':
    root_directory = '.'  # Start from current directory
    text_to_find = 'Smeargle'
    search_for_text(root_directory, text_to_find)
