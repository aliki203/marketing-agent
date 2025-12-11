"""Test the ADK runner setup"""

from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner

load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash"

# Create a simple agent for testing
test_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='test_agent',
    description="A simple test agent",
    instruction="You are a helpful assistant. Answer the user's question briefly.",
    output_key="answer"
)

# Create the runner
print("Creating runner...")
runner = InMemoryRunner(agent=test_agent, app_name='agents')
print("Runner created successfully!")

# Test the runner
print("\nTesting runner.run()...")
try:
    events = runner.run(
        user_id='test_user',
        session_id='test_session',
        new_message='Hello, can you hear me?'
    )

    print("Processing events...")
    for event in events:
        print(f"Event type: {type(event).__name__}")
        if event.is_final_response():
            print(f"Final response: {event}")

    print("\nTest completed successfully!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
