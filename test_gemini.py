import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ОШИБКА: GEMINI_API_KEY не найден")
    raise SystemExit

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Ответь одним предложением: почему детям полезно заниматься спортом?"
)

print()
print("GEMINI ОТВЕТИЛ:")
print(response.text)