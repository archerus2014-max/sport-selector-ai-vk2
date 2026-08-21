import os
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

credentials = os.getenv("GIGACHAT_CREDENTIALS")

if not credentials:
    print("ОШИБКА: GIGACHAT_CREDENTIALS не найден в .env")
    raise SystemExit(1)

print("Ключ GigaChat найден.")
print("Отправляю запрос в GigaChat...")

try:
    with GigaChat(
        credentials=credentials,
        model="GigaChat-2",
        verify_ssl_certs=False
    ) as client:

        response = client.chat.create(
            "Ты консультант по детскому спорту. "
            "Ответь по-русски простыми словами: "
            "почему ребенку полезно заниматься спортом?"
        )

        print()
        print("GIGACHAT ОТВЕТИЛ:")
        print("=" * 60)
        print(response.messages[0].content[0].text)

except Exception as e:
    print()
    print("ОШИБКА GIGACHAT:")
    print("=" * 60)
    print(type(e).__name__)
    print(e)
