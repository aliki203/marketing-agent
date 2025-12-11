"""Simple test to check if Gradio starts"""

import gradio as gr

def respond(message: str, history: list) -> str:
    return f"You said: {message}"

demo = gr.ChatInterface(
    fn=respond,
    title="Simple Test",
    description="Testing if Gradio works",
)

if __name__ == "__main__":
    print("Starting Gradio...")
    demo.launch()
