import os
import json

def save_to_json(data, filename, base_path):
    """
    Save data to a JSON file in the specified base path. If the file already exists,
    replace its content; otherwise, create a new file.
    :param data: The data to save.
    :param filename: The name of the JSON file.
    :param base_path: The base folder where the file should be saved.
    """
    # Construct the full file path directly to the generated_questions folder
    folder = os.path.abspath(base_path)
    os.makedirs(folder, exist_ok=True)  # Ensure the folder exists
    filepath = os.path.join(folder, filename)

    # Check if the file exists
    if os.path.exists(filepath):
        print(f"File {filename} already exists. Replacing its content...")
    else:
        print(f"File {filename} does not exist. Creating a new file...")

    # Write or replace the content of the file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Data saved to {filepath}")