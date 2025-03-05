from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from typing import TypedDict, Annotated 
import yaml
import os

with open('psw/token.yml', 'r') as f:
    token_file = yaml.safe_load(f)

TOKEN = token_file['TOKEN']

os.environ["OPENAI_API_KEY"] = TOKEN


llm = ChatOpenAI(model = "gpt-4o", temperature=0.7)

# Annotaded serve per aggiungere metadati ad un tipo, questa annotazione non cambia il tipo effettivo ma fornisce informazioni extra 
class ChatState(TypedDict):
    messages: Annotated[list[AIMessage | HumanMessage | SystemMessage], "add"]

system_messages = "Sono il tuo assistente personale"

state : ChatState = {"messages" : []}
state['messages'].append(SystemMessage(content = system_messages))

    #def user_input(state: ChatState):
    #    user_messages = input("Tu: ")
    #    state['messages'].append(HumanMessage(content=user_messages))
    #    return state

def generate_response(state: ChatState):
    response = llm.invoke(state['messages'][-1].content)
    state['messages'].append(AIMessage(content=response.content))
    return state

workflow = StateGraph(ChatState)
#workflow.add_node('user input', user_input)
workflow.add_node('generate response', generate_response)

#workflow.add_edge(START,'user input')
workflow.add_edge(START,'generate response')

#workflow.add_edge('user input', 'generate response')
workflow.add_edge('generate response', END)

agent  = workflow.compile()


#agent, chat_state = build_graph()
#while True:
#    chat_state = agent.invoke(chat_state)  # Invoca il grafo passando SOLO lo stato
#    response = chat_state["messages"][-1].content  # Prende l'ultima risposta
#    print(f"🤖 ChatGPT: {response}")

def chat_with_agent(user_messages):
    #state = ChatState['messages'].append(AIMessage(content=user_messages))
    state = ChatState(messages=[HumanMessage(content=user_messages)])
    state = agent.invoke(state)
    return state['messages'][-1].content