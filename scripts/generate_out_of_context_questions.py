from utilities.api_requests import make_api_request
from utilities.question_formatter import clean_question, create_question_json, assemble_chunks
from utilities.file_operations import save_to_json

def generate_out_of_context_questions(num_questions, context=""):
    """
    Generate out-of-context questions.
    :param num_questions: The number of questions to generate.
    :param context: Optional context to provide.
    :return: A list of question JSON objects.
    """
    question_objects = []

    for question_id in range(1, num_questions + 1):
        payload = {
            "model": "llama3.2",
            "prompt": f"Generate question {question_id} without specific context:\n\n{context}",
        }
        response = make_api_request(payload)
        if response:
            raw_question = assemble_chunks(response)
            cleaned_question = clean_question(raw_question)
            question_json = create_question_json(cleaned_question, question_id)
            question_objects.append(question_json)
            print(f"Question {question_id} generated: {raw_question}")
        else:
            print(f"Failed to generate question {question_id}.")
    
    return question_objects


def main():
    """
    Main function to drive the generation of out-of-context questions.
    """
    print("Welcome to the Out-of-Context Question Generator!")
    num_questions = int(input("How many questions do you want to generate? "))
    context = input("Provide a context (optional): ").strip()
    questions = generate_out_of_context_questions(num_questions, context)
    save_to_json(questions, "out_of_context_questions.json")
    print("\nQuestions have been successfully saved!")


if __name__ == "__main__":
    main()
