import os
from scripts.extract_results import extract_results
from scripts.extract_excel import load_excel_data, save_to_generated_results
from scripts.similarity import compute_similarity
from scripts.report_generator import generate_report

def main():
    # Step 1: Extract Postman results and save to generated_results
    print("Extracting Postman results...")
    postman_env_file = "data/Test.postman_environment.json"  # Update path if necessary
    try:
        extract_results(postman_env_file)
    except Exception as e:
        print(f"Error extracting Postman results: {e}")
        return

    # Step 2: Extract Excel data and save to generated_results
    print("Extracting Excel data...")
    excel_file = "data/ExcelResponses.xlsx"  # Update path if necessary
    try:
        extracted_excel_data = load_excel_data(excel_file)
        save_to_generated_results(extracted_excel_data, "extracted_excel.json")
    except Exception as e:
        print(f"Error extracting Excel data: {e}")
        return

    # Step 3: Compute semantic similarity report
    print("Computing similarity report...")
    try:
        compute_similarity()
    except Exception as e:
        print(f"Error computing similarity report: {e}")
        return

    # Step 4: Generate HTML and Excel reports
    print("Generating reports...")
    try:
        generate_report(threshold=80)  # Adjust threshold if necessary
    except Exception as e:
        print(f"Error generating reports: {e}")
        return

    print("All steps completed successfully!")

if __name__ == "__main__":
    main()
