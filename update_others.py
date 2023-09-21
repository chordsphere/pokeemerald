def insert_text_into_file(filepath, line_no, text_to_insert):
    """Insert given text into a file at a specified line number."""
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Insert the text at the specified line number
    lines.insert(line_no - 1, text_to_insert)  # Adjusting for 0-indexing

    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(lines)


if __name__ == '__main__':
    # Define the modifications
    modifications = [
        {
            'filepath': './pokeemerald/sound/direct_sound_data.inc',
            'line_no': 1330,
            'text': 'Cry_Mimileech::\n\t.incbin "sound/direct_sound_samples/cries/smeargle.bin"\n\n\t.align 2\n'
        },
        {
            'filepath': './pokeemerald/sound/cry_tables.inc',
            'line_no': 238,
            'text': '\tcry Cry_Mimileech\n'
        },
        {
            'filepath': './pokeemerald/sound/cry_tables.inc',
            'line_no': 629,
            'text': '\tcry_reverse Cry_Mimileech\n'
        },
        {
            'filepath': './pokeemerald/include/constants/species.h',
            'line_no': 419,
            'text': '#define SPECIES_MIMILEECH 413\n'
        },
        {
            'filepath': './pokeemerald/src/data/pokemon/pokedex_text.h',
            'line_no': 1416,
            'text': '''const u8 gMimileechPokedexText[] = _(
    "A MIMILEECH marks its territory using a\\n"
    "fluid that leaks out from the tip of its\\n"
    "tail. About 5,000 different marks left by\\n"
    "this POKéMON have been found.");\n'''
        }
    ]

    # Apply each modification
    for mod in modifications:
        insert_text_into_file(mod['filepath'], mod['line_no'], mod['text'])
