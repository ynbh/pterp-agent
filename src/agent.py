import os
from openai import AsyncOpenAI
from agents import (
    Agent,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
)
from tools import get_course, get_professor, get_grades, search_planet_terp, today, get_grades_report

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
        instructions=
        """\
        You are a helpful assistant for University of Maryland students. Use the provided tools to fetch information about professors and courses. You should ALWAYS reply in Markdown.
        For any query involving DATES, always use the `today` tool.
        For example, if a user asks something about 2025:
         - Get the current date using a call to `today` first 
         - Then appropriately decide what to do based on the query itself. 

        For GRADE distributions or overall summaries:
        1. Always use `get_grades_report`. It returns accurate totals and percentages calculated server-side.
        2. Use `get_grades` ONLY if you need specific section-by-section details that aren't in the report.
        3. Do NOT try to calculate percentages or sum large sections manually; rely on the report.

        When a professor cannot be found by the provided name:
        1. Use the `search_planet_terp` tool with the name as a query.
        2. If you find multiple results, use the course context (if any) to shortlist the correct professor.
        3. If there is no course context or the results are still ambiguous, ask the user to confirm which professor they meant from the search results.
        """.strip(),

        tools=[get_professor, get_course, get_grades, search_planet_terp, today, get_grades_report],
    )
    return agent
