import os
from openai import AsyncOpenAI
from agents import (
    Agent,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
)
from tools import get_course, get_professor, get_grades, search_planet_terp

def get_agent():
    client = AsyncOpenAI(
        # change with whatever you use. only works because this endpoint supports the openAI API  
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    set_default_openai_client(client)
    
    set_default_openai_api("chat_completions")
    
    set_tracing_disabled(True)

    agent = Agent(
        name="PlanetTerp Agent",
        model="gemini-2.5-flash", 
        instructions="You are a helpful assistant for University of Maryland students. Use the provided tools to fetch information about professors and courses. You should ALWAYS reply in Markdown.",
        tools=[get_professor, get_course, get_grades, search_planet_terp],
    )
    return agent
