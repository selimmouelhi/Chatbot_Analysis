
# Chatbot Analysis Automation

## Workflow Overview

This project is designed to automate the testing and evaluation of chatbot responses against a predefined set of questions and expected answers stored in an Excel file. The workflow includes:

### Prerequisites
1. **Postman Environment**: Ensure you have a valid Postman environment that automates the sending of chatbot questions through the backend API. The responses should be captured in a structured JSON format within an environment variable.
2. **Environment Structure**: The Postman environment should store a `questions` array in the following JSON structure:
    ```json
    [
        {
            "question": "Your question here?",
            "answer": "Chatbot's response here."
        },
        ...
    ]
    ```
3. **Extracting the Environment**: After running the automation in Postman, export the environment and save it in the `data` folder of this project. The file should be named `exported_results_env.json`.

### Project Structure and Workflow
1. **Input Data**:
   - **Excel File**: Contains the predefined questions and expected answers. Save it as `extracted_excel.json` under the `data` folder. The file must include columns for `Question` and `Expected Answer`.
   - **Postman Export**: Contains the chatbot's questions and responses, extracted from the Postman environment as described above.

2. **Execution Flow**:
   - **Run Scripts**: Use `main.py` to execute all scripts in the correct order:
     - Extract questions and expected answers from the Excel file.
     - Process the exported Postman environment JSON file.
     - Compute semantic similarity between the questions and answers.
     - Generate a detailed report in both HTML and Excel formats.

3. **Reports**:
   - Reports are generated in the `generated_reports` folder.
   - A summary of chatbot accuracy and any mismatches is provided.

---

## Project Structure

```
Chatbot_Analysis/
│
├── data/
│   ├── exported_results_env.json  # Exported Postman environment JSON
│   ├── extracted_excel.json       # Questions and expected answers in JSON format
│
├── generated_similarity/
│   └── generated_similarity.json  # Semantic similarity results
│
├── generated_reports/
│   ├── semantic_similarity_report.html  # Styled HTML report
│   ├── semantic_similarity_report.xlsx  # Excel report
│
├── scripts/
│   ├── extract_excel.py           # Extracts questions and answers from Excel
│   ├── extract_results.py         # Processes the exported Postman environment
│   ├── similarity.py              # Computes semantic similarity
│   ├── report_generator.py        # Generates HTML and Excel reports
│
├── main.py                        # Main script to run the project
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Chatbot_Analysis
   ```

2. **Set Up the Python Environment**:
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Prepare Input Data**:
   - Place the `exported_results_env.json` and `extracted_excel.json` files in the `data/` folder.

4. **Run the Project**:
   - Execute the main script:
     ```bash
     python main.py
     ```

---

## Features

1. **Automated Chatbot Analysis**:
   - Extracts data from Postman and Excel.
   - Compares semantic similarity between questions and answers.

2. **Detailed Reports**:
   - Provides an overall chatbot accuracy score.
   - Highlights low-performing answers (<90% similarity) as "risky."
   - Sections for both successful and unsuccessful matches.

3. **Customizable Thresholds**:
   - Default similarity threshold: `80%`.
   - Adjust in `report_generator.py` as needed.

4. **Styling**:
   - HTML reports are styled for easy readability.
   - Risky sections are highlighted in red.

---