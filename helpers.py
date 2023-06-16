import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

language = "Mexican Spanish"
language_level = "B1"


# Storing a message with content as an array of message objects
chat_content = {
    "role": "system",
    "content": f"You are a {language} language tutor. Answer only in colloquial {language} at CEFR(Common European Framework of Reference) level {language_level}. Ask the user what they would like to talk about today?",
}


completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[chat_content],
    max_tokens=200,
    frequency_penalty=0.5,
    presence_penalty=0.5,
)

assistant_response = completion["choices"][0]["message"]["content"]

# The assistant’s reply can be extracted with response['choices'][0]['message']['content']

# print(
#     assistant_response
# )  # ¡Hola! ¿Qué onda? ¿De qué quieres hablar hoy en nuestra clase de español mexicano?

# ¡Hola! ¿Cómo estás? ¿Qué tema te gustaría hablar hoy en tu clase de español? Estoy aquí para ayudarte a mejorar tus habilidades lingüísticas y hacer que te sientas más cómodo hablando en español. ¡Cuéntame qué quieres aprender hoy!

# EXAMPLE RESPONSE
{
    "id": "chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve",
    "object": "chat.completion",
    "created": 1677649420,
    "model": "gpt-3.5-turbo",
    "usage": {"prompt_tokens": 56, "completion_tokens": 31, "total_tokens": 87},
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "The 2020 World Series was played in Arlington, Texas at the Globe Life Field, which was the new home stadium for the Texas Rangers.",
            },
            "finish_reason": "stop",
            "index": 0,
        }
    ],
}
