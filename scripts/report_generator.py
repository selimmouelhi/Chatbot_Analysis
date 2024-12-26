import os
import json
import pandas as pd


def load_similarity_results():
    """
    Load the similarity results from the 'generated_similarity' folder.
    :return: Parsed JSON data.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(base_path, "generated_similarity", "generated_similarity.json")

    print(f"Loading results from: {file_path}")
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_to_html(data, output_path, summary):
    """
    Save the results to an HTML file with styling.
    :param data: Data to save.
    :param output_path: Path to the output HTML file.
    :param summary: Summary data for the report header.
    """
    styles = """
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1, h2, h3 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table th, table td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }
        table th {
            background-color: #f4f4f4;
        }
        .success {
            background-color: #d4edda;
        }
        .risky {
            background-color: #fff3cd;
        }
        .unsuccessful {
            background-color: #f8d7da;
        }
    </style>
    """
    summary_html = f"""
    <h1>Chatbot Analysis Report</h1>
    <h2>Summary</h2>
    <p><strong>Total Questions:</strong> {summary['total']}</p>
    <p><strong>Successful Matches (≥90%):</strong> {summary['successful']} ({summary['success_rate']}%)</p>
    <p><strong>Risky Matches (80-89%):</strong> {summary['risky']}</p>
    <p><strong>Unmatched Questions:</strong> {summary['unmatched']}</p>
    <p><strong>Average Answer Similarity:</strong> {summary['average_similarity']:.2f}%</p>
    """

    table_rows = ""
    for row in data:
        if row.get("success") == "Successful":
            row_class = "success"
        elif row.get("success") == "Risky":
            row_class = "risky"
        else:
            row_class = "unsuccessful"

        table_rows += f"""
        <tr class="{row_class}">
            <td>{row.get('question_postman', 'N/A')}</td>
            <td>{row.get('answer_chatbot', 'N/A')}</td>
            <td>{row.get('question_excel', 'N/A')}</td>
            <td>{row.get('expected_answer', 'N/A')}</td>
            <td>{row.get('question_similarity', '0%')}</td>
            <td>{row.get('answer_similarity', '0%')}</td>
            <td>{row.get('success', 'Unsuccessful')}</td>
        </tr>
        """

    table_html = f"""
    <h2>Detailed Results</h2>
    <table>
        <thead>
            <tr>
                <th>Chatbot Question</th>
                <th>Chatbot Answer</th>
                <th>Excel Question</th>
                <th>Expected Answer</th>
                <th>Question Similarity</th>
                <th>Answer Similarity</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """

    html_content = f"<!DOCTYPE html><html><head>{styles}</head><body>{summary_html}{table_html}</body></html>"

    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"HTML report generated at: {output_path}")


def save_to_excel(data, output_path):
    """
    Save the results to an Excel file.
    :param data: Data to save.
    :param output_path: Path to the output Excel file.
    """
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False, sheet_name="Results", engine="openpyxl")
    print(f"Excel report generated at: {output_path}")


def generate_report(threshold=80):
    """
    Generate a report in HTML and Excel formats.
    :param threshold: Threshold for successful semantic match.
    """
    try:
        results = load_similarity_results()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    processed_results = []
    successful_matches = 0
    risky_matches = 0
    unmatched_matches = 0
    total_similarity = 0
    total_records = len(results)

    for result in results:
        # Extract and round answer similarity
        answer_similarity_value = round(float(result.get("answer_similarity", "0").strip("%")), 2)
        question_similarity_value = round(float(result.get("question_similarity", "0").strip("%")), 2)
        success_status = "Successful" if answer_similarity_value >= 90 else "Risky" if answer_similarity_value >= threshold else "Unsuccessful"

        result["answer_similarity"] = f"{answer_similarity_value:.2f}%"
        result["question_similarity"] = f"{question_similarity_value:.2f}%"
        result["success"] = success_status

        processed_results.append(result)

        if success_status == "Successful":
            successful_matches += 1
        elif success_status == "Risky":
            risky_matches += 1
        else:
            unmatched_matches += 1

        total_similarity += answer_similarity_value

    average_similarity = round(total_similarity / total_records, 2) if total_records > 0 else 0
    success_rate = round((successful_matches / total_records) * 100, 2) if total_records > 0 else 0

    # Summary statistics
    summary = {
        "total": total_records,
        "successful": successful_matches,
        "risky": risky_matches,
        "unmatched": unmatched_matches,
        "average_similarity": average_similarity,
        "success_rate": success_rate,
    }

    # Save results to generated_reports folder
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    generated_reports_folder = os.path.join(base_path, "generated_reports")
    os.makedirs(generated_reports_folder, exist_ok=True)

    html_output_path = os.path.join(generated_reports_folder, "semantic_similarity_report.html")
    excel_output_path = os.path.join(generated_reports_folder, "semantic_similarity_report.xlsx")

    save_to_html(processed_results, html_output_path, summary)
    save_to_excel(processed_results, excel_output_path)

    print("Reports successfully generated!")


# Test function
if __name__ == "__main__":
    print("Testing the report generation...")
    generate_report(threshold=80)
