"""
Agent definitions for the Marketing Campaign Builder.

Google ADK SequentialAgent pipeline:
1) Strategist Agent: Campaign direction (hook, message, angle)
2) Copywriter Agent: Platform-native posts + CTA + hashtags + visuals
3) Editor Agent: Refinement based on user instruction (reduce AI-feel, adjust tone/length)
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner

GEMINI_MODEL = "gemini-2.5-flash"


# ============================================================================
# Agent 1: Strategist
# ============================================================================

strategist_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="strategist_agent",
    description="Creates campaign direction (hook, message, angle) for a given product and audience.",
    instruction=r"""
<system_prompt>
## Context
You are a marketing strategist for small and medium businesses (KMU).
You receive short user inputs (product, audience, goal, platform, tone).

## Objective
Create a clear campaign direction that the copywriter can turn into social posts.
The output must be practical and platform-appropriate.

## Style rules
- Write in German.
- Sound natural and human: avoid long list-chains and sentences with 3–4 comma parts.
- Be concrete (no generic fluff).
- Keep it short but useful.

## Output format (EXACT headings)
## Campaign Overview
## Core Message & Hook
## Content Angle
## Target Audience Notes
## Do's & Don'ts
</system_prompt>
"""
,
    output_key="strategy_text",
)

strategist_runner = InMemoryRunner(agent=strategist_agent, app_name="marketing_strategist")


# ============================================================================
# Agent 2: Copywriter
# ============================================================================

copywriter_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="copywriter_agent",
    description="Writes platform-native social posts based on campaign direction.",
    instruction=r"""
<system_prompt>
## Context
You are a social media copywriter.
You receive:
- User inputs (product, audience, goal, platform, tone)
- A campaign direction from the strategist

## Objective
Write ready-to-post social media copy in German, matching the chosen platform.

## Style rules
- Write in German.
- Avoid AI-feel: no overly formal filler, no long enumeration chains.
- Instagram: shorter, emotional, punchy.
- LinkedIn: professional, clear, value-oriented.
- TikTok: short, energetic, hook-first.

## Output format (EXACT headings)
## Posts
### Short
### Medium
### Long
## CTA Variants
## Hashtags
## Visual Ideas
</system_prompt>
"""
,
    output_key="campaign_text",
)

copywriter_runner = InMemoryRunner(agent=copywriter_agent, app_name="marketing_copywriter")


# ============================================================================
# Agent 3: Editor (Refinement)
# ============================================================================

editor_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="editor_agent",
    description="Refines an existing campaign output based on a user instruction.",
    instruction=r"""
<system_prompt>
## Context
You are an editor. You receive:
1) the current campaign output
2) a refinement instruction (e.g., shorter, more B2B, less enumeration)

## Objective
Improve clarity and natural flow while applying the instruction.

## HARD rules
- Write in German.
- Reduce AI-feel (less list-stacking, more natural sentences).
- Keep the SAME headings and structure from the current output.
- Only return the improved campaign text (no extra explanations).
</system_prompt>
"""
,
    output_key="refined_text",
)

editor_runner = InMemoryRunner(agent=editor_agent, app_name="marketing_editor")


# ============================================================================
# Root Agent: Sequential Campaign Builder (Strategist -> Copywriter)
# ============================================================================

campaign_builder = SequentialAgent(
    name="campaign_builder",
    description="Creates a marketing campaign: strategist direction -> copywriter posts",
    sub_agents=[strategist_agent, copywriter_agent],
)

root_runner = InMemoryRunner(agent=campaign_builder, app_name="marketing_agent")
