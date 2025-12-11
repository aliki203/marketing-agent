"""Async debug script to see what's in the events"""

import asyncio
from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash"

async def main():
    # Create a simple test agent
    code_writer_agent = LlmAgent(
        model=GEMINI_MODEL,
        name='code_writer_agent',
        description="You write Python code.",
        instruction="""
        You are a Python code generator.
        Based on users requests, write code the fulfills the requirement.
        Output only the complete Python code block,
        enclosed in triple backticks (```python ... ```
        Do not add any other text before or after the code block
        """,
        output_key="generated_code"
    )

    root_agent = SequentialAgent(
        name='test_pipeline',
        sub_agents=[code_writer_agent],
        description="Test pipeline"
    )

    runner = InMemoryRunner(agent=root_agent, app_name='agents')

    # Create a session
    print("Creating session...")
    session = await runner.session_service.create_session(user_id='user', app_name='agents')
    print(f"Session created: {session.id}\n")

    # Create a Content object for the message
    content = types.Content(
        role='user',
        parts=[types.Part(text='Write a simple hello world function')]
    )

    print("Running agent...")
    events_async = runner.run_async(
        user_id='user',
        session_id=session.id,
        new_message=content
    )

    print("\n=== Processing Events ===\n")
    event_count = 0
    async for event in events_async:
        print(f"Event {event_count}:")
        print(f"  Type: {type(event).__name__}")
        print(f"  is_final_response: {event.is_final_response()}")

        if hasattr(event, 'actions') and event.actions:
            print(f"  Has actions: True")
            if hasattr(event.actions, 'state_delta') and event.actions.state_delta:
                print(f"  State delta keys: {list(event.actions.state_delta.keys())}")
                for key, value in event.actions.state_delta.items():
                    if isinstance(value, str):
                        print(f"    {key}: {value[:100]}...")
                    else:
                        print(f"    {key}: {value}")

        if hasattr(event, 'content') and event.content:
            print(f"  Has content: True")
            if hasattr(event.content, 'parts') and event.content.parts:
                print(f"  Number of parts: {len(event.content.parts)}")
                for j, part in enumerate(event.content.parts):
                    if hasattr(part, 'text') and part.text:
                        print(f"  Part {j} text: {part.text[:200]}...")

        print()
        event_count += 1

    print(f"Done! Processed {event_count} events")

if __name__ == "__main__":
    asyncio.run(main())
