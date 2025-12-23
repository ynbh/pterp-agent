import asyncio
import argparse
import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

from agents import Runner
from agent import get_agent

load_dotenv()

console = Console()


async def chat():
    parser = argparse.ArgumentParser(description="Interactive PlanetTerp Assistant.")
    parser.add_argument(
        "prompt", type=str, help="Initial prompt to send to the agent.", nargs="?"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    args = parser.parse_args()

    agent = get_agent()

    # we maintain the conversation history as a list of items
    conversation_history = []

    console.print(
        Panel(
            Text("Welcome to PlanetTerp Agent!", style="bold blue", justify="center"),
            border_style="red",
        )
    )
    console.print("Type 'exit' or 'quit' to end the session.\n")

    initial_prompt = args.prompt
    first_turn = True

    while True:
        try:
            if first_turn and initial_prompt:
                user_input = initial_prompt
                first_turn = False
                console.print(f"[bold green]You[/]: {user_input}")
            else:
                user_input = Prompt.ask("[bold green]You[/]")
                first_turn = False

            if user_input.lower() in ["exit", "quit"]:
                console.print("[bold red]Goodbye![/]")
                break

            if user_input.lower() == "save":
                if not conversation_history:
                    console.print("[yellow]Nothing to save yet![/]")
                    continue

                from datetime import datetime

                os.makedirs("conversations", exist_ok=True)

                filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                filepath = os.path.join("conversations", filename)

                with open(filepath, "w") as f:
                    f.write("# PlanetTerp Agent Conversation History\n\n")
                    for item in conversation_history:
                        role = item.get("role")
                        content = item.get("content")

                        if not role or role == "system" or not content:
                            continue

                        text_content = ""
                        if isinstance(content, str):
                            text_content = content
                        elif isinstance(content, list):
                            for part in content:
                                if isinstance(part, dict):
                                    text_content += part.get("text", "")
                                elif isinstance(part, str):
                                    text_content += part

                        if not text_content.strip():
                            continue

                        f.write(f"## {role.capitalize()}\n\n{text_content}\n\n---\n\n")

                console.print(f"[bold green]Conversation saved to {filepath}[/]")
                continue

            if not user_input.strip():
                continue

            # pass the whole conversation history + the new user input
            # Runner.run(agent, input) where input can be a list of items
            user_message = {"role": "user", "content": user_input}
            current_input = conversation_history + [user_message]

            with console.status("[bold blue]Agent is thinking...", spinner="dots"):
                result = await Runner.run(agent, input=current_input)

            # update history using to_input_list() which captures the full context
            conversation_history = result.to_input_list()

            console.print("\n[bold blue]PlanetTerp Agent[/]")
            console.print(Markdown(result.final_output))
            console.print("-" * console.width)

            if args.debug:
                found_tools = False
                debug_text = Text("\nTool Execution Log:", style="dim italic")
                for item in result.new_items:
                    if hasattr(item, "type") and item.type == "tool_call_item":
                        found_tools = True
                        if hasattr(item.raw_item, "function"):
                            fn = item.raw_item.function
                            debug_text.append(
                                f"\n[Tool Call] {fn.name}({fn.arguments})",
                                style="yellow",
                            )
                        else:
                            debug_text.append(
                                f"\n[Tool Call] {item.raw_item}", style="yellow"
                            )

                if found_tools:
                    console.print(debug_text)
                    console.print("-" * console.width)

        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted. Goodbye![/]")
            break
        except Exception as e:
            if args.debug:
                import traceback

                console.print(f"\n[bold red]Error:[/] {e}")
                console.print(traceback.format_exc())
            else:
                console.print(f"\n[bold red]Error:[/] {e}")


if __name__ == "__main__":
    asyncio.run(chat())
