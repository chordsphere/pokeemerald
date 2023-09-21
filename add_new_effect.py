import re
import os

def get_last_byte_id(filename):
    """Get the last used byte ID from the battle_script.inc file."""
    with open(filename, 'r') as file:
        data = file.read()

    matches = re.findall(r'\.byte (0x[0-9a-fA-F]+)', data)
    if not matches:
        raise ValueError(f"No .byte directive found in {filename}")

    return matches[-1]

def get_num_effects(filename):
    """Get the value after NUM_BATTLE_MOVE_EFFECTS from battle_move_effects.h."""
    with open(filename, 'r') as file:
        data = file.read()

    match = re.search(r'NUM_BATTLE_MOVE_EFFECTS\s+(\d+)', data)
    if not match:
        raise ValueError(f"NUM_BATTLE_MOVE_EFFECTS not found in {filename}")

    return int(match.group(1))

def main():
    filename = './pokeemerald/asm/macros/battle_script.inc'

    last_byte_id = get_last_byte_id(filename)
    last_byte_int = int(last_byte_id, 16)
    new_byte_id = f"0x{last_byte_int + 1:02X}"

    effect_name = input("Enter the name of the new effect (e.g. settypetotargettype): ")
    move_name = input("Enter the name of the move (e.g. Camouflage): ")

    new_macro = f"""
    .macro {effect_name} ptr:req
        .byte {new_byte_id}
        .4byte \\ptr
    .endm
\n
"""

    with open(filename, 'r') as file:
        data = file.readlines()

    data.insert(4, new_macro)

    with open(filename, 'w') as file:
        file.writelines(data)

    battle_script = f"""
BattleScript_Effect{move_name}::
\tattackcanceler
\tattackstring
\tppreduce
\t{effect_name} BattleScript_ButItFailed
\tattackanimation
\twaitanimation
\tprintstring STRINGID_PKMNCHANGEDTYPE
\twaitmessage B_WAIT_TIME_LONG
\tgoto BattleScript_MoveEnd
\n
"""
    byte_directive = f"\t.4byte BattleScript_Effect{move_name}             @ EFFECT_{move_name.upper()}\n"

    scripts_filename = './pokeemerald/data/battle_scripts_1.s'
    with open(scripts_filename, 'r') as file:
        data = file.readlines()

    data.insert(282, battle_script)
    data.insert(234, byte_directive)

    with open(scripts_filename, 'w') as file:
        file.writelines(data)

    effects_filename = './pokeemerald/include/constants/battle_move_effects.h'
    num_effects = get_num_effects(effects_filename)

    new_effect = f"#define EFFECT_{move_name.upper()} {num_effects}\n"
    num_effects_line = f"#define NUM_BATTLE_MOVE_EFFECTS {num_effects + 1}\n"


    with open(effects_filename, 'r') as file:
        data = file.readlines()

    data_string = "".join(data)
    pattern = r"#define NUM_BATTLE_MOVE_EFFECTS \d+"
    match = re.search(pattern, data_string)

    if not match:
        raise ValueError("Couldn't locate the NUM_BATTLE_MOVE_EFFECTS definition in the file.")

    # Get the index by counting newlines up to the match
    idx = data_string.count('\n', 0, match.start())

    # Insert the new effect line before the NUM_BATTLE_MOVE_EFFECTS line
    data.insert(idx, new_effect)

    # Update the NUM_BATTLE_MOVE_EFFECTS line with the new value
    data[idx + 1] = num_effects_line + '\n'

    with open(effects_filename, 'w') as file:
        file.writelines(data)


    print(f"Added new effect '{effect_name}' with byte ID {new_byte_id} to {filename}")
    print(f"Added battle script and .4byte directive for '{move_name}' to {scripts_filename}")
    print(f"Updated {effects_filename} with new effect and incremented NUM_BATTLE_MOVE_EFFECTS.")

if __name__ == "__main__":
    main()
