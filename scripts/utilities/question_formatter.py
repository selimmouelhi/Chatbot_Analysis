
import json
def assemble_chunks(response_text):
    """
    Assemble chunks of responses into a coherent message.
    :param response_text: The raw response text from the API.
    :return: A single, combined string representing the full question.
    """
    assembled_text = ""
    try:
        # Split the response into lines
        response_lines = response_text.strip().split("\n")

        # Parse each line and extract the "response" field
        for line in response_lines:
            try:
                line_data = json.loads(line)  # Parse the line as JSON
                if "response" in line_data and not line_data.get("done", False):
                    assembled_text += line_data["response"]
            except json.JSONDecodeError:
                continue
    except Exception as e:
        print(f"Error assembling chunks: {e}")

    return assembled_text.strip()

def clean_question(raw_response):
    """
    Clean up the raw question response from the API.
    :param raw_response: The raw response text from the API.
    :return: A cleaned question string.
    """
    raw_question = raw_response.strip().split(":", 1)[-1].strip()  # Remove everything before the colon
    raw_question = raw_question.replace("\n\n", " ").replace("\n", " ").strip()
    if raw_question.startswith("\"") and raw_question.endswith("\""):
        raw_question = raw_question[1:-1].strip()
    return raw_question


def create_question_json(question_text, question_id):
    """
    Create a JSON object for a question.
    :param question_text: The text of the question.
    :param question_id: The ID for the question.
    :return: A dictionary representing the question in JSON format.
    """
    return {"id": question_id, "message": question_text}
