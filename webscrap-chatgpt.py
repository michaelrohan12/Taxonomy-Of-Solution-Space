import openai
import time

# Set up OpenAI API credentials
openai.api_key = "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"

# Define a function to get a response from ChatGPT
def get_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

# Define the prompts to use for generating responses
prompts = ["Hello, how are you today?", "What is your favorite color?", "Can you tell me a joke?"]

# Get responses for each prompt and store them in a text file
with open("responses.txt", "w") as f:
    for prompt in prompts:
        response = get_response(prompt)
        f.write(f"Prompt: {prompt}\n")
        f.write(f"Response: {response}\n\n")
        time.sleep(1)  # Add a delay to avoid hitting the API rate limit
