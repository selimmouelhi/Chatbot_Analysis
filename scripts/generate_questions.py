import os
import json
import requests


def load_data_for_summary():
    """
    Load data from the extracted Excel dataset and prepare it for summarization.
    :return: A long string combining questions and answers from the dataset.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(base_path,"generated_results", "extracted_excel.json")

    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Combine questions and answers into a single text
    combined_text = []
    for item in data:
        question = item.get("Question", "").strip()
        answer = item.get("Expected Answer", "").strip()
        if question and answer:
            combined_text.append(f"{question} {answer}")

    return " ".join(combined_text)


def split_text_into_chunks(text, max_chunk_size=2000):
    """
    Split text into manageable chunks for better summarization.
    :param text: The text to split.
    :param max_chunk_size: Maximum size of each chunk (in characters).
    :return: A list of text chunks.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= max_chunk_size:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_chunk(chunk):
    """
    Summarize a single chunk of text using the Llama 3.2 model and process the response.
    :param chunk: Text chunk to summarize.
    :return: Cleaned and refined summarized text.
    """
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3.2",
        "prompt": f"Summarize the following text into a clear and concise context:\n\n{chunk}",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            # Extract and clean the response
            response_lines = response.text.strip().split("\n")
            valid_responses = []

            for line in response_lines:
                try:
                    # Parse each line as JSON
                    line_data = json.loads(line)
                    # Include only meaningful "response" text
                    if "response" in line_data and isinstance(line_data["response"], str):
                        valid_responses.append(line_data["response"].strip())
                except json.JSONDecodeError:
                    # Skip invalid JSON (e.g., metadata lines)
                    continue

            # Combine the valid response parts into a single output
            cleaned_response = " ".join(valid_responses)
            return cleaned_response

        except Exception as e:
            print("Error processing response:", e)
            return "Error: Unable to process the API response."
    else:
        print(f"API Error [{response.status_code}]: {response.text}")
        return "Error: API request failed."




def summarize_context(text):
    """
    Summarize a large block of text by processing it in chunks.
    :param text: The text to summarize.
    :return: A refined, cohesive summary.
    """
    # Split the text into manageable chunks
    chunks = split_text_into_chunks(text)

    print(f"Processing {len(chunks)} chunks for summarization...")

    refined_chunks = []
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {idx}/{len(chunks)}...")
        summary = summarize_chunk(chunk)
        refined_chunks.append(summary)

    # Combine all refined chunks into a single summary
    combined_summary = " ".join(refined_chunks)
    print("Refinement complete. Generating final summary...")

    # Optionally, refine the combined summary
    final_summary = summarize_chunk(combined_summary)
    return final_summary


def generate_context():
    """
    Load the dataset, summarize it, and return the summarized context.
    :return: A summarized context string.
    """
    print("Loading dataset for context generation...")
    long_text = load_data_for_summary()

    print("\nGenerating summarized context...")
    summarized_context = summarize_context(long_text)

    print("\nSummarized Context (Preview):")
    print(summarized_context[:500])  # Show a preview of the summarized context

    return summarized_context

