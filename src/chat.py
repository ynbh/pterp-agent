import asyncio
import argparse
from dotenv import load_dotenv
from agents import Runner
from agent import get_agent


from rich.console import Console 
from rich.markdown import Markdown 

load_dotenv()

async def main():
    parser = argparse.ArgumentParser(description="Chat with the PlanetTerp Assistant.")
    parser.add_argument("prompt", type=str, help="The prompt to send to the agent.", nargs="?")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    args = parser.parse_args()

    agent = get_agent()

    prompt = args.prompt or "Do an analysis on Clyde Kruskal."
    
    if args.debug:
        print(f"Running agent with prompt: {prompt}")

    result = await Runner.run(agent, prompt)

    console = Console()
    MARKDOWN = result.final_output 
    md = Markdown(MARKDOWN)

    console.print(md)

    if args.debug:
        print("Tool Execution Log:")
        found_tools = False
        for item in result.new_items:
            if hasattr(item, "type") and item.type == "tool_call_item":
                found_tools = True
                if hasattr(item.raw_item, "function"):
                    fn = item.raw_item.function
                    print(f"[Tool Call] {fn.name}({fn.arguments})")
                else:
                    print(f"[Tool Call] {item.raw_item}")

        if not found_tools:
            print("No tools were called.")

if __name__ == "__main__":
    asyncio.run(main())