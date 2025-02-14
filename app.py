import chainlit as cl 
import yaml 
from ollama import chat
from ollama import ChatResponse

from openai import AsyncOpenAI

with open('psw/token.yml', 'r') as f:
    token_file = yaml.safe_load(f)

TOKEN = token_file['TOKEN']

aclient = AsyncOpenAI(api_key=TOKEN)




async def call_model(prompt, model, temperature = 0.1):
    try:
        if model == "gpt-4o":
            message_history = []
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
        else:
            message_history = []
            message_history.append({"role":"user", "content":prompt})
            response: ChatResponse = chat(model='deepseek-r1', messages= message_history)
            
            #content = response.message.content
            content = response["message"]["content"] 
            message_history.append({"role":"assistant", "content":content})
            return content 


    except Exception as e:
        return f"Errore durante la chiamata all'API: {str(e)}"

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="DeepSeek",
            markdown_description="The underlying LLM model is **DeepSeek**.",
        ),
        cl.ChatProfile(
            name="GPT-4",
            markdown_description="The underlying LLM model is **GPT-4**.",
        ),
    ]

@cl.on_chat_start
async def on_chat_start():
    print("la chat è iniziata")
    chat_profile = cl.user_session.get("chat_profile", "GPT-4")

    # determina il modello da usare 
    model = "deepseek-r1" if chat_profile == "DeepSeek" else "gpt-4o"

    print(model)
    cl.user_session.set("model", model)


    await cl.Message(
        content=f"starting chat using the {chat_profile} chat profile"
    ).send()

# Definizione del chatbot con Chainlit
@cl.on_message
async def main(message: cl.Message):
    print(cl.chat_context.to_openai())
    # Recupera il messaggio dell'utente
    user_message = message.content
    
    #recupera il modello della sessione
    model = cl.user_session.get('model','gpt-4o')

    # Chiamata all'API di OpenAI
    response = await call_model(user_message, model)

    # Invia la ris posta al frontend di Chainlit
    await cl.Message(content=response).send()




