import os
import re
import csv

def insert_or_replace_line_in_file(filepath, line_no, new_line):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Replace the desired line
    lines[line_no - 1] = new_line

    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def process_files():
    # Insert or replace lines in specified files
    insert_or_replace_line_in_file('./pokeemerald/include/constants/species.h', 421, "#define NUM_SPECIES 414\n")
    insert_or_replace_line_in_file('./pokeemerald/src/starter_choose.c', 116, "    SPECIES_MIMILEECH,\n")
    insert_or_replace_line_in_file('./pokeemerald/src/data/pokemon/pokedex_entries.h', 2829, "\n")

if __name__ == '__main__':
    process_files()
