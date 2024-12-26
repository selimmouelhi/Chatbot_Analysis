import os
import pandas as pd
import json

def load_excel_data(excel_file):
    """
    Load the questions and expected answers from an Excel file.
    :param excel_file: Path to the Excel file.
    :return: List of dictionaries with 'question' and 'expected_answer'.
    """
    try:
        # Get the absolute path to the file
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        file_path = os.path.join(base_path, excel_file)

        # Print the file path for debugging
        print(f"Attempting to read file: {file_path}")

        # Read the Excel file explicitly specifying the engine
        df = pd.read_excel(file_path, engine='openpyxl')

        # Ensure the Excel file contains 'Question' and 'Expected Answer' columns
        if 'Question' not in df.columns or 'Expected Answer' not in df.columns:
            raise ValueError("The Excel file must contain 'Question' and 'Expected Answer' columns.")

        # Convert the relevant columns into a list of dictionaries
        return df[['Question', 'Expected Answer']].to_dict('records')

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Ensure it exists in the correct directory.")
        exit()
    except ValueError as ve:
        print(f"Error: {ve}")
        exit()
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        exit()

def save_to_generated_results(data, filename):
    """
    Save the extracted data to the 'generated_results' folder as JSON.
    :param data: Data to save (list of dictionaries).
    :param filename: Name of the file to save.
    """
    # Get the absolute path to the generated_results folder
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    generated_results_folder = os.path.join(base_path, "generated_results")

    # Create the folder if it doesn't exist
    os.makedirs(generated_results_folder, exist_ok=True)

    # Save the file as a JSON
    file_path = os.path.join(generated_results_folder, filename)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Data saved to {file_path}")

### uncomment to test the single script
"""
if __name__ == "__main__":
    # Provide the relative path to your test Excel file
    file_path = 'data/ExcelResponses.xlsx'

    # Test the function
    extracted_data = load_excel_data(file_path)

    # Save the extracted data
    save_to_generated_results(extracted_data, "extracted_excel.json")

    # Print the extracted data for debugging
    print("Extracted Data:")
    print(json.dumps(extracted_data, indent=4))
"""