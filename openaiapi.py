import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_chat_response(prompt, language, language_level):
    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"You are a helpful {language} language tutor. Answer only in colloquial {language} at CEFR(Common European Framework of Reference) level {language_level}.",
        }
    )

    user_message = {}
    user_message["role"] = "user"
    user_message["content"] = prompt
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )

    try:
        message = response["choices"][0]["message"]["content"].replace("/n", "<br>")
    except:
        message = "I'm sorry, I seem to be experiencing technical difficulties. Try again later."

    return message
