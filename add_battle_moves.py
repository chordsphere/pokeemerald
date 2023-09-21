import os

def add_new_move(template_name, new_move_name):
    # Check if the file exists
    if not os.path.exists("./pokeemerald/src/data/battle_moves.h"):
        print("File not found!")
        return
    
    # Read the file content
    with open("./pokeemerald/src/data/battle_moves.h", 'r') as file:
        content = file.readlines()
    
    # Identify the starting and ending line numbers for the template move
    start_line = None
    end_line = None
    for index, line in enumerate(content):
        if template_name in line:
            start_line = index
        if start_line is not None and '},' in line:
            end_line = index
            break
    
    # Debug Information
    print(f"Template Start Line: {start_line}")
    print(f"Template End Line: {end_line}")

    # If the template move is found
    if start_line is not None and end_line is not None:
        # Extract the template move
        template_content = content[start_line:end_line+1]
        
        # Replace the template move name with the new move name
        template_content[0] = template_content[0].replace(template_name, new_move_name)
        
        # Insert the new move to line 16
        for i, line in enumerate(template_content):
            if i==0:
                content.insert(15+i, "\n"+line)
            else:
                content.insert(15+i, line)
        
        # Write the updated content back to the file
        with open("./pokeemerald/src/data/battle_moves.h", 'w') as file:
            file.writelines(content)
        print(f"Added new move {new_move_name} successfully!")
    else:
        print(f"Template move {template_name} not found!")

def add_new_move_name(new_move_name):
    filepath = "./pokeemerald/src/data/text/move_names.h"
    
    # Check if the file exists
    if not os.path.exists(filepath):
        print(f"{filepath} not found!")
        return

    # Extract the human-readable move name (e.g., "KARATE CHOP")
    move_readable_name = new_move_name.replace("MOVE_", "").replace("_", " ").title()
    
    # Define the new move line to be inserted
    new_move_line = f'    [{new_move_name}] = _("{move_readable_name.upper()}"),\n'
    
    # Read the file content
    with open(filepath, 'r') as file:
        content = file.readlines()

    # Insert the new move to line 4
    content.insert(3, new_move_line)

    # Write the updated content back to the file
    with open(filepath, 'w') as file:
        file.writelines(content)

    print(f"Added new move {new_move_name} to {filepath} successfully!")

def add_new_move_description(new_move_name, description):
    filepath = "./pokeemerald/src/data/text/move_descriptions.h"

    # Check if the file exists
    if not os.path.exists(filepath):
        print(f"{filepath} not found!")
        return

    # Generate the variable name for the move description
    var_name = f"s{new_move_name.replace('MOVE_', '').title().replace('_', '')}Description"
    description_content = f'static const u8 {var_name}[] = _(\n    "{description}");\n'

    # Read the file content
    with open(filepath, 'r') as file:
        content = file.readlines()

    # Insert the move description to line 4
    content.insert(3, description_content)

    # Insert the move name and its associated description at line 1423
    reference_line = f'    [{new_move_name} - 1] = {var_name},\n'
    content.insert(1423, reference_line)

    # Write the updated content back to the file
    with open(filepath, 'w') as file:
        file.writelines(content)

    print(f"Added new move {new_move_name} description to {filepath} successfully!")

def update_moves_header(new_move_name):
    filepath = "./pokeemerald/include/constants/moves.h"

    # Check if the file exists
    if not os.path.exists(filepath):
        print(f"{filepath} not found!")
        return

    # Read the file content
    with open(filepath, 'r') as file:
        content = file.readlines()

    # Search for MOVES_COUNT and retrieve its current value
    move_count = None
    for line in content:
        if "MOVES_COUNT" in line:
            move_count = int(line.split()[-1])
            break

    if move_count is not None:
        # Insert the new move definition at line 5
        new_move_definition = f"#define {new_move_name} {move_count}\n"
        content.insert(4, new_move_definition)

        # Increment MOVES_COUNT value by 1
        for index, line in enumerate(content):
            if "MOVES_COUNT" in line:
                content[index] = f"#define MOVES_COUNT {move_count + 1}\n"
                break

        # Write the updated content back to the file
        with open(filepath, 'w') as file:
            file.writelines(content)

        print(f"Updated {filepath} successfully!")
    else:
        print(f"MOVES_COUNT not found in {filepath}!")

# (Rest of the script remains unchanged)

if __name__ == "__main__":
    template_name = input("Enter the name of the move you want to use as a template (example: MOVE_POUND): ")
    new_move_name = input("Enter the name for the new move (example: MOVE_KARATE_CHOP): ")
    description = input("Enter the description for the new move: ")
    
    add_new_move(template_name, new_move_name)
    add_new_move_name(new_move_name)
    add_new_move_description(new_move_name, description)
    update_moves_header(new_move_name)

