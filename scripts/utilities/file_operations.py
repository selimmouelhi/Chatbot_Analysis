import os
import json

def save_to_json(data, filename):
    """
    Save data to a JSON file in the 'generated_questions' folder, which is at the same level as the 'scripts' folder.
    :param data: The data to save.
    :param filename: The name of the JSON file.
    """
    # Navigate to the folder at the same level as 'scripts'
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_questions"))
    os.makedirs(base_path, exist_ok=True)  # Create 'generated_questions' folder if it doesn't exist

    # Construct the full file path
    filepath = os.path.join(base_path, filename)

    # Write data to the JSON file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Data saved to {filepath}")