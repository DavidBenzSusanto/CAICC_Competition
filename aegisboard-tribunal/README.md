# ⚖️ AegisBoard — Multi-Agent Policy & Rulebook Advisory Tribunal

A production-ready [Gradio](https://gradio.app) web application that convenes a
**4-agent AI tribunal** — **LEX-01**, **CTX-02**, **ETH-03**, and **CHR-04** — to
deliberate on an organization's policy rulebook against a manually narrated case,
then hand down a **conclusive verdict**, a **primary sanction**, and a **policy
loophole rewrite**.

All inference runs on the **ModelScope** OpenAI-compatible endpoint at
`https://api-inference.modelscope.ai/v1`. No API key is ever hard-coded.

---

## 🧩 Active 4-Model Runtime Routing (default)

Every deliberation **automatically routes one approved ModelScope model per
persona** so all four models run live in the same case:

| `role_id` | Persona | Name | Accent | ModelScope Model |
| --- | --- | --- | --- | --- |
| `prosecutor` | Strict Rule-Checker | **LEX-01** | Crimson `#ef4444` | `Qwen/Qwen3.8-27B` |
| `defense` | Contextual & Intent Analyst | **CTX-02** | Teal `#14b8a6` | `stepfun-ai/Step-3.5-Flash` |
| `ethics` | Ethics & Precedent Evaluator | **ETH-03** | Amber `#f59e0b` | `zai-org/GLM-5.2` |
| `chair` | Board Chair / Chief Synthesizer | **CHR-04** | Gold `#eab308` | `deepseek-ai/DeepSeek-V4-Pro-0813` |

The four approved models:

- `deepseek-ai/DeepSeek-V4-Pro-0813`
- `zai-org/GLM-5.2`
- `Qwen/Qwen3.8-27B`
- `stepfun-ai/Step-3.5-Flash`

### Automatic fallback

Each call is wrapped in a try/except fallback handler. If a route times out,
rate-limits, or returns malformed JSON, it automatically retries on
`zai-org/GLM-5.2` or `Qwen/Qwen3.8-27B` before surfacing an error — the tribunal
never crashes on a single endpoint hiccup.

---

## ✨ Features

- **Floating-limb chibi astro-bots** — a pure SVG/CSS avatar renderer built from
  deterministic geometric primitives (`<rect rx>`, `<circle>`, `<ellipse>`,
  `<radialGradient>`, `<filter>`). No freehand `<path>` coordinates for arms or
  legs.
- **Cutscene deliberation flow (`yield`)** — `convene_board` is a Python
  generator that streams stage updates as each persona finishes: the active bot
  switches to `.state-speaking` / `.state-objecting`, shows a comic-style speech
  cloud with its live argument and `[Clause X.Y]` citation, and animated dashed
  beams link it to the role it is challenging or synthesizing.
- **Interactive stage controls** on `.council-stage`:
  - **Room Theme** — `Classic Tribunal`, `Cyber War Room`, `Zen Boardroom`
    (switches CSS variables for mahogany/amber, neon-cyan grid, or frosted
    emerald).
  - **Seating Orientation** — `Semicircle Tribunal` vs `Adversarial Arena`
    (prosecutor and defense face off on opposite sides; ethics + chair centered).
  - **Phase 2 Roadmap Preview** — a clickable accordion describing the v2.0
    Three.js/WebGL 3D courtroom upgrade path.
- **Grounded Policy Viewer** — cited clauses glow in the rulebook.
- **Interactive Consultation Bar** — the Chair poses 2 clarifying questions; your
  replies are folded into a re-deliberation.
- **Exportable Official Dossier** — one-click `.md` download of the full advisory
  report (case summary, per-bot arguments, cited clauses, consultation Q&A,
  verdict, primary sanction, and the policy loophole rewrite).
- **Permanent dark theme** — forces `document.body.classList.add('dark')` and
  overrides `.gradio-container`, `.block`, `.form`, `.accordion`, `input`,
  `textarea`, `select`, and `.wrap` with dark slate glassmorphism (no stark white
  cards).
- **Strict env-var token security** — keys read from `MODELSCOPE_API_KEY` /
  `MODELSCOPE_SDK_TOKEN` first, optional UI fallback.

---

## 🏗️ Architecture

```
aegisboard-tribunal/
├── app.py            # Single-file Gradio app (UI + routing + rendering + CSS)
├── requirements.txt  # Python dependencies
└── README.md
```

`app.py` sections:

1. **Configuration & constants** — endpoint, 4 approved models, `role_id` →
   name/title/accent/model routing, themes, orientations, stage positions.
2. **LLM helper** — `resolve_api_key` (env-first), `build_client`, JSON
   extraction, and `_call_with_fallback` (per-route try/except fallback).
3. **Personas & prompts** — per-persona system/mission and the chair synthesis
   prompt; `_run_bot`, `_run_chair`, `_deliberate_full`.
4. **Chibi renderer** — `render_chibi_bot_svg` returning the pure-SVG bot.
5. **Stage rendering** — `render_stage` (cutscene state machine, beam overlay,
   speech clouds, model badges).
6. **Callbacks** — the `convene_board` generator, `submit_followup`,
   `theme_orient_store`, `download_dossier`.
7. **UI assembly** — three-column layout, settings accordion, roadmap accordion,
   download button.

### Cutscene data flow

```
Rulebook + Case ──► convene_board() [generator]
                     ├─ LEX-01 (Qwen3.8-27B)  ── yield "speaking" frame
                     ├─ CTX-02 (Step-3.5)     ── yield "defense" frame
                     ├─ ETH-03 (GLM-5.2)      ── yield "ethics" frame
                     └─ CHR-04 (DeepSeek-V4)  ── yield "synthesis" → "verdict"
                          (each call auto-falls back on failure)
                          │
                          ▼
        JSON { bots[], chair{}, verdict{} }  ──► stage / policy viewer / dossier
```

---

## 🚀 Setup

### 1. Prerequisites

- Python 3.10+
- A ModelScope API key.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key (environment variable)

```bash
# Linux / macOS / WSL
export MODELSCOPE_API_KEY="your-key-here"

# Windows PowerShell
$env:MODELSCOPE_API_KEY = "your-key-here"
```

The key is **never** hard-coded. If no environment variable is present, the
settings bar opens automatically so you can paste a key at runtime.

---

## 🖥️ Run locally

```bash
python app.py
```

Open http://localhost:7860. The app calls `demo.queue().launch(...)` so the
generator `yield` streaming works smoothly. Override the port:

```bash
PORT=8080 python app.py
```

---

## ☁️ Run on ModelScope Studio

ModelScope Studio runs Gradio apps directly from a repository / `app.py`
entrypoint.

1. Upload this folder to ModelScope Studio.
2. Set `MODELSCOPE_API_KEY` (or `MODELSCOPE_SDK_TOKEN`) in the Studio
   Secrets / Environment panel.
3. Point Studio at `app.py` (the launch binds `0.0.0.0:$PORT`, defaults `7860`).
4. Launch — `demo.queue()` keeps the streaming cutscene responsive on the free
   CPU tier.

---

## 📄 Advisory dossier contents

The exported `.md` dossier includes:

1. **Case Summary**
2. **Council Arguments & Cited Clauses** (per bot, with the routed model)
3. **User Consultation Q&A** (Chair questions + your replies)
4. **Conclusive Verdict** (classification, confidence, severity)
5. **Primary Sanction / Action** (+ remediation & safeguards)
6. **Policy Loophole Rewrite** (exposed weakness + suggested rewrite)

---

## 🔐 Security notes

- API keys are resolved from the environment variables
  `MODELSCOPE_API_KEY` / `MODELSCOPE_SDK_TOKEN` first; the UI password box is
  only a local fallback.
- `.gitignore` excludes `.env`, `*.key`, `*.token`, caches, and temp files.
- The endpoint is pinned to `https://api-inference.modelscope.ai/v1`; only the
  four approved model IDs are ever used.