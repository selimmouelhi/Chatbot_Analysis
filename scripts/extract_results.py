import os
import json

def extract_results(environment_file, output_file='exported_results_env.json'):
    """
    Extract the `exportResults` variable from the exported Postman environment file.
    :param environment_file: Path to the Postman environment file.
    :param output_file: Name of the file to save the extracted results.
    """
    try:
        # Get the absolute path to the environment file
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        env_file_path = os.path.join(base_path, environment_file)

        # Load the Postman environment file
        with open(env_file_path, 'r', encoding='utf-8') as file:
            environment = json.load(file)
    except FileNotFoundError:
        print(f"Error: '{env_file_path}' file not found.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: Failed to parse '{env_file_path}'. Ensure it's a valid JSON file.")
        exit()

    # Extract the `exportResults` variable
    export_results = None
    if "values" in environment:
        for item in environment["values"]:
            if item["key"] == "exportResults":
                try:
                    # Parse the JSON value of the `exportResults` variable
                    export_results = json.loads(item["value"])
                except json.JSONDecodeError:
                    print("Error: Failed to parse 'exportResults' value as JSON.")
                    print(f"Raw value: {item['value']}")
                    exit()
                break

    if export_results:
        # Save the extracted results to the `generated_results` folder
        try:
            # Get the absolute path to the generated_results folder
            generated_results_folder = os.path.join(base_path, "generated_results")
            os.makedirs(generated_results_folder, exist_ok=True)  # Create the folder if it doesn't exist

            # Save the file
            output_file_path = os.path.join(generated_results_folder, output_file)
            with open(output_file_path, 'w', encoding='utf-8') as output:
                json.dump(export_results, output, ensure_ascii=False, indent=4)
            print(f"Extracted results saved to '{output_file_path}'.")
        except IOError:
            print(f"Error: Failed to write to '{output_file_path}'.")
    else:
        print("No 'exportResults' variable found in the environment file.")
"""
if __name__ == "__main__":
    # Example test case
    environment_file = 'data/Test.postman_environment.json'  # Path to the exported Postman environment file
    extract_results(environment_file)
"""