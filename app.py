import chainlit as cl 
import yaml 
from openai import AsyncOpenAI

with open('psw/token.yml', 'r') as f:
    token_file = yaml.safe_load(f)

TOKEN = token_file['TOKEN']

aclient = AsyncOpenAI(api_key=TOKEN)




async def call_openai_api(prompt, model = "text-davinci-003", temperature = 0.1):
    try:
        response = await aclient.chat.completions.create(model = model,
        messages=[{"role":"users", "content": prompt}],
        temperature=temperature)
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Errore durante la chiamata all'API: {str(e)}"

# Definizione del chatbot con Chainlit
@cl.on_message
async def main(message):
    # Recupera il messaggio dell'utente
    user_message = message.content

    # Chiamata all'API di OpenAI
    response = await call_openai_api(user_message)

    # Invia la risposta al frontend di Chainlit
    await cl.Message(content=response).send()