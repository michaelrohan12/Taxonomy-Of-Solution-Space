import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI API credentials
openai.api_key = os.getenv('API_KEY')

# Define a function to get a response from ChatGPT


def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=4082,
        temperature=0,
    )

    return response.choices[0].message.content.strip()


# Define the prompts to use for generating responses
prompts = ["Hello, how are you today?"]

# Get responses for each prompt and store them in a text file
with open("responses.txt", "w") as f:
    for prompt in prompts:
        response = get_response(prompt)
        f.write(f"Prompt: {prompt}\n")
        f.write(f"Response: {response}\n\n")
        time.sleep(1)  # Add a delay to avoid hitting the API rate limit
