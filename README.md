# Marketing-Agent – KI-gestützte Kampagnengenerierung für KMUs

## 1. Projektbeschreibung und Ziele

Dieses Projekt entwickelt eine Anwendung zur automatisierten Erstellung von Marketingkampagnen für kleine und mittlere Unternehmen (KMUs). Ziel ist es, durch den Einsatz von generativer KI und Google ADK (Agent Development Kit) Marketingtexte, Kampagnenideen und Social-Media-Content auf Knopfdruck zu erstellen.

Im Zentrum steht eine leicht bedienbare Gradio-Oberfläche, die es ermöglicht, mit minimalem Input wie Produkt, Zielgruppe und Marketingziel professionelle Kampagnenvarianten zu erhalten und diese direkt weiter anzupassen.

**Anwendungsbereiche:**
✅ **Social-Media-Content**: Instagram, LinkedIn, TikTok  
✅ **Kampagnenplanung**: Hooks, CTAs, Hashtags  
✅ **Strategieentwicklung**: Zielgruppenanalyse, Content Angles  
✅ **Iterative Optimierung**: KI-gestützte Verfeinerung basierend auf Feedback 

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

## 💡 Beispiel

### Beispiel 1: Instagram Launch-Kampagne

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
Fair-Trade-Kaffee für bewusste Genießer – Nachhaltigkeit trifft Geschmack

## Core Message & Hook
**Hook**: "Dein Kaffee kann die Welt verändern"
**Message**: Jede Tasse unterstützt Kleinbauern und schützt die Umwelt

## Posts

### Short (Story/Reel)
Dein Kaffee. Dein Impact. ☕🌱  
**100% bio, 100% fair, 100% Genuss.**  
Jetzt probieren → Link in Bio

### Medium (Feed-Post)
Guter Kaffee muss nicht die Welt kosten – aber er kann sie **besser machen**.  

Unser Bio-Kaffee kommt direkt von Kleinbauern in Kolumbien.  
Fair bezahlt. Umweltschonend angebaut. Unvergleichlich im Geschmack.

**Bereit für deinen Impact?** ☕  
Shoppe jetzt über den Link in der Bio.

#fairtradecoffee #biokaffee #nachhaltigleben

## CTA Variants
- **Jetzt probieren** → Link in Bio
- **Entdecke faire Bohnen** 🌱
- **Shoppe bewusst** – ab 12,99€

## Hashtags
#fairtradecoffee #biokaffee #nachhaltigleben #specialtycoffee #coffeelover

