import requests

def make_api_request(payload, url="http://localhost:11434/api/generate"):
    """
    Make a POST request to the API and return the response.
    :param payload: The payload to send to the API.
    :param url: The API URL.
    :return: The response text, or None if the request fails.
    """
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.text
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Request Error: {e}")
        return None
