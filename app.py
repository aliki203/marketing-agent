"""
Gradio UI for the Business Intelligence Agent Pipeline.

This app demonstrates Google ADK's SequentialAgent pattern:
1. Text-to-SQL Agent (standalone)
2. SQL execution via BIService
3. Insight Pipeline (SequentialAgent: Visualization → Explanation)
"""

import gradio as gr
import asyncio
from dotenv import load_dotenv
from google.genai import types

# Import marketing agent runners
from bi_agent import root_runner, editor_runner

# Load environment variables from bi_agent/.env
load_dotenv(dotenv_path='bi_agent/.env')


async def run_campaign_async(user_text: str):
    """
    Run the marketing campaign builder pipeline using root_runner.

    Pipeline:
    1) Strategist Agent -> strategy_text
    2) Copywriter Agent -> campaign_text
    """
    # Create session
    session = await root_runner.session_service.create_session(
        user_id="user",
        app_name="marketing_agent"
    )

    # Create user message
    content = types.Content(
        role="user",
        parts=[types.Part(text=user_text)]
    )

    # Run the pipeline
    events_async = root_runner.run_async(
        user_id="user",
        session_id=session.id,
        new_message=content
    )

    # Extract results from state
    results = {}
    async for event in events_async:
        if event.actions and event.actions.state_delta:
            for key, value in event.actions.state_delta.items():
                results[key] = value

    return results



def build_campaign_prompt(product, audience, goal, platform, tone, extra):
    return f"""Produkt/Dienstleistung: {product}
Zielgruppe: {audience}
Marketingziel: {goal}
Plattform: {platform}
Tonalität/Brand Voice: {tone}
Zusatzinfos: {extra or ""}""".strip()


async def process_request_async(product, audience, goal, platform, tone, extra):
    try:
        # Validate inputs
        if not product.strip() or not audience.strip() or not goal.strip():
            return "Bitte Produkt, Zielgruppe und Marketingziel ausfüllen."

        user_text = build_campaign_prompt(product, audience, goal, platform, tone, extra)

        # Run marketing pipeline
        results = await run_campaign_async(user_text)

        # Final output from copywriter agent
        return results.get("campaign_text", "Kein Ergebnis erhalten.")

    except Exception as e:
        return f"Error: {str(e)}"


def process_request(product, audience, goal, platform, tone, extra):
    try:
        return asyncio.run(process_request_async(product, audience, goal, platform, tone, extra))
    except Exception as e:
        return f"Error: {str(e)}"

async def refine_async(current_output: str, refine_text: str):
    if not (current_output or "").strip():
        return "Kein Output vorhanden. Bitte erst eine Kampagne generieren."
    if not (refine_text or "").strip():
        return "Bitte eine Verfeinerung eingeben (z.B. 'kürzer', 'mehr B2B', 'weniger Aufzählungen')."

    session = await editor_runner.session_service.create_session(
        user_id="user",
        app_name="marketing_editor"
    )

    content = types.Content(
        role="user",
        parts=[types.Part(
            text=f"CURRENT OUTPUT:\n{current_output}\n\nREFINE INSTRUCTION:\n{refine_text}"
        )]
    )

    events_async = editor_runner.run_async(
        user_id="user",
        session_id=session.id,
        new_message=content
    )

    results = {}
    async for event in events_async:
        if event.actions and event.actions.state_delta:
            for key, value in event.actions.state_delta.items():
                results[key] = value

    return results.get("refined_text", "Kein Refinement erhalten.")


def refine(current_output: str, refine_text: str):
    try:
        return asyncio.run(refine_async(current_output, refine_text))
    except Exception as e:
        return f"Error: {str(e)}"



# ============================================================================
# Gradio UI
# ============================================================================

with gr.Blocks(title="Social Media Ad Builder") as demo:
    gr.Markdown("""
    # Social Media Ad Builder 

    Erstelle Social-Media-Kampagnen für KMUs.  
    Pipeline: **Strategist → Copywriter**, mit optionalem **Editor-Agent** zur Verfeinerung.  
    """)

    with gr.Row():
        product = gr.Textbox(label="Produkt / Dienstleistung", placeholder="z.B. Premium Notizbuch A5", lines=1)
        platform = gr.Dropdown(["Instagram", "LinkedIn", "TikTok"], value="Instagram", label="Plattform")

    with gr.Row():
        audience = gr.Textbox(label="Zielgruppe", placeholder="z.B. Studenten, junge Berufstätige", lines=1)
        tone = gr.Dropdown(
            ["modern", "seriös", "emotional", "locker", "B2B-professionell"],
            value="modern",
            label="Tonalität / Brand Voice"
        )

    goal = gr.Textbox(label="Marketingziel", placeholder="z.B. Reichweite, Leads, Sales", lines=1)
    extra = gr.Textbox(label="Zusatzinfos (optional)", placeholder="USPs, Preis, Besonderheiten, Aktionen ...", lines=3)

    generate_btn = gr.Button("Kampagne generieren", variant="primary")
    output = gr.Textbox(label="Kampagnen-Output", lines=18)

    gr.Markdown("## Verfeinern")
    refine_text = gr.Textbox(
        label="Verfeinerung (z.B. 'kürzer', 'mehr CTA', 'weniger Aufzählungen', 'mehr B2B')",
        lines=2
    )
    refine_btn = gr.Button("Ergebnis verfeinern")

    generate_btn.click(
        fn=process_request,
        inputs=[product, audience, goal, platform, tone, extra],
        outputs=[output]
    )

    refine_btn.click(
        fn=refine,
        inputs=[output, refine_text],
        outputs=[output]
    )


if __name__ == "__main__":
    demo.launch()