## Visual Ideas
- Flat Lay: Kaffeetasse, Bohnen, grüne Pflanze
- Behind-the-Scenes: Kaffeebauern auf Plantage
- Video: Latte-Art im Zeitraffer
```


---

## 4. Reflexion: Herausforderungen & Lerneffekte

### Herausforderungen

**1. Prompt Engineering für natürlichen Output**
- **Problem**: Erste Outputs waren sehr "AI generiert" mit übermäßigen Aufzählungen und formaler Sprache
- **Lösung**: Explizite Style-Rules in System Prompts ("Vermeide lange Aufzählungsketten"), iteratives Testen und Refinement
- **Erkenntnis**: Prompt-Design ist ebenso wichtig wie Modell-Auswahl

**2. Strukturierung des Multi-Agent-Ansatzes**
- **Problem**: Anfangs war unklar, wie Strategist und Copywriter sinnvoll zusammenarbeiten sollen und welche Aufgaben klar getrennt werden müssen
- **Lösung**: Rollen klar definiert (Strategie vs. Text), Pipeline visualisiert und beide Agenten zunächst getrennt getestet
- **Erkenntnis**: Eine saubere Aufgabenverteilung verbessert Qualität, Verständlichkeit und Erweiterbarkeit deutlich

**3. Integration in die Gradio-UI**
- **Problem**: Die Verbindung zwischen Agenten-Logik und Benutzeroberfläche war anfangs unübersichtlich, insbesondere bei der Übergabe von Eingaben und der Darstellung des Outputs
- **Lösung**: Pipeline zunächst ohne UI getestet, danach schrittweise in Gradio integriert und Output-Komponente angepasst
- **Erkenntnis**: Technische Logik allein reicht nicht – User Experience und klare Darstellung sind entscheidend

**4. Plattform-spezifische Optimierung**
- **Problem**: Gleicher Content für Instagram und LinkedIn funktioniert nicht
- **Lösung**: Platform-Awareness in Copywriter-Prompt, explizite Regeln für jede Plattform
- **Erkenntnis**: LLMs können Kontext-Switch, brauchen aber klare Instruktionen

**5. Markdown-Darstellung im Output**
- **Problem**: Wir wollten den Kampagnen-Output strukturiert mit Markdown (Überschriften, Fettdruck) darstellen. In Gradio wurde Markdown jedoch in der Textbox nicht gerendert, sondern nur als reiner Text angezeigt (z.B. `**fett**` statt fett formatiert).
- **Lösung**: Wir haben verschiedene Anzeige-Varianten getestet (z.B. Markdown-Komponente statt Textbox). Letztlich haben wir uns bewusst für die Textbox entschieden, da sie stabiler wirkte und die Struktur trotz sichtbarer Markdown-Syntax nachvollziehbar blieb.
- **Erkenntnis**: Technische Perfektion ist nicht immer entscheidend – wichtiger ist eine stabile, funktionierende und nachvollziehbare Lösung.


### Lerneffekte

**Multi-Agent vs. Single-Agent**
- Zu Beginn wurde versucht, alle Aufgaben von einem Agenten erledigen zu lassen
- Die Aufteilung in Strategist und Copywriter führte zu deutlich strukturierteren Ergebnissen
- Der Sequential-Ansatz sorgte für klarere Logik (erst Strategie, dann konkrete Texte)
- Die Trennung erleichterte Tests und Anpassungen einzelner Komponenten

**User Experience Design**
- Zu viele Freiheitsgrade überfordern Nutzer → Auswahlfelder sind hilfreicher als Freitext
- Klare Struktur im Output (Short / Medium / Long / CTA) verbessert Lesbarkeit
- Die Refinement-Funktion erhöht den praktischen Nutzen deutlich, da Texte gezielt angepasst werden können

**Praktische Anwendbarkeit**
- Tests mit realistischen Beispielen (z. B. lokale Betriebe) zeigten:
  - Der Output muss sofort einsetzbar sein
  - Hashtags sind für Social Media essenziell
  - Visual Ideas helfen besonders KMUs bei der direkten Umsetzung
- Ein klar strukturierter Output steigert die Praxistauglichkeit erheblich

**Technische Erkenntnisse**
- Gut formulierte Prompts beeinflussen die Output-Qualität stärker als erwartet
- Klare Formatvorgaben stabilisieren die Ergebnisse
- Iteratives Testen und schrittweises Anpassen sind wichtiger als einmalige „perfekte“ Prompts
- Eine saubere Trennung von Logik (Agenten) und Oberfläche (UI) vereinfacht Weiterentwicklungen

**Teamarbeit und Projektorganisation**
- Klare Verantwortlichkeiten reduzieren Überschneidungen
- Regelmäßiger Austausch verbessert Verständnis und Codequalität
- Gemeinsames Debugging fördert das technische Gesamtverständnis

**Was wir beim nächsten Mal anders machen würden**
- Früher echtes User-Testing einplanen
- Prompt-Varianten systematisch vergleichen und dokumentieren
- Projektstruktur und Git-Workflow von Beginn an klarer definieren



---

**Team**: Aliki Greune, Julie Vorwalder, Kevin Kuhn
**Repository**: (https://github.com/aliki203/marketing-agent)  
*Prüfungsleistung: Generative KI und Agenten-Entwicklung (Februar 2026)*



