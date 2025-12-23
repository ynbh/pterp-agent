import os
from openai import AsyncOpenAI
from agents import (
    Agent,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
)
from tools import (
    get_course,
    get_professor,
    get_grades,
    search_planet_terp,
    today,
    get_grades_report,
)
from reddit import search_umd_reddit


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
        instructions="""\
        You are a helpful assistant for University of Maryland students. Use the provided tools to fetch information about professors and courses. You should ALWAYS reply in Markdown.
        For any query involving DATES, always use the `today` tool.
        For example, if a user asks something about 2025:
         - Get the current date using a call to `today` first 
         - Then appropriately decide what to do based on the query itself. 

        For GRADE distributions or overall summaries:
        1. Always use `get_grades_report`. It returns accurate totals and percentages calculated server-side.
        2. Use `get_grades` ONLY if you need specific section-by-section details that aren't in the report.
        3. Do NOT try to calculate percentages or sum large sections manually; rely on the report.

        When a professor cannot be found by the provided name (e.g., only a last name is given, or the tool returns a "not found" message):
        1. You MUST use the `search_planet_terp` tool with the name as a query. Do NOT report a failure to the user until you have attempted this search.
        2. If you find multiple results:
           - Use the course context (if any) to automatically shortlist the correct professor.
           - Example: If the user says "Kauffman for CMSC216", and search returns "Christopher Kauffman" and "Larry Kauffman", check if "Christopher Kauffman" is the one associated with CMSC216. If so, proceed with him without asking.
        3. Only ask for clarification if there is no course context to help, or if multiple professors with the same name are associated with that specific course.

        For qualitative sentiment and community advice (e.g., when asked "what do people think" or for an analysis):
        1. FIRST, provide sentiment based on PlanetTerp data (official reviews and grades).
        2. SECOND, provide "student perspective" from Reddit using `search_umd_reddit`.
           - Construct queries using KEYWORDS joined by `OR` (must be uppercase) to maximize results.
           - Good: `Kruskal OR 351 OR algorithms`
           - Bad: `what do people think of Kruskal's teaching style in 351`
        3. Focus on `selftext` for anecdotal context and `num_comments` or `upvote_ratio` to gauge consensus.
        4. Synthesize these two sources to provide a balanced overview.
        """.strip(),
        tools=[
            get_professor,
            get_course,
            get_grades,
            search_planet_terp,
            today,
            get_grades_report,
            search_umd_reddit,
        ],
    )
    return agent
