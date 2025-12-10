"""
Gradio UI for the Google ADK Code Pipeline.

This app provides a user interface with three separate output windows,
one for each agent in the pipeline:
1. Code Writer Output
2. Code Reviewer Output
3. Code Refactorer Output
"""

import gradio as gr
import asyncio
from dotenv import load_dotenv
from google.genai import types

# Import agents and runner from agents.py
from agents import runner

load_dotenv()


async def process_request_async(message: str):
    """
    Process user request through the sequential agent pipeline.
    Returns separate outputs for each agent.
    """
    # Create a session for this request
    session = await runner.session_service.create_session(user_id='user', app_name='agents')

    # Create a Content object for the message
    content = types.Content(
        role='user',
        parts=[types.Part(text=message)]
    )

    # Run the sequential agent with the user's request
    events_async = runner.run_async(
        user_id='user',
        session_id=session.id,
        new_message=content
    )

    # Process events and collect outputs
    generated_code = ""
    review_comments = ""
    refactored_code = ""

    async for event in events_async:
        # Extract state changes from each event
        if event.actions and event.actions.state_delta:
            state_delta = event.actions.state_delta
            if "generated_code" in state_delta:
                generated_code = state_delta["generated_code"]
            if "review_comments" in state_delta:
                review_comments = state_delta["review_comments"]
            if "refactored_code" in state_delta:
                refactored_code = state_delta["refactored_code"]

    return generated_code, review_comments, refactored_code


def process_request(message: str):
    """
    Synchronous wrapper for Gradio.
    Returns three separate outputs for each agent.
    """
    try:
        generated_code, review_comments, refactored_code = asyncio.run(
            process_request_async(message)
        )
        return generated_code, review_comments, refactored_code
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return error_msg, error_msg, error_msg


# ============================================================================
# Gradio UI with three separate output windows
# ============================================================================

with gr.Blocks(title="Google ADK Code Pipeline") as demo:
    gr.Markdown("""
    # Google ADK Code Pipeline

    Diese Pipeline verarbeitet deine Anfrage durch drei spezialisierte Agenten:
    1. **Code Writer** - Generiert initial Python Code
    2. **Code Reviewer** - Überprüft den Code und gibt Feedback
    3. **Code Refactorer** - Verbessert den Code basierend auf dem Feedback

    Gib eine Beschreibung ein, was du programmiert haben möchtest.
    """)

    with gr.Row():
        user_input = gr.Textbox(
            label="Deine Anfrage",
            placeholder="z.B. 'Write a function to calculate fibonacci numbers'",
            lines=3
        )

    with gr.Row():
        submit_btn = gr.Button("Pipeline starten", variant="primary")
        clear_btn = gr.Button("Löschen")

    gr.Markdown("## Output der drei Agenten")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 1️⃣ Code Writer Output")
            code_writer_output = gr.Markdown(
                label="Generated Code",
                value="*Warte auf Input...*"
            )

        with gr.Column():
            gr.Markdown("### 2️⃣ Code Reviewer Output")
            code_reviewer_output = gr.Markdown(
                label="Review Comments",
                value="*Warte auf Input...*"
            )

        with gr.Column():
            gr.Markdown("### 3️⃣ Code Refactorer Output")
            code_refactorer_output = gr.Markdown(
                label="Refactored Code",
                value="*Warte auf Input...*"
            )

    # Examples
    gr.Examples(
        examples=[
            ["Write a function to calculate fibonacci numbers"],
            ["Create a class for a simple bank account with deposit and withdraw methods"],
            ["Write a function to check if a string is a palindrome"],
            ["Create a function to sort a list using quicksort algorithm"],
        ],
        inputs=user_input
    )

    # Button actions
    submit_btn.click(
        fn=process_request,
        inputs=[user_input],
        outputs=[code_writer_output, code_reviewer_output, code_refactorer_output]
    )

    clear_btn.click(
        fn=lambda: ("", "*Warte auf Input...*", "*Warte auf Input...*", "*Warte auf Input...*"),
        inputs=None,
        outputs=[user_input, code_writer_output, code_reviewer_output, code_refactorer_output]
    )


if __name__ == "__main__":
    demo.launch()
