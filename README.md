# Marketing-Agent – KI-gestützte Kampagnengenerierung für KMUs

## 1. Projektbeschreibung und Ziele

Dieses Projekt entwickelt eine Anwendung zur automatisierten Erstellung von Marketingkampagnen für kleine und mittlere Unternehmen (KMUs). Ziel ist es, durch den Einsatz von generativer KI und Google ADK (Agent Development Kit) Marketingtexte, Kampagnenideen und Social-Media-Content auf Knopfdruck zu erstellen.

Im Zentrum steht eine leicht bedienbare Gradio-Oberfläche, die es ermöglicht, mit minimalem Input wie Produkt, Zielgruppe und Marketingziel professionelle Kampagnenvarianten zu erhalten und diese direkt weiter anzupassen.

**Anwendungsbereiche:**
- Erstellung von Werbetexten
- Optimierung von Social-Media-Content
- Entwicklung von Marketingstrategien
- Personalisierung von Kundenansprachen

---

## 2. Installation und Ausführung

### Voraussetzungen

- **Python 3.12+**
- **uv** (Python Paketmanager): [Installation](https://docs.astral.sh/uv/)
- **Google Gemini API-Key**: [API-Schlüssel generieren](https://aistudio.google.com/app/apikey)

### Schritt-für-Schritt-Anleitung

1. **Repository klonen**
   ```bash
   git clone https://github.com/aliki203/marketing-agent.git
   cd marketing-agent
   ```

2. **Umgebungsvariablen konfigurieren**
   
   Erstelle die Datei `bi_agent/.env` mit folgendem Inhalt:
   ```env
   GOOGLE_API_KEY=dein_api_key_hier
   ```

3. **Abhängigkeiten installieren**
   ```bash
   uv sync
   ```

4. **Anwendung starten**
   ```bash
   uv run app.py
   ```
   
   → Gradio-Interface öffnet sich unter **http://127.0.0.1:7860**

**Alternative:** ADK Web Interface
```bash
uv run adk web . --port 8000
```
→ Öffnet sich unter **http://127.0.0.1:8000**

---

## 3. Hauptfunktionen und Verwendung des Agenten

### 3.1 Agenten-Architektur

Die Anwendung nutzt eine **Sequential Agent Pipeline** mit drei spezialisierten KI-Agenten:

1. **Strategist Agent**
   - Entwickelt Kampagnenstrategie (Hook, Message, Content Angle)
   - Analysiert Zielgruppe und Marketingziel
   - Output: Strategische Kampagnenrichtung

2. **Copywriter Agent**
   - Erstellt plattformoptimierte Social-Media-Posts
   - Generiert Hashtags, Call-to-Actions und Visual-Ideen
   - Passt Tonalität an (Instagram/LinkedIn/TikTok)
   - Output: Fertige Post-Varianten (Short/Medium/Long)

3. **Editor Agent**
   - Verfeinert Ergebnisse basierend auf User-Feedback
   - Ermöglicht iterative Optimierung
   - Output: Optimierter Kampagnen-Content

### 3.2 Verwendung der Anwendung

**Schritt 1: Eingabe machen**
- **Produkt/Dienstleistung**: z.B. "Premium Leder-Notizbuch A5"
- **Zielgruppe**: z.B. "Kreative Professionals, 25-40 Jahre"
- **Marketingziel**: z.B. "Launch-Kampagne mit Sales-Fokus"
- **Plattform**: Instagram / LinkedIn / TikTok
- **Tonalität**: Modern / Seriös / Emotional / Locker / B2B-professionell
- **Zusatzinfos** (optional): USPs, Preisinformationen, Aktionen

**Schritt 2: Kampagne generieren**
- Button "Kampagne generieren" klicken
- Pipeline läuft durch (Strategist → Copywriter)
- Ergebnis wird nach ca. 10-20 Sekunden angezeigt

**Schritt 3: Optional verfeinern**
- Verfeinerungs-Anweisung eingeben (z.B. "kürzer", "mehr Emojis", "weniger Aufzählungen")
- Button "Ergebnis verfeinern" klicken
- Editor-Agent optimiert den Output

### 3.3 Beispiel-Workflow

**Input:**
```
Produkt: Bio-Kaffee aus fairem Handel
Zielgruppe: Umweltbewusste Millennials, 25-35
Ziel: Brand Awareness
Plattform: Instagram
Tonalität: Modern
```

**Output (Auszug):**
```markdown
## Campaign Overview
Fair-Trade-Kaffee für bewusste Genießer – 
Nachhaltigkeit trifft Geschmack

## Posts

### Short
Dein Kaffee. Dein Impact. ☕🌱
100% bio, 100% fair, 100% Genuss.
Jetzt probieren → Link in Bio

#fairtradecoffee #nachhaltigleben #biokaffee

### Medium
Guter Kaffee muss nicht die Welt kosten – 
aber er kann sie besser machen.
[...]
```

---

## 4. Reflexion: Herausforderungen & Lerneffekte

### Herausforderungen

**1. Prompt Engineering für natürlichen Output**
- **Problem**: Erste Outputs waren sehr "AI-like" mit übermäßigen Aufzählungen und formaler Sprache
- **Lösung**: Explizite Style-Rules in System Prompts ("Vermeide lange Aufzählungsketten"), iteratives Testen und Refinement
- **Erkenntnis**: Prompt-Design ist ebenso wichtig wie Modell-Auswahl

**2. Multi-Agent State-Management**
- **Problem**: Verstehen, wie `state_delta` zwischen Strategist und Copywriter weitergegeben wird
- **Lösung**: ADK-Dokumentation studiert, Debug-Logs eingefügt, `output_key` korrekt definiert
- **Erkenntnis**: ADK abstrahiert viel, aber Verständnis der Event-Streams ist essentiell

**3. Async/Await in Gradio**
- **Problem**: Gradio-Buttons rufen synchrone Funktionen auf, aber ADK-Runner sind asynchron
- **Lösung**: Wrapper-Funktion mit `asyncio.run()` implementiert
- **Erkenntnis**: Bridge-Pattern zwischen sync/async Welten notwendig

**4. Plattform-spezifische Optimierung**
- **Problem**: Gleicher Content für Instagram und LinkedIn funktioniert nicht
- **Lösung**: Platform-Awareness in Copywriter-Prompt, explizite Regeln für jede Plattform
- **Erkenntnis**: LLMs können Kontext-Switch, brauchen aber klare Instruktionen

**5. Teamkoordination und Aufgabenteilung**
- **Problem**: Paralleles Arbeiten am Code führte zu Merge-Konflikten und unterschiedlichen Coding-Standards
- **Lösung**: Klare Modul-Verantwortlichkeiten definiert, regelmäßige Code-Reviews durchgeführt
- **Erkenntnis**: Kommunikation und Git-Workflow-Planung sind für Teamprojekte essenziell

### Lerneffekte

**Multi-Agent vs. Single-Agent**
- Das Team experimentierte zunächst mit einem monolithischen Agent-Ansatz
- Der Sequential-Ansatz brachte bessere Qualität (Strategist fokussiert auf Strategie, Copywriter auf Text)
- Klareres Debugging und modulare Erweiterbarkeit durch Aufgabentrennung

**User Experience Design**
- Zu viele Optionen überfordern → 5 Tonalitäten statt Freitext
- Instant Feedback wichtig → Loading-Indikator in Gradio
- Refinement-Funktion erhöht Nutzerzufriedenheit massiv

**Praktische Anwendbarkeit**
- Tests mit echten Beispielen (lokale Cafés, Handwerksbetriebe) zeigten:
  - Output muss sofort verwendbar sein (keine Nacharbeit)
  - Hashtags sind unverzichtbar für Social Media
  - Visual Ideas helfen KMUs enorm (oft keine Designer im Team)

**Technische Erkenntnisse**
- Systematisch getestete Prompts verbessern Output-Qualität maßgeblich
- Spezialisierte Agenten steigern sowohl Flexibilität als auch Ergebnisqualität
- Iterative Verfeinerung ist entscheidend für praxistaugliche KI-Lösungen

**Teamarbeit und Projektmanagement**
- Regelmäßige Sync-Meetings halfen, das Team auf gemeinsame Ziele auszurichten
- Code-Reviews verbesserten Codequalität und Wissensaustausch im Team
- Aufgabenteilung nach Stärken (UI/UX, Agent-Entwicklung, Testing) erhöhte Effizienz
- Gemeinsames Debugging komplexer Probleme führte zu tieferem Verständnis der ADK-Architektur

**Was wir beim nächsten Mal anders machen würden**
- Früher User-Testing einplanen (erst nach 80% Entwicklung getestet → viele späte Anpassungen)
- Besseres Error-Handling von Anfang an (momentan nur Basic-Validierung)
- Caching für wiederholte Anfragen implementieren (Kosten sparen)
- A/B-Testing verschiedener Prompt-Varianten systematisch dokumentieren
- Klarere Git-Branch-Strategie von Projektbeginn an

---

**Team**: Aliki Greune, Julie Vorwalder, Kevin Kuhn
**Repository**: (https://github.com/aliki203/marketing-agent)  
*Prüfungsleistung: Generative KI und Agenten-Entwicklung (Februar 2026)*