def translate_text(text, target_language):
    """
    Translate text to a specified target language using a translation API.
    :param text: Text to translate.
    :param target_language: Language code for translation ('da' for Danish, 'en' for English).
    :return: Translated text.
    """
    url = "https://api.mymemory.translated.net/get"  # Example translation API
    params = {
        "q": text,
        "langpair": f"en|{target_language}" if target_language == "da" else f"da|en",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            translation_data = response.json()
            return translation_data.get("responseData", {}).get("translatedText", text)
        except Exception as e:
            print(f"Error translating text: {e}")
            return text
    else:
        print(f"Translation API Error: {response.status_code}")
        return text



def save_generated_questions(questions, filename):
    """
    Save generated questions to a JSON file.
    :param questions: List of questions to save.
    :param filename: Name of the JSON file.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    generated_questions_folder = os.path.join(base_path, "generated_questions")
    os.makedirs(generated_questions_folder, exist_ok=True)

    file_path = os.path.join(generated_questions_folder, filename)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(questions, json_file, indent=4, ensure_ascii=False)

    print(f"Questions saved to: {file_path}")

def generate_questions_from_context(context, num_questions, language="en"):
    """
    Generate questions based on a given context and language.
    :param context: The context for question generation.
    :param num_questions: Number of questions to generate.
    :param language: Target language ('en' for English, 'da' for Danish).
    :return: List of generated questions.
    """
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    prompt = f"Generate {num_questions} questions based on the following context in {language}:\n\n{context}"

    response = requests.post(url, headers=headers, json={"model": "llama3.2", "prompt": prompt})

    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data.get("response", "").split("\n")[:num_questions]
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []
    else:
        print(f"Error from API: {response.status_code}")
        return []

def beautify_summary(summary_text):
    """
    Beautify the summary text by structuring it into readable sections with proper formatting.
    :param summary_text: Raw summarized text.
    :return: Formatted and readable summary.
    """
    # Define sections and their keywords for identification
    sections = {
        "Reporting Absence": ["absence", "report", "time off"],
        "Time Off": ["time off", "leave", "absence notice"],
        "Work Schedule and Shift Coverage": ["shift", "schedule", "coverage"],
        "Leave and Benefits": ["leave", "benefit", "bonus", "accidents"],
        "Pension and Flexible Work Arrangements": ["pension", "flexible"],
        "Other Information": ["insurance", "HR", "policies"]
    }

    # Initialize a dictionary to hold sections
    formatted_sections = {key: [] for key in sections.keys()}

    # Split the summary text into sentences for processing
    sentences = summary_text.split(". ")
    for sentence in sentences:
        for section, keywords in sections.items():
            if any(keyword in sentence.lower() for keyword in keywords):
                formatted_sections[section].append(sentence.strip())
                break

    # Build the formatted summary string
    formatted_summary = []
    for section, content in formatted_sections.items():
        if content:  # Only include sections with content
            formatted_summary.append(f"### **{section}**\n")
            for line in content:
                formatted_summary.append(f"- {line.strip()}.")
            formatted_summary.append("")  # Add a blank line for spacing

    return "\n".join(formatted_summary)


def summarize_context_beautified(text):
    """
    Summarize a large block of text, beautify it, and return a formatted summary.
    :param text: The text to summarize.
    :return: A formatted, cohesive summary.
    """
    # Split the text into manageable chunks
    chunks = split_text_into_chunks(text)

    print(f"Processing {len(chunks)} chunks for summarization...")

    refined_chunks = []
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {idx}/{len(chunks)}...")
        summary = summarize_chunk(chunk)
        refined_chunks.append(summary)

    # Combine all refined chunks into a single summary
    combined_summary = " ".join(refined_chunks)
    print("Refinement complete. Generating final summary...")

    # Optionally, refine the combined summary
    final_summary = summarize_chunk(combined_summary)

    # Beautify the summary for better readability
    beautified_summary = beautify_summary(final_summary)

    return beautified_summary


def generate_and_save_context():
    """
    Generate and save the summarized context in a more beautiful format.
    """
    print("Loading dataset for context generation...")
    long_text = load_data_for_summary()

    print("\nGenerating summarized context...")
    summarized_context = summarize_context_beautified(long_text)

    print("\nSummarized Context (Preview):")
    print(summarized_context[:500])  # Show a preview of the summarized context

    # Save the beautified summary to a file
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    generated_context_folder = os.path.join(base_path, "generated_context")
    os.makedirs(generated_context_folder, exist_ok=True)

    context_file_path = os.path.join(generated_context_folder, "summarized_context.txt")
    with open(context_file_path, "w", encoding="utf-8") as file:
        file.write(summarized_context)

    print(f"\nSummarized context saved to: {context_file_path}")
    return summarized_context

def generate_and_save_questions():
    """
    Generate questions in both Danish and English, and save them to files.
    :return: None
    """
    print("Loading contexts...")
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    context_danish_file = os.path.join(base_path, "generated_context", "context_danish.txt")
    context_english_file = os.path.join(base_path, "generated_context", "context_english.txt")

    with open(context_danish_file, "r", encoding="utf-8") as file:
        context_danish = file.read()

    with open(context_english_file, "r", encoding="utf-8") as file:
        context_english = file.read()

    num_questions = int(input("\nHow many questions do you want to generate? "))

    print("\nGenerating questions in Danish...")
    questions_danish = generate_questions_from_context(context_danish, num_questions, "Danish")

    print("\nGenerating questions in English...")
    questions_english = generate_questions_from_context(context_english, num_questions, "English")

    # Save questions to files
    save_generated_questions(questions_danish, "questions_danish.json")
    save_generated_questions(questions_english, "questions_english.json")

def generate_out_of_context_questions(num_questions, context=""):
    """
    Dynamically generate the specified number of questions without a specific context.
    :param num_questions: The number of questions to generate.
    :param context: Optional context to include in the question generation.
    :return: A list of generated questions.
    """
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    # Ensure num_questions is an integer
    if isinstance(num_questions, str):
        try:
            num_questions = int(num_questions)
        except ValueError:
            raise ValueError("num_questions must be an integer or convertible to an integer.")

    questions = []  # Store generated questions

    # Loop for the specified number of questions
    for question_number in range(1, num_questions + 1):  # Start numbering at 1
        payload = {
            "model": "llama3.2",
            "prompt": f"Generate question {question_number} without specific context:\n\n{context}",
        }

        try:
            # Make the API request
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                # Extract the response JSON line by line
                response_lines = response.text.strip().split("\n")
                question_text = ""

                for line in response_lines:
                    try:
                        # Parse each line as JSON
                        line_data = json.loads(line)
                        
                        # Skip lines where "done" is true or invalid entries
                        if line_data.get("done", False):
                            continue
                        
                        # Append valid question parts
                        if "response" in line_data:
                            question_text += line_data["response"]
                    except json.JSONDecodeError:
                        continue

                # Add the cleaned-up question to the list
                if question_text.strip():  # Ensure non-empty questions are added
                    questions.append(question_text.strip())
                    print(f"Question {question_number} generated: {question_text.strip()}")
                else:
                    print(f"Question {question_number} was not generated successfully.")
            else:
                print(f"Error generating question {question_number}: {response.status_code}, {response.text}")

        except Exception as e:
            print(f"Error during question generation: {e}")

    return questions





def main():
    """
    Main function to drive the script. Handles user input for generating questions
    in-context or out-of-context and ensures proper saving of results.
    """
    print("Welcome to the Contextual Question Generator!")
    print("Do you want to generate questions in-context or out-of-context?")
    choice = input("Type '1' for in-context or '2' for out-of-context: ").strip()

    if choice == "1":
        # Generate and save context
        generate_and_save_context()
        print("\nContext successfully generated and saved.")

        # Read the generated context in Danish and English
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        context_danish_path = os.path.join(base_path, "generated_context", "context_danish.txt")
        context_english_path = os.path.join(base_path, "generated_context", "context_english.txt")

        with open(context_danish_path, "r", encoding="utf-8") as file:
            context_danish = file.read()

        with open(context_english_path, "r", encoding="utf-8") as file:
            context_english = file.read()

        # Prompt user for the number of questions
        num_questions = int(input("\nHow many questions do you want to generate? "))

        print("\nGenerating questions in Danish...")
        questions_danish = generate_questions_from_context(context_danish, num_questions, "Danish")

        print("\nGenerating questions in English...")
        questions_english = generate_questions_from_context(context_english, num_questions, "English")

        # Save the generated questions
        save_generated_questions(questions_danish, "contextual_questions_danish.json")
        save_generated_questions(questions_english, "contextual_questions_english.json")

    elif choice == "2":
        # Generate questions without context or with a provided context
        print("\nDo you want to provide a custom context? (y/n)")
        custom_context_choice = input().strip().lower()

        if custom_context_choice == "y":
            print("\nPlease enter your custom context:")
            provided_context = input("Custom context: ").strip()
        else:
            provided_context = None

        num_questions = int(input("\nHow many questions do you want to generate? "))

        print("\nGenerating out-of-context questions...")
        questions = generate_out_of_context_questions(num_questions, provided_context)

        # Save the generated questions
        save_generated_questions(questions, "out_of_context_questions.json")

    else:
        print("Invalid choice. Please try again.")

    print("\nProcess complete. Thank you for using the tool!")


if __name__ == "__main__":
    main()