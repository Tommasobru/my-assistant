import chainlit as cl 
import yaml 
from openai import AsyncOpenAI

with open('psw/token.yml', 'r') as f:
    token_file = yaml.safe_load(f)

TOKEN = token_file['TOKEN']

aclient = AsyncOpenAI(api_key=TOKEN)


message_history = []

async def call_openai_api(prompt, model = "gpt-4o", temperature = 0.1):
    try:
        # aggiungi il nuovo messaggio dell'utente alla cronologia
        message_history.append({"role":"user", "content":prompt})

        # chiamata API
        response = await aclient.chat.completions.create(model = model,
        messages=message_history,
        temperature=temperature)
        content = response.choices[0].message.content

        # aggiungi la risposta del modello alla cronologia
        message_history.append({"role":"assistant", "content":content})

        return content
    except Exception as e:
        return f"Errore durante la chiamata all'API: {str(e)}"

@cl.on_chat_start
def on_chat_start():
    print("Nuova chat iniziata")

# Definizione del chatbot con Chainlit
@cl.on_message
async def main(message: cl.Message):
    print(cl.chat_context.to_openai())
    # Recupera il messaggio dell'utente
    user_message = message.content
    # Chiamata all'API di OpenAI
    response = await call_openai_api(user_message)

    # Invia la ris posta al frontend di Chainlit
    await cl.Message(content=response).send()




