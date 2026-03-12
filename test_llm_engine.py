import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("No API Key found. Skipping test.")
else:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct:free",
            messages=[
                {"role": "system", "content": "You are a test bot."},
                {"role": "user", "content": "Say hello!"}
            ],
            temperature=0.2,
            max_tokens=100
        )
        print("Success:", response.choices[0].message.content.strip())
    except Exception as e:
        print("Error:", e)
