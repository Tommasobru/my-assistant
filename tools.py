import yaml
import os
from langchain_community.tools.tavily_search import TavilySearchResults

with open('psw/tavily.yml', 'r') as f:
    token_file = yaml.safe_load(f)

TOKEN = token_file['TOKEN']

os.environ["OPENAI_API_KEY"] = TOKEN

tavily_tool = TavilySearchResults(max_results=5)

