# Chatbot Analysis Tool

This tool evaluates chatbot responses by comparing them with an expected dataset provided in an Excel file. It calculates semantic similarity for each response, highlights mismatches, and generates reports in both **HTML** and **Excel** formats.

---

## Project Structure

```plaintext
chatbot_analysis/
├── README.md              # Instructions on how to use the project
├── requirements.txt       # Python dependencies for the project
├── main.py                # Main script to run the analysis
├── data/                  # Input data folder
│   ├── exported_results.json   # Chatbot responses (exported JSON file)
│   ├── questions_answers.xlsx  # Excel file with expected questions and answers
├── scripts/               # Folder for scripts
│   ├── extract_excel.py        # Extract data from the Excel file
│   ├── similarity.py           # Compare responses using AI
│   ├── report_generator.py     # Generate reports in HTML and Excel formats
├── reports/               # Output reports folder
│   ├── chatbot_report.xlsx     # Generated Excel report
│   ├── chatbot_report.html     # Generated HTML report
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/chatbot-analysis.git
   cd chatbot-analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Place your **Excel file** (`questions_answers.xlsx`) and **chatbot responses file** (`exported_results.json`) in the `data/` folder.

2. Run the analysis:
   ```bash
   python3 main.py
   ```

3. Check the generated reports in the `reports/` folder:
   - **chatbot_report.xlsx**: Detailed Excel report.
   - **chatbot_report.html**: HTML report for quick viewing.

---

## Dependencies

- `pandas`: For reading and writing Excel files.
- `openpyxl`: Backend for handling Excel file formats.
- `sentence-transformers`: For semantic similarity calculations.
- `tabulate`: For creating clean tabular HTML reports.

Install these dependencies using:
```bash
pip install -r requirements.txt
```

---

## Example Report

### **Excel Report**
The Excel report contains:
- **Questions**: The question asked.
- **Expected Answers**: The correct or expected response from the Excel file.
- **Chatbot Answers**: The chatbot's actual response.
- **Similarity Scores**: Semantic similarity between expected and actual answers.
- **Match**: Yes/No indicating if the similarity is above 80%.

### **HTML Report**
The HTML report contains:
- A clean, styled table for quick comparison.
- Similarity highlights for mismatches.

