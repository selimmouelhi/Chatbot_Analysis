import os
import json
import unicodedata
from sentence_transformers import SentenceTransformer, util

# Load the sentence transformer model
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def preprocess_text(text):
    """
    Preprocess the text for consistent comparison.
    - Normalize special characters.
    - Strip extra whitespace.
    - Convert to lowercase.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)  # Normalize special characters (e.g., æ, ø, å)
    return text.strip().lower()  # Convert to lowercase and strip spaces

def calculate_similarity(text1, text2):
    """
    Calculate the semantic similarity between two texts.
    :param text1: First text to compare.
    :param text2: Second text to compare.
    :return: Semantic similarity score as a float.
    """
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return float(similarity_score)

def load_json(file_name, folder_name="generated_results"):
    """
    Load a JSON file from the specified folder.
    :param file_name: Name of the JSON file.
    :param folder_name: Folder where the JSON file is located.
    :return: Parsed JSON data.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(base_path, folder_name, file_name)

    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def save_json(data, folder_name, file_name):
    """
    Save data to a JSON file in the specified folder.
    :param data: Data to save.
    :param folder_name: Folder where the JSON file will be saved.
    :param file_name: Name of the file to save.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Data saved to {file_path}")

def compare_postman_with_excel(postman_item, excel_data, question_threshold=0.75, answer_threshold=0.75):
    """
    Compare a single Postman question/answer with all Excel questions/answers.
    :param postman_item: Question and answer from Postman results.
    :param excel_data: List of questions and expected answers from Excel.
    :param question_threshold: Threshold for question similarity.
    :param answer_threshold: Threshold for answer similarity.
    :return: A dictionary containing the comparison result.
    """
    postman_question = preprocess_text(postman_item["question"])
    postman_answer = preprocess_text(postman_item["answer"])

    for excel_item in excel_data:
        excel_question = preprocess_text(excel_item["Question"])
        excel_answer = preprocess_text(excel_item["Expected Answer"])

        # Compare questions
        question_similarity = calculate_similarity(postman_question, excel_question)

        if question_similarity > question_threshold:
            # Compare answers only if the question is similar
            answer_similarity = calculate_similarity(postman_answer, excel_answer)

            return {
                "question_postman": postman_item["question"],
                "answer_chatbot": postman_item["answer"],
                "question_excel": excel_item["Question"],
                "expected_answer": excel_item["Expected Answer"],
                "question_similarity": f"{question_similarity * 100:.2f}%",
                "answer_similarity": f"{answer_similarity * 100:.2f}%",
                "matching": "Semantic Match" if answer_similarity > answer_threshold else "Answer Mismatch"
            }

    # If no match is found
    return {
        "question_postman": postman_item["question"],
        "answer_chatbot": postman_item["answer"],
        "question_excel": "No corresponding question",
        "expected_answer": "No corresponding answer",
        "question_similarity": "0%",
        "answer_similarity": "0%",
        "matching": "No Match"
    }

def compute_similarity():
    """
    Load data, compute semantic similarities, and save results.
    """
    try:
        # Load the datasets
        exported_results = load_json("exported_results_env.json")
        extracted_excel = load_json("extracted_excel.json")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    results = []

    # Compare each Postman question/answer with all Excel questions/answers
    for postman_item in exported_results:
        result = compare_postman_with_excel(postman_item, extracted_excel)
        results.append(result)

    # Save results
    save_json(results, "generated_similarity", "generated_similarity.json")

    # Print summary
    total_questions = len(exported_results)
    matched_questions = sum(1 for r in results if r["matching"] == "Semantic Match")
    print(f"Total questions processed: {total_questions}")
    print(f"Questions matched semantically: {matched_questions}")
    print(f"Results saved to 'generated_similarity/generated_similarity.json'")

"""
if __name__ == "__main__":
    compute_similarity()
"""

