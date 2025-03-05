import chainlit as cl 
import yaml 
from ollama import chat
from ollama import ChatResponse
from openai import AsyncOpenAI
from workflow.agent import chat_with_agent
from langchain.schema import SystemMessage, AIMessage, HumanMessage


with open('psw/token.yml', 'r') as f:
    token_file = yaml.safe_load(f)

TOKEN = token_file['TOKEN']

aclient = AsyncOpenAI(api_key=TOKEN)




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
    
    response = chat_with_agent(user_messages=user_message)
    #state['messages'].append(HumanMessage(content=user_message))

    #chat_state = agent.invoke(chat_state)
    
    #recupera il modello della sessione
    #model = cl.user_session.get('model','gpt-4o')

    # Chiamata all'API di OpenAI
    #response = chat_state['messages'][-1]

    # Invia la ris posta al frontend di Chainlit
    await cl.Message(content=response).send()




