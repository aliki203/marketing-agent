# Marketing Campaign Builder (Google ADK + Gradio)

## Projektziel
Dieses Projekt implementiert einen KI-Agenten mit dem Google Agent Development Kit (ADK), der KMUs bei der Erstellung von Social-Media-Kampagnen unterstützt. Aus wenigen Eingaben (Produkt, Zielgruppe, Marketingziel, Plattform, Tonalität) generiert der Agent eine Kampagnenidee und fertige Post-Varianten. Zusätzlich kann das Ergebnis über eine Verfeinerungsfunktion iterativ verbessert werden.

## Features
- Kampagnen-Generierung über eine Agenten-Pipeline (Strategist → Copywriter)
- Plattform-Auswahl: Instagram, LinkedIn, TikTok
- Anpassbare Tonalität/Brand Voice
- Verfeinerung (Refine) über Editor-Agent (z.B. „kürzer“, „mehr CTA“, „weniger Aufzählungen“)
- Gradio UI mit Eingabe, Ausgabe und Basis-Validierung

## Installation
### Voraussetzungen:
- Python 3.11+ (empfohlen)
- API Key / Credentials in `bi_agent/.env` (siehe unten)

### Setup (Beispiel mit venv)
```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt 
```
##




