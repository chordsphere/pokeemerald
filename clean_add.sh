#!/bin/bash

# Check if the scripts are executable or not
if [[ ! -x ./replace_emerald.sh ]] || [[ ! -x ./create_smeargle_csv.py ]] || [[ ! -x ./find_smeargle.py ]]; then
    echo "One or more scripts are not executable. Please make sure they have execute permissions."
    exit 1
fi

# Define the target directory and repo URL
TARGET_DIR="$HOME/pokemon_mods/pokeemerald"
REPO_URL="$HOME/pokemon_mods_backup"

# Check if the directory exists, if so delete it
if [ -d "$TARGET_DIR" ]; then
    echo "Deleting existing directory: $TARGET_DIR"
    rm -rf "$TARGET_DIR"
else
    echo "$TARGET_DIR does not exist, proceeding to clone."
fi

# Clone the repository
echo "Cloning the repository..."
cp -R "$REPO_URL" "$TARGET_DIR"

echo "Clone completed!"

# Run create_smeargle_csv.py
echo "Running create_smeargle_csv.py"

python3 ./create_smeargle_csv.py
if [ $? -ne 0 ]; then
    echo "Failed to run create_smeargle_csv.py"
    exit 1
fi

echo "Running find_smeargle.py"

# Run find_smeargle.py
python3 ./find_smeargle.py
if [ $? -ne 0 ]; then
    echo "Failed to run find_smeargle.py"
    exit 1
fi

echo "Running update_others.py"

# Run find_smeargle.py
python3 ./update_others.py
if [ $? -ne 0 ]; then
    echo "Failed to run update_others.py"
    exit 1
fi

echo "Running update_num_species.py"

# Run find_smeargle.py
python3 ./update_num_species.py
if [ $? -ne 0 ]; then
    echo "Failed to run update_num_species.py"
    exit 1
fi

echo "Copying graphics folder"
cp -R ./pokeemerald/graphics/pokemon/smeargle ./pokeemerald/graphics/pokemon/mimileech

#echo "Building agbcc"

#git clone https://github.com/pret/agbcc
cd agbcc
#./build.sh
./install.sh ../pokeemerald

