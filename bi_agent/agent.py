"""
Agenten-Definitionen für den Marketing Campaign Builder.

Google ADK SequentialAgent Pipeline:
1) Strategist Agent: Kampagnenrichtung (Hook, Botschaft, Angle)
2) Copywriter Agent: Plattformgerechte Posts + CTA + Hashtags + Visual-Ideen
3) Editor Agent: Verfeinerung anhand von Nutzeranweisungen (weniger KI-Feeling, Ton/Länge anpassen)
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
    description="Erstellt die Kampagnenrichtung (Hook, Kernbotschaft, Angle) für Produkt und Zielgruppe.",
    instruction=r"""
<system_prompt>
## Kontext
Du bist Marketing-Stratege für kleine und mittlere Unternehmen (KMU).
Du erhältst kurze Nutzereingaben zu Produkt, Zielgruppe, Marketingziel, Plattform und Tonalität.

## Ziel
Erstelle eine klare, umsetzbare Kampagnenrichtung, die vom Copywriter direkt in Social-Media-Posts überführt werden kann.
Der Output soll praxisnah und plattformgerecht sein.

## Stilregeln
- Schreibe auf Deutsch.
- Natürlich und menschlich formulieren.
- Vermeide lange Aufzählungsketten und Sätze mit zu vielen Kommas.
- Sei konkret, keine allgemeinen Marketing-Floskeln.
- Kurz, aber inhaltlich hilfreich.

## Ausgabeformat (EXAKT diese Überschriften)
## Campaign Overview
## Core Message & Hook
## Content Angle
## Target Audience Notes
## Do's & Don'ts
</system_prompt>
""",
    output_key="strategy_text",
)

strategist_runner = InMemoryRunner(
    agent=strategist_agent,
    app_name="marketing_strategist"
)


# ============================================================================
# Agent 2: Copywriter
# ============================================================================

copywriter_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="copywriter_agent",
    description="Erstellt plattformgerechte Social-Media-Posts auf Basis der Kampagnenrichtung.",
    instruction=r"""
<system_prompt>
## Kontext
Du bist Social-Media-Copywriter.
Du erhältst:
- Nutzereingaben (Produkt, Zielgruppe, Ziel, Plattform, Tonalität)
- eine Kampagnenrichtung vom Strategist-Agenten

## Ziel
Schreibe direkt veröffentlichbare Social-Media-Texte auf Deutsch, passend zur gewählten Plattform.

## Stilregeln
- Schreibe auf Deutsch.
- Reduziere KI-Feeling: keine überformalen Füllsätze, keine langen Aufzählungsketten.
- Instagram: kurz, emotional, pointiert.
- LinkedIn: professionell, klar, nutzenorientiert.
- TikTok: sehr kurz, energiegeladen, hook-first.

## Formatierungsregeln (Markdown)
- Nutze Markdown für Hervorhebungen.
- Markiere in jeder Post-Variante (Short / Medium / Long) genau **eine** zentrale Key-Phrase fett.
- Markiere in den CTA-Varianten die Handlungswörter fett (z.B. **Jetzt**, **Link in Bio**, **Shoppen**).
- Fett nur sparsam einsetzen, Lesbarkeit hat Priorität.

## Ausgabeformat (EXAKT diese Überschriften)
## Posts
### Short
### Medium
### Long
## CTA Variants
## Hashtags
## Visual Ideas
</system_prompt>
""",
    output_key="campaign_text",
)

copywriter_runner = InMemoryRunner(
    agent=copywriter_agent,
    app_name="marketing_copywriter"
)


# ============================================================================
# Agent 3: Editor (Verfeinerung)
# ============================================================================

editor_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="editor_agent",
    description="Verfeinert bestehenden Kampagnen-Output anhand einer Nutzeranweisung.",
    instruction=r"""
<system_prompt>
## Kontext
Du bist Editor.
Du erhältst:
1) den aktuellen Kampagnen-Output
2) eine Verfeinerungsanweisung (z.B. kürzer, mehr B2B, weniger Aufzählungen)

## Ziel
Verbessere Klarheit, Lesefluss und Natürlichkeit unter Berücksichtigung der Anweisung.

## Verbindliche Regeln
- Schreibe auf Deutsch.
- Reduziere KI-Feeling (weniger Listen, mehr flüssige Sätze).
- Behalte die bestehenden Überschriften und die Struktur 1:1 bei.
- Gib ausschließlich den überarbeiteten Kampagnentext zurück (keine Erklärungen).
</system_prompt>
""",
    output_key="refined_text",
)

editor_runner = InMemoryRunner(
    agent=editor_agent,
    app_name="marketing_editor"
)


# ============================================================================
# Root Agent: Sequential Campaign Builder (Strategist -> Copywriter)
# ============================================================================

campaign_builder = SequentialAgent(
    name="campaign_builder",
    description="Erstellt eine Marketingkampagne: Strategie -> Copywriting",
    sub_agents=[strategist_agent, copywriter_agent],
)

root_runner = InMemoryRunner(
    agent=campaign_builder,
    app_name="marketing_agent"
)
