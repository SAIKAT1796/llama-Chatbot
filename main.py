import requests
import json

def generate_response(prompt):
    """
    Sends a POST request to the specified URL with the provided prompt,
    processes the response to combine fragments into a single coherent paragraph.

    Parameters:
    - prompt (str): The question or prompt to be sent in the POST request.

    Returns:
    - combined_response (str): The combined response from the fragments.
    """
    # URL to which the request is to be sent
    url = "http://localhost:11434/api/generate"

    # Data to be sent in the POST request
    data = {"model": "llama3", "prompt": prompt}

    # Making the POST request
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    # The responses provided as a string
    responses_string = response.text

    # Splitting the string into individual JSON strings
    json_responses = responses_string.split('\n')

    # Parsing the JSON strings into a list of dictionaries
    responses = []
    for response_str in json_responses:
        if response_str.strip():  # Skip empty lines
            try:
                responses.append(json.loads(response_str))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue

    # Function to combine response fragments into a single string
    def combine_responses(responses):
        return ''.join(item['response'] for item in responses)

    # Combine the responses
    combined_response = combine_responses(responses)
    return combined_response

def main():
    while True:
        user_prompt = input("Enter your question (or type 'exit' to quit): ")
        if user_prompt.lower() == 'exit':
            break
        try:
            combined_response = generate_response(user_prompt)
            print("Combined Response:", combined_response)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()
