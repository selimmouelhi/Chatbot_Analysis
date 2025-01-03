import os
import json
import requests
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


def main():
    """
    Main function to drive the script. Handles user input for generating questions
    in-context or out-of-context and ensures proper saving of results.
    """
    print("Welcome to the Contextual Question Generator!")
    print("Do you want to generate questions in-context or out-of-context?")
   

    
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



    print("\nProcess complete. Thank you for using the tool!")


if __name__ == "__main__":
    main()