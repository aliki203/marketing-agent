"""
Agent definitions for the code pipeline.

This module contains three specialized agents:
- Code Writer: Generates Python code based on user requests
- Code Reviewer: Reviews the generated code and provides feedback
- Code Refactorer: Refactors the code based on review comments
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner

GEMINI_MODEL = "gemini-2.5-flash"


# ============================================================================
# Sub-Agents
# ============================================================================

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

code_reviewer_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='code_reviewer_agent',
    description="You review Python code.",
    instruction="""
    You are an expert Python code reviewer.
    Your task is to provide constructive feedback on the provided code.
    Code to Review:
    ```python
    {generated_code}
    ```
    Output:
    Provide your feedback as a concise, bulleted list.
    If the code is excellent and requires no changes,
    simply state: "No major issues found."
    """,
    output_key="review_comments"
)

code_refactorer_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='code_refactorer_agent',
    description="You refactor Python code based on review comments.",
    instruction="""
    You are a Python code refactorer.

    Original Code:
    ```python
    {generated_code}
    ```

    Review comments:
    {review_comments}

    Your goal is to improve the given Python code based on the provided review comments.
    Output only the complete Python code block,
    enclosed in triple backticks (```python ... ```).
    Do not add any other text before or after the code block.
    """,
    output_key="refactored_code",
)


# ============================================================================
# Sequential Agent Pipeline
# ============================================================================

root_agent = SequentialAgent(
    name='code_pipeline_agent',
    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent],
    description="Executes a sequence of agents"
)

# Create the runner
runner = InMemoryRunner(agent=root_agent, app_name='agents')
