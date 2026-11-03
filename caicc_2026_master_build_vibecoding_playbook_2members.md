# CAICC 2026 Track 2 — Master Build & Vibecoding Playbook
**Project Title:** AegisBoard — Gamified Multi-Agent Policy & Rulebook Advisory Tribunal  
**Competition:** Campus AI Co-Creation Competition (CAICC 2026) — Track 2: Prompt to App  
**Submission Window:** Wednesday, 4 November 2026, 16:00 – 23:59 WIB (via WhatsApp Group Google Form)

---

> ### Document Partition Map
> * **PART I — Initial Rules, General Shape & 2-Member Team Plan (Sections 1–3):** Competition guardrails, finalized application architecture/UI blueprint, multi-model runtime routing, Floating-Limb Chibi Astro-Bot specification, and the 2-member workload split & schedule (1,000 Combined Magic Cubes/Day).
> * **PART II — Step-by-Step Execution Guide from First to Last Step (Sections 4–9):** Chronological walkthrough from initial account/environment setup, project initialization, and the 3 Master Vibecoding Prompts to local testing, ModelScope Studio CPU deployment (STEP E), and final submission (STEP F).

---
---

# PART I: INITIAL RULES, GENERAL SHAPE & 2-MEMBER TEAM PLAN

---

## 1. Golden Rules & Disqualification Guardrails (READ FIRST)
Every team member must strictly follow these rules from the CAICC 2026 Participant Guide:

1. **4 Approved Models ONLY:** Both your coding assistant (Claude Code / OpenCode) AND your application's internal AI calls may **ONLY** use these exact four ModelScope models:
   * `zai-org/GLM-5.2` (GLM-5.2)
   * `deepseek-ai/DeepSeek-V4-Pro-0813` (DeepSeek-V4-Pro-0813)
   * `stepfun-ai/Step-3.5-Flash` (Step-3.5-Flash)
   * `Qwen/Qwen3.8-27B` (Qwen3.8-27B)
   * *Using any other model in coding or inside the app leads to immediate disqualification.*
2. **Zero Exposed API Keys / Tokens:** **NEVER** hardcode your `your_modelscope_token` inside `app.py` or commit it to Git. Read it via `os.getenv("MODELSCOPE_API_KEY")` and store the actual token inside **ModelScope Studio Secrets** during deployment.
3. **Free CPU Only:** Deploy on **ModelScope Studio** using **Gradio** on **Free CPU (allocated on demand)**. Do NOT select GPU or xGPU.
4. **Vibecoding Constraint (<30 Human Lines):** Do not write application code manually. Let OpenCode / Claude Code generate and edit all `.py`, `.txt`, and `.md` files using the surgical prompts in **Section 6** below.
5. **Mandatory Evidence Collection (50% of Score!):** "ModelScope AI Usage" is worth **50% of the total judging score**. Every time you run a prompt in OpenCode or Claude Code, **take a full-screen screenshot** clearly showing:
   * The **approved model name** (e.g., `DeepSeek V4 Pro` or `GLM-5.2`) in the top-right corner/status bar.
   * Your prompt and the AI's multi-round code generation/refinement.
6. **Magic Cubes Quota Management (1,000 Combined Magic Cubes/Day):** Every account receives **500 Magic Cubes per day** (350 daily login + 150 competition bonus) which expire at midnight each day. With 2 team members, your team commands **1,000 combined Magic Cubes per day**. Because we have pre-engineered the exact prompts in this file, you will only need **3–4 prompting rounds total** to build the entire app.

---

## 2. Finalized Application Blueprint (UI/UX, Multi-Model Routing & Visual Lock-In)

### 2.1 Core Purpose & Decisive Output
**AegisBoard** is an interactive **Compliance & Ethics Advisory Board** where organizations upload their official policy/rulebook and consult a 4-agent AI tribunal on incident reports.
* Unlike passive RAG tools, AegisBoard runs a structured adversarial & analytical debate and locks in a **Conclusive Final Suggestion**:
  1. **Definitive Verdict Badge:** (`SUBSTANTIATED VIOLATION`, `PROCEDURAL BREACH ONLY`, or `UNSUBSTANTIATED / CLEARED`) + Consensus Confidence Score (%).
  2. **Primary Conclusive Action / Sanction:** One decisive, actionable punishment or remediation step grounded directly in the rulebook's penalty schedule.
  3. **Policy Vulnerability & Loophole Alert:** Highlights ambiguous clauses in the organization's rulebook that caused debate and suggests exact rewrites.

### 2.2 The 4 Debating AI Characters & Multi-Model Runtime Routing (Maximizing the 50% "ModelScope AI Usage" Criterion)
To actively showcase all 4 approved ModelScope models during live deliberation (with automatic fallback to `zai-org/GLM-5.2` or `Qwen/Qwen3.8-27B` if an endpoint times out):
1. **Bot 1 — The Strict Rule-Checker (`prosecutor` / "LEX-01"):**
   * **Visual:** Crimson visor (`#ef4444`).
   * **Routed Model:** `Qwen/Qwen3.8-27B` — for rapid literal clause extraction, strict violation detection, and citation matching.
2. **Bot 2 — The Contextual / Intent Analyst (`defense` / "CTX-02"):**
   * **Visual:** Teal visor (`#14b8a6`).
   * **Routed Model:** `stepfun-ai/Step-3.5-Flash` — for low-latency analysis of mitigating factors, *mens rea* (intent vs. accident), situational pressures, and policy ambiguity.
3. **Bot 3 — The Ethics & Precedent Evaluator (`ethics` / "ETH-03"):**
   * **Visual:** Amber visor (`#f59e0b`).
   * **Routed Model:** `zai-org/GLM-5.2` — for nuanced evaluation of proportionality, organizational core values, spirit of the policy, and precedent consistency.
4. **Bot 4 — The Board Chair (`chair` / "CHR-04" / Chief Synthesizer):**
   * **Visual:** Gold/Royal visor (`#eab308`) with gavel.
   * **Routed Model:** `deepseek-ai/DeepSeek-V4-Pro-0813` — moderates the debate, weighs the Contextual/Intent Analyst and Ethics/Precedent Evaluator arguments against the Strict Rule-Checker, generates clarifying questions for the user, and locks in the **Conclusive Final Verdict + Primary Recommended Action/Punishment + Policy Vulnerability Patch** in strict JSON format.

### 2.3 Mandatory Dual-Requirement Case Intake
* The **"Convene Advisory Board"** execution is **strictly blocked/locked** unless the user provides **BOTH**:
  1. **Rulebook / Context Document:** Uploaded via file picker (`.pdf`, `.txt`, `.md`) or loaded via one of the 3 built-in one-click Demo Scenarios (Campus Academic Integrity, Corporate Data Security, E-Commerce Seller Policy).
  2. **Manual Case Explanation Prompt:** A written narrative in the prompt box explaining what happened, who was involved, and the context of the case (minimum 20 characters).

### 2.4 UI/UX Visual Specification & "Floating-Limb Chibi Astro-Bot" Pure SVG/CSS Architecture (No External Skin Packs)
Built as a single self-contained **Gradio (`gr.Blocks`)** web app with forced dark mode (`js="() => { document.body.classList.add('dark'); }"`) and custom CSS/HTML/SVG injection:

* **CRITICAL CONSTRAINT FOR OPENCODE (No Freehand SVG Paths):**
  * Explicitly forbid the coding model from using freehand SVG `<path>` coordinates to draw robot arms, elbows, or legs.
  * Require it to render **"Floating-Limb Chibi Bots"** (inspired by Astro Bot and EVE) using deterministic geometric SVG primitives (`<rect rx="...">`, `<circle>`, `<ellipse>`, `<radialGradient>`, and `<filter>`).
* **Left Column — Grounded Rulebook & Case Intake:**
  * One-Click Demo Scenario Selector (Campus Academic Integrity, Corporate Data Security, E-Commerce Seller Policy) + File Upload (`.pdf`, `.txt`, `.md`).
  * Mandatory Narrative Prompt Textbox + Dual-Gate Validation Banner.
  * **Grounded Policy Viewer:** Scrollable document viewer that automatically highlights cited clauses (e.g., `[Clause X.Y]`) in glowing amber/yellow when the bots reference them.
* **Center Column — The 2D Interactive Council Stage (`.council-stage`):**
  * **Interactive Stage Controls (Top of Center Column):**
    1. **Room Theme Selector:** Switches CSS variables on `.council-stage` between `Classic Tribunal` (warm mahogany/amber gold), `Cyber War Room` (deep slate/neon cyan grid), and `Zen Boardroom` (frosted glass/emerald slate).
    2. **Seating Orientation Selector:** Switches layout between `Semicircle Tribunal` (all 4 bots arranged in an arc facing the user) and `Adversarial Arena` (Strict Rule-Checker and Contextual Analyst facing each other on opposite sides, with Ethics and the Board Chair centered).
    3. **Phase 2 Roadmap Preview Badge:** A clickable accordion/modal showing the v2.0 Three.js/WebGL 3D Courtroom upgrade path.
  * **Cutscene Deliberation Flow (`yield`):** When the user clicks "Convene Advisory Board", the Python generator yields HTML stage updates sequentially so each bot animates one by one:
    * Active bot switches to `.state-speaking` or `.state-objecting`, displaying a comic-style `<div class="speech-cloud">` directly above its head with its live argument and clause citation (`[Clause X.Y]`).
    * An animated SVG overlay draws glowing dashed connection lines (`stroke-dasharray: 8 6; animation: dash-flow 0.8s linear infinite`) linking the active bot to the bot it is challenging or synthesizing.
  * **Interactive Board Consultation Bar:** Below the stage, the Board Chair poses 2 clarifying questions to the human user. The user can type additional facts or answers to trigger a **Follow-up Re-Deliberation**.
* **Right Column — The Conclusive Verdict & Action Dossier:**
  * **Conclusive Verdict Card:** High-impact badge (`SUBSTANTIATED VIOLATION`, `PROCEDURAL BREACH ONLY`, or `UNSUBSTANTIATED / CLEARED`) with confidence meter.
  * **Primary Recommended Action / Sanction Box:** Clear, decisive enforcement action/punishment grounded in the rulebook.
  * **Role Fulfillment Breakdown:** Dedicated cards showing how the *Strict Rule-Checker*, *Contextual/Intent Analyst*, and *Ethics/Precedent Evaluator* shaped the decision (along with the ModelScope model badge used for each).
  * **Policy Vulnerability Patch:** Specific clause rewrite recommendation + Export Case Brief (`.md`) button.

---

## 3. 2-Person Workload Split (1,000 Combined Magic Cubes/Day) & Timeline (Nov 2 – Nov 4, 2026)

As a strictly 2-person team, divide responsibilities across your **1,000 combined daily Magic Cubes** as follows:

* **Member 1 (Lead Architect, Prompt Engineer & Backend Logic):**
  * **Tool & Model Selection:** Uses OpenCode configured with `deepseek-ai/DeepSeek-V4-Pro-0813` for initial full-stack generation (**Prompt 1**) and `zai-org/GLM-5.2` for targeted backend edits (**Prompt 3**).
  * **Responsibilities:** Builds the core `app.py` architecture, ModelScope OpenAI-compatible API client (`https://api-inference.modelscope.ai/v1`), Multi-Model Runtime Routing across all 4 approved models with automatic fallback, the Mandatory Dual-Gate Intake validator (blocking execution unless both the Rulebook/Context file AND the manual narrative explanation are provided), the step-by-step generator (`yield`) cutscene state machine, and the interactive Board Chair follow-up interrogation loop.
  * **Quota Strategy:** Uses Member 1's 500 daily Magic Cubes (350 daily login + 150 competition bonus) for backend and pipeline iterations.

* **Member 2 (UI/UX Stage Director, Demo Case Creator & Deployment/Submission Lead):**
  * **Tool & Model Selection:** Uses OpenCode configured with `zai-org/GLM-5.2` (**Prompt 2**) to refine front-end CSS keyframes, SVG robot sprites, speech bubbles, and layout responsiveness.
  * **Responsibilities:** Polishes the 2D Interactive Council Stage, creates the 3 built-in one-click Demo Scenarios (Campus Academic Integrity, Corporate Data Security, E-Commerce Seller Policy), executes **STEP E** (deploying to ModelScope Studio on Free CPU with `MODELSCOPE_API_KEY` stored in Studio Secrets), and compiles the **STEP F** Google Form submission package (project `.zip`, 2–3 key prompts, and OpenCode screenshots clearly showing the approved model name in the top-right corner).
  * **Quota Strategy:** Uses Member 2's separate 500 daily Magic Cubes for UI/UX refinement and live Studio testing.

### Master Schedule
* **Monday Night (2 Nov):** Complete Steps A, B, and C (Account Binding + OpenCode Config). Member 1 runs **Master Prompt 1** (`deepseek-ai/DeepSeek-V4-Pro-0813`) in OpenCode before midnight WIB to utilize Monday's Magic Cubes.
* **Tuesday (3 Nov):** Member 2 runs **Master Prompt 2** (`zai-org/GLM-5.2` — Visual Stage, Keyframes, 3 Demo Scenarios, Phase 2 Preview & Dossier Export) and Member 1 runs **Master Prompt 3** (`zai-org/GLM-5.2` — Backend Resilience, Fallback Routing & Dark UI Polish). Deploy initial build to ModelScope Studio (**STEP E**).
* **Wednesday Morning (4 Nov, 09:00 – 15:00 WIB):** Final QA test on the public ModelScope Studio link, package the `.zip` archive, verify all OpenCode screenshots showing the approved model names in the top-right corner, and finalize the report.
* **Wednesday Afternoon (4 Nov, 16:00 – 23:59 WIB):** Submit via the WhatsApp Group Google Form (**STEP F** — window closes strictly at **23:59 WIB**). Screenshot the submission confirmation page!

---
---

# PART II: STEP-BY-STEP EXECUTION GUIDE (FROM FIRST STEP TO LAST STEP)

---

## 4. [Step 1] Environment Setup Checklist (Steps A, B & C from Guidebook)

### STEP A: Bind Alibaba Cloud International Account
1. Log in at [https://modelscope.ai](https://modelscope.ai).
2. Click your **Avatar (top-right)** $\rightarrow$ **"Alibaba Cloud — Bind immediately"**.
3. Click **"Link your Alibaba Cloud account to get free resources"**.
4. Sign in to your Alibaba Cloud International account (or register one).
5. On the **Third-party Application Admin Authorization** screen, keep all 3 permissions checked (`OpenID`, `UID`, `Profile`) and click **Authorize**.
6. Confirm you are redirected back to ModelScope Settings and your Alibaba Cloud email is visible under **Basic Information**.

### STEP B: Create Your ModelScope Access Token
1. In ModelScope, click your **Avatar (top-right)** $\rightarrow$ **Settings** $\rightarrow$ **Access Tokens** (left sidebar).
2. Click **Create Your Token** $\rightarrow$ select **Fine-grained permission token**.
3. Enter token name: `coding token`, select **Long-term use**, check **Invoke API Inference**, and click **Create Token**.
4. Click **Copy** and save your token somewhere private on your computer. *(Never put this inside your code files!)*

### STEP C: Install & Configure OpenCode (Recommended) or Claude Code
Ensure **Node.js 18+** is installed (`node -v`).

#### Option 1: OpenCode (Recommended — Shows Model Name Clearly in Top-Right UI for Screenshots)
1. Open Terminal (Mac) or PowerShell (Windows).
2. Install OpenCode globally:
   ```bash
   npm install -g opencode-ai
   ```
   *(Windows PowerShell Note: If it says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, type `Y`, press Enter, and retry).*
3. Create the OpenCode configuration file:
   * **Mac:**
     ```bash
     mkdir -p ~/.config/opencode
     nano ~/.config/opencode/opencode.json
     ```
   * **Windows PowerShell:**
     ```powershell
     mkdir $HOME\.config\opencode -Force
     notepad $HOME\.config\opencode\opencode.json
     ```
4. Paste this **exact** JSON (replace `your_modelscope_token` with your actual token from Step B):
   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "model": "modelscope_ai/deepseek-ai/DeepSeek-V4-Pro-0813",
     "provider": {
       "modelscope_ai": {
         "npm": "@ai-sdk/openai-compatible",
         "name": "ModelScope International",
         "options": {
           "baseURL": "https://api-inference.modelscope.ai/v1",
           "apiKey": "your_modelscope_token"
         },
         "models": {
           "zai-org/GLM-5.2": {
             "name": "GLM-5.2"
           },
           "deepseek-ai/DeepSeek-V4-Pro-0813": {
             "name": "DeepSeek V4 Pro"
           },
           "stepfun-ai/Step-3.5-Flash": {
             "name": "Step 3.5 Flash"
           },
           "Qwen/Qwen3.8-27B": {
             "name": "Qwen3.8 27B"
           }
         }
       }
     }
   }
   ```
5. Save and close (`Ctrl+O`, `Enter`, `Ctrl+X` in nano; `Ctrl+S` in Notepad).
6. Tip: Inside OpenCode, you can type `/models` at any time to switch between `DeepSeek V4 Pro` (Member 1 — Prompt 1) and `GLM-5.2` (Member 2 — Prompt 2 & Member 1 — Prompt 3).

---

## 5. [Step 2] Local Project Folder & Zero-Human-Code Setup

1. Open Terminal / PowerShell and create a clean project folder:
   ```bash
   mkdir aegisboard-tribunal
   cd aegisboard-tribunal
   ```
2. Set your environment variable locally in your terminal session so when you test the app locally, Python can read your token without hardcoding it:
   * **Mac / Linux:**
     ```bash
     export MODELSCOPE_API_KEY="your_modelscope_token"
     ```
   * **Windows PowerShell:**
     ```powershell
     $env:MODELSCOPE_API_KEY="your_modelscope_token"
     ```
3. Launch OpenCode inside the `aegisboard-tribunal` folder:
   ```bash
   opencode
   ```
4. **Connectivity Check:** Type `"Verify connectivity by listing files in the current directory"` and take your first screenshot showing the approved model name in the top-right corner!

---

## 6. [Step 3] The 3 Master Vibecoding Prompts (Copy-Paste into OpenCode)

> **CRITICAL REMINDER:** Copy and paste these prompts one at a time into OpenCode. After each prompt finishes generating the files, **TAKE A SCREENSHOT** of the OpenCode window (clearly showing both your prompt and the approved model name in the top-right corner) and save it to a separate `screenshots_for_submission` folder outside your project directory! Also save these 3 prompts for the Google Form submission.

---

### 🚀 MASTER PROMPT 1 (Member 1 — `deepseek-ai/DeepSeek-V4-Pro-0813`): Core Multi-Model Tribunal Engine, Yield Cutscene Generator & Floating-Limb Chibi Bot Stage
*(Member 1 pastes this into OpenCode using `deepseek-ai/DeepSeek-V4-Pro-0813`. It builds the complete working `app.py`, `requirements.txt`, and `.gitignore`. Take Screenshot #1!)*

````text
Build a complete, production-ready Python Gradio web application in `app.py` and generate `requirements.txt` (plus `.gitignore`) for a project called "AegisBoard: Multi-Agent Policy & Rulebook Advisory Tribunal".

STRICT COMPETITION CONSTRAINTS (MUST FOLLOW):
1. All AI inference calls inside `app.py` MUST use the OpenAI-compatible client (`openai` Python SDK) pointing strictly to `base_url="https://api-inference.modelscope.ai/v1"`.
2. NEVER hardcode any API key or token in the source code. Read the API key strictly from environment variables (`os.getenv("MODELSCOPE_API_KEY") or os.getenv("MODELSCOPE_SDK_TOKEN")`), with an optional password-masked fallback textbox in a collapsible top settings bar ONLY if the environment variable is not set.
3. Only the 4 approved ModelScope models may be used anywhere in the application:
   - `deepseek-ai/DeepSeek-V4-Pro-0813`
   - `zai-org/GLM-5.2`
   - `Qwen/Qwen3.8-27B`
   - `stepfun-ai/Step-3.5-Flash`
4. Do NOT use any other models or external paid APIs. Ensure it runs smoothly on Free CPU-only environments.

APPLICATION ARCHITECTURE & MULTI-MODEL RUNTIME ROUTING:
1. MANDATORY DUAL-REQUIREMENT CASE INTAKE:
   - Users must provide BOTH:
     (a) Organization Policy/Rulebook & Context Report: via file upload (supporting `.txt`, `.md`, `.pdf` using `pypdf`) OR by loading one of 3 rich built-in one-click Demo Scenarios ("Campus Academic Integrity", "Corporate Data Security", "E-Commerce Seller Policy").
     (b) Mandatory Manual Case Explanation Prompt: A narrative textbox where the user manually explains what happened, who was involved, and the dilemma.
   - Validation Gate: If EITHER the Policy/Rulebook text OR the Manual Case Explanation (minimum 20 characters) is missing, block deliberation and display a clear warning banner instructing the user to provide both inputs.

2. MULTI-MODEL RUNTIME ROUTING FOR THE 4 DEBATING AI CHARACTERS (WITH AUTOMATIC FALLBACK):
   Actively route each of the 4 tribunal personas to its dedicated approved ModelScope model during live deliberation, with automatic fallback to `zai-org/GLM-5.2` or `Qwen/Qwen3.8-27B` if an endpoint times out or errors:
   - Bot 1 (`prosecutor` / "LEX-01: Strict Rule-Checker", Crimson `#ef4444`): Routed to `Qwen/Qwen3.8-27B` for rapid literal clause extraction, strict violation lookup, and citation matching (`[Clause X.Y]`).
   - Bot 2 (`defense` / "CTX-02: Contextual & Intent Analyst", Teal `#14b8a6`): Routed to `stepfun-ai/Step-3.5-Flash` for low-latency analysis of mitigating factors, intent vs. accident, situational pressure, and policy ambiguity.
   - Bot 3 (`ethics` / "ETH-03: Ethics & Precedent Evaluator", Amber `#f59e0b`): Routed to `zai-org/GLM-5.2` for nuanced evaluation of proportionality, organizational values, spirit vs. letter of the rule, and precedent consistency.
   - Bot 4 (`chair` / "CHR-04: Chief Board Chair", Gold `#eab308`): Routed to `deepseek-ai/DeepSeek-V4-Pro-0813` to moderate the debate, weigh the Defense and Ethics arguments against the Prosecutor, generate 2 clarifying questions for the human user, and lock in the Conclusive Final Verdict + Primary Recommended Action/Punishment + Policy Vulnerability Patch in strict JSON format.

3. CUTSCENE DELIBERATION FLOW (`yield` GENERATOR STATE MACHINE):
   - When the user clicks "Convene Advisory Board", use a Python generator function (`yield`) to stream HTML stage updates sequentially so each bot animates one by one in a live courtroom cutscene:
     * Step 1: Yield initial scanning state (`.state-scanning`) across the council.
     * Step 2: Run & yield Bot 1 (`prosecutor` on `Qwen/Qwen3.8-27B`) in `.state-speaking` with its comic `<div class="speech-cloud">` and `[Clause X.Y]` citation highlighted in the Grounded Policy Viewer.
     * Step 3: Run & yield Bot 2 (`defense` on `stepfun-ai/Step-3.5-Flash`) in `.state-objecting` / `.state-speaking` with an animated SVG dashed beam (`stroke-dasharray: 8 6; animation: dash-flow 0.8s linear infinite`) challenging the Prosecutor.
     * Step 4: Run & yield Bot 3 (`ethics` on `zai-org/GLM-5.2`) in `.state-speaking` with connecting workflow beams.
     * Step 5: Run & yield Bot 4 (`chair` on `deepseek-ai/DeepSeek-V4-Pro-0813`) in `.state-verdict`, locking in the Right Column Conclusive Verdict Dossier and populating the Interactive Consultation Bar with 2 clarifying questions.

4. CRITICAL SVG/CSS CONSTRAINT — "FLOATING-LIMB CHIBI ASTRO-BOTS" (NO FREEHAND SVG PATHS):
   - FORBIDDEN: Do NOT use freehand SVG `<path>` coordinates to draw robot arms, elbows, or legs.
   - REQUIRED: Render "Floating-Limb Chibi Bots" (inspired by Astro Bot and EVE) using ONLY deterministic geometric SVG primitives (`<rect rx="...">`, `<circle>`, `<ellipse>`, `<radialGradient>`, and `<filter>`).
   - Embed and use this exact parameterized Python helper function to render each of the 4 bots so their geometry is 100% symmetric and toy-like:

```python
def render_chibi_bot_svg(role_id: str, name: str, accent_color: str, state: str, speech_text: str = "") -> str:
    """
    role_id: 'prosecutor' (Crimson #ef4444), 'defense' (Teal #14b8a6),
             'ethics' (Amber #f59e0b), 'chair' (Gold #eab308)
    state: 'idle' | 'scanning' | 'speaking' | 'objecting' | 'verdict'
    """
    # Role-specific LED eye expressions inside the visor
    eyes_svg = {
        "prosecutor": f'<rect class="led-eye" x="54" y="58" width="18" height="8" rx="4" fill="{accent_color}" transform="rotate(12 63 62)"/><rect class="led-eye" x="88" y="58" width="18" height="8" rx="4" fill="{accent_color}" transform="rotate(-12 97 62)"/>',
        "defense": f'<ellipse class="led-eye" cx="63" cy="62" rx="9" ry="10" fill="{accent_color}"/><ellipse class="led-eye" cx="97" cy="62" rx="9" ry="10" fill="{accent_color}"/><circle cx="66" cy="59" r="3" fill="#ffffff"/><circle cx="100" cy="59" r="3" fill="#ffffff"/>',
        "ethics": f'<circle class="led-eye" cx="63" cy="62" r="8" stroke="{accent_color}" stroke-width="3" fill="none"/><circle class="led-eye" cx="97" cy="62" r="8" stroke="{accent_color}" stroke-width="3" fill="none"/><circle cx="63" cy="62" r="3" fill="{accent_color}"/><circle cx="97" cy="62" r="3" fill="{accent_color}"/>',
        "chair": f'<rect class="led-eye" x="54" y="56" width="18" height="11" rx="5" fill="{accent_color}"/><rect class="led-eye" x="88" y="56" width="18" height="11" rx="5" fill="{accent_color}"/><g class="chair-gavel"><rect x="128" y="88" width="6" height="32" rx="3" fill="#d97706"/><rect x="118" y="82" width="26" height="12" rx="4" fill="{accent_color}"/></g>'
    }.get(role_id, "")

    speech_html = f'<div class="speech-cloud" style="border-color:{accent_color};">{speech_text}</div>' if speech_text else ''

    return f'''
    <div class="bot-unit bot-{role_id} state-{state}" style="--accent: {accent_color};">
      {speech_html}
      <svg class="chibi-svg" viewBox="0 0 160 185" width="145" height="165" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="shell-{role_id}" cx="35%" cy="25%" r="70%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="65%" stop-color="#e2e8f0"/>
            <stop offset="100%" stop-color="#94a3b8"/>
          </radialGradient>
          <filter id="glow-{role_id}" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="{accent_color}" flood-opacity="0.45"/>
          </filter>
        </defs>
        <!-- Ground Shadow -->
        <ellipse class="bot-shadow" cx="80" cy="172" rx="34" ry="7" fill="rgba(0,0,0,0.28)"/>
        <!-- Antenna -->
        <g class="bot-head-group">
          <line x1="80" y1="26" x2="80" y2="12" stroke="#cbd5e1" stroke-width="4" stroke-linecap="round"/>
          <circle class="antenna-tip" cx="80" cy="10" r="6" fill="{accent_color}" filter="url(#glow-{role_id})"/>
          <!-- Glossy Chibi Head -->
          <rect x="34" y="24" width="92" height="68" rx="32" fill="url(#shell-{role_id})" stroke="#cbd5e1" stroke-width="2"/>
          <!-- Side Ear Pods -->
          <rect x="24" y="46" width="10" height="24" rx="5" fill="{accent_color}"/>
          <rect x="126" y="46" width="10" height="24" rx="5" fill="{accent_color}"/>
          <!-- Dark Glass Visor -->
          <rect x="44" y="38" width="72" height="42" rx="18" fill="#0f172a" stroke="{accent_color}" stroke-width="1.5"/>
          <!-- Visor Gloss Reflection -->
          <ellipse cx="62" cy="45" rx="16" ry="4" fill="rgba(255,255,255,0.18)" transform="rotate(-8 62 45)"/>
          <!-- Role LED Eyes -->
          {eyes_svg}
        </g>
        <!-- Glossy Chibi Torso -->
        <g class="bot-torso-group">
          <rect x="52" y="98" width="56" height="52" rx="24" fill="url(#shell-{role_id})" stroke="#cbd5e1" stroke-width="2"/>
          <!-- Core Emblem -->
          <circle class="core-badge" cx="80" cy="122" r="10" fill="#0f172a" stroke="{accent_color}" stroke-width="2"/>
          <circle cx="80" cy="122" r="5" fill="{accent_color}" filter="url(#glow-{role_id})"/>
        </g>
        <!-- Floating Sphere Hands (No Stick Limbs) -->
        <circle class="hand-left" cx="30" cy="120" r="11" fill="url(#shell-{role_id})" stroke="{accent_color}" stroke-width="2"/>
        <circle class="hand-right" cx="130" cy="120" r="11" fill="url(#shell-{role_id})" stroke="{accent_color}" stroke-width="2"/>
      </svg>
      <div class="bot-label">{name}</div>
      <div class="bot-state-badge">{state.upper()}</div>
    </div>
    '''
```

   - Required CSS Keyframe Animations to Include:
     * `.state-idle .bot-head-group, .state-idle .bot-torso-group`: smooth vertical hover (`translateY(-5px)` over `2.4s ease-in-out infinite`) + `.led-eye` blink (`scaleY(0.1)` at 92% keyframe).
     * `.state-scanning .antenna-tip`: fast neon pulse (`scale(1.4)`) + scanning visor sweep.
     * `.state-speaking`: energetic bounce (`translateY(-10px) scale(1.04)`), glowing aura border around the bot unit, and pop-in `.speech-cloud` animation (`cubic-bezier(0.34, 1.56, 0.64, 1)`).
     * `.state-objecting`: rapid horizontal shake (`translateX(-5px)` to `translateX(5px)`), `.hand-left` and `.hand-right` raised high (`translateY(-22px)`).
     * `.state-verdict .chair-gavel`: gavel strike rotation (`rotate(-38deg)` to `rotate(12deg)`).

5. 3-COLUMN GAMIFIED UI/UX LAYOUT (`gr.Blocks` with Forced Dark Theme & Custom CSS):
   - Force Dark Theme Mode: Add `js="() => { document.body.classList.add('dark'); }"` to `gr.Blocks(...)` and style all Gradio accordions, textboxes, and dropdowns with dark glassmorphic styling matching the dark canvas (`#0b0e1c`), preventing stark white light-mode card clashes.
   - LEFT COLUMN (Rulebook & Intake Locker):
     * One-Click Demo Scenario Selector ("Campus Academic Integrity", "Corporate Data Security", "E-Commerce Seller Policy") + File Upload (`.pdf`, `.txt`, `.md`) + editable Rulebook Textbox.
     * Mandatory Manual Case Narrative Prompt Textbox.
     * "Convene Advisory Board" primary button.
     * Grounded Policy Viewer (HTML panel) that highlights exact clauses (`[Clause X.Y]`) cited by the bots.
   - CENTER COLUMN (The 2D Interactive Council Stage `.council-stage`):
     * Top Interactive Stage Controls:
       1. Room Theme Selector: Switches CSS variables on `.council-stage` between `Classic Tribunal` (warm mahogany/amber gold), `Cyber War Room` (deep slate/neon cyan grid), and `Zen Boardroom` (frosted glass/emerald slate).
       2. Seating Orientation Selector: Switches layout between `Semicircle Tribunal` (all 4 bots arranged in an arc facing the user) and `Adversarial Arena` (Strict Rule-Checker and Contextual Analyst facing each other on opposite sides, with Ethics and the Board Chair centered).
       3. Phase 2 Roadmap Preview Badge: A clickable accordion/modal showing the v2.0 Three.js/WebGL 3D Courtroom upgrade path.
     * Animated `.council-stage` container rendering the 4 `render_chibi_bot_svg(...)` units, speech clouds, model badges, and SVG dashed workflow connection beams (`stroke-dasharray: 8 6; animation: dash-flow 0.8s linear infinite`).
     * Interactive Consultation Bar below the stage: Displays the Board Chair's 2 clarifying questions, a follow-up answer textbox, and a "Submit Follow-Up Context to Board" button that triggers a re-deliberation loop.
   - RIGHT COLUMN (Conclusive Final Verdict & Action Dossier):
     * Conclusive Final Verdict Banner (`SUBSTANTIATED VIOLATION`, `PROCEDURAL BREACH ONLY`, or `UNSUBSTANTIATED / CLEARED`), Consensus Confidence %, and Severity Tier.
     * Conclusive Primary Action / Sanction Card.
     * Role Fulfillment Breakdown (showing Prosecutor, Defense, Ethics, and Chair conclusions + active ModelScope model badges).
     * Policy Vulnerability & Loophole Patch card with exact suggested clause rewrite.

Ensure `requirements.txt` contains clean, standard packages (`gradio`, `openai`, `pypdf`) so it deploys without build errors on ModelScope Studio CPU.
````

---

### 🎨 MASTER PROMPT 2 (Member 2 — `zai-org/GLM-5.2`): Chibi Astro-Bot Keyframes, Stage Layouts, 3 Demo Scenarios & Dossier Export
*(Switch OpenCode model to `zai-org/GLM-5.2` via `/models`. Member 2 runs this prompt to refine the front-end CSS keyframes, SVG sprite animations, speech bubbles, 3 rich Demo Scenarios, Phase 2 3D Preview, and Markdown export. Take Screenshot #2!)*

````text
Enhance `app.py` with refined front-end CSS keyframe animations, responsive stage layouts, rich built-in demo cases, and dossier export while strictly preserving the 4-model runtime routing (`Qwen/Qwen3.8-27B`, `stepfun-ai/Step-3.5-Flash`, `zai-org/GLM-5.2`, `deepseek-ai/DeepSeek-V4-Pro-0813`), the `render_chibi_bot_svg` Floating-Limb Chibi Bot primitive specification (NO freehand SVG `<path>` limbs), and environment-variable token security:

1. FLOATING-LIMB CHIBI BOT CSS KEYFRAMES & STATE MACHINE:
   - Refine CSS animations for `.bot-unit` and its child SVG groups (`.bot-head-group`, `.bot-torso-group`, `.hand-left`, `.hand-right`, `.led-eye`, `.chair-gavel`, `.bot-shadow`):
     * `.state-idle`: Gentle floating hover (`translateY`) with independent delayed bobbing on `.hand-left` and `.hand-right` and synchronized `.bot-shadow` scaling.
     * `.state-scanning`: Visor `.led-eye` horizontal scan sweep and glowing antenna pulse while inspecting the rulebook.
     * `.state-speaking`: Energetic talk bounce, glowing border pulse on `.speech-cloud`, and expressive hand gestures using `transform: translate(...)` on the floating sphere hands.
     * `.state-objecting`: Rapid objection hop/shake, intense crimson/teal drop-shadow glow, and animated SVG dashed challenge beam (`stroke-dasharray: 8 6; animation: dash-flow 0.8s linear infinite`).
     * `.state-verdict`: Board Chair `.chair-gavel` strike animation and golden aura lock-in.

2. STAGE THEMES, SEATING ORIENTATIONS & PHASE 2 3D PREVIEW:
   - Ensure the `.council-stage` CSS variables smoothly transition between:
     * `Classic Tribunal` (warm mahogany wood tones & amber gold lighting),
     * `Cyber War Room` (deep slate & neon cyan perspective grid),
     * `Zen Boardroom` (frosted glass & emerald slate).
   - Ensure the Seating Orientation toggle cleanly rearranges the 4 `.bot-unit` cards between `Semicircle Tribunal` (4-bot arc facing the user) and `Adversarial Arena` (Prosecutor `LEX-01` and Defense `CTX-02` facing each other on opposite sides, with Ethics `ETH-03` and Chair `CHR-04` centered), dynamically adjusting the SVG overlay connection lines to match.
   - Polish the clickable "Phase 2 Roadmap Preview Badge" accordion/modal showcasing how the exact state machine (`idle`, `scanning`, `speaking`, `objecting`, `verdict`) maps to the v2.0 Three.js/WebGL 3D Courtroom upgrade path.

3. 3 RICH ONE-CLICK DEMO SCENARIOS & EXPORTABLE DOSSIER:
   - Ensure the 3 built-in Demo Scenarios ("Campus Academic Integrity", "Corporate Data Security", "E-Commerce Seller Policy") contain detailed, multi-clause policy rulebooks (with numbered sections like `Clause 1.1`, `Clause 2.3`, `Clause 4.2` and explicit penalty schedules) paired with nuanced, morally grey incident narratives that trigger lively clashes between `LEX-01`, `CTX-02`, and `ETH-03`.
   - Add a "Download Official Advisory Dossier (.md)" button in the Right Column that exports a formatted Markdown report (Case Summary, Multi-Model Agent Arguments & Cited Clauses, User Consultation Q&A, Conclusive Final Verdict, Primary Sanction, and Policy Vulnerability Patch), and generate a clean `README.md`.
````

---

### 🛡️ MASTER PROMPT 3 (Member 1 / Member 2 — `zai-org/GLM-5.2` or `deepseek-ai/DeepSeek-V4-Pro-0813`): Complete Multi-Model Routing, Floating-Limb Chibi Bot SVG Upgrade, `yield` Cutscene & Dark Glassmorphic Polish
*(Since Prompts 1 & 2 have already been executed on `app.py`, paste this comprehensive Master Prompt 3 into OpenCode right now to upgrade `app.py` with the active 4-Model Runtime Routing, the exact `render_chibi_bot_svg` Floating-Limb Chibi Astro-Bot specification, the sequential `yield` cutscene generator, Interactive Stage Controls, and the Permanent Dark Theme fix! Take Screenshot #3!)*

````text
Upgrade and refactor `app.py` (and `README.md`) to lock in all final architectural, visual, and multi-model competition requirements while strictly preserving environment-variable token security (`os.getenv("MODELSCOPE_API_KEY") or os.getenv("MODELSCOPE_SDK_TOKEN")`) and `base_url="https://api-inference.modelscope.ai/v1"`:

1. ACTIVE 4-MODEL RUNTIME ROUTING BY DEFAULT (WITH AUTOMATIC FALLBACK):
   - Make multi-model routing the active default behavior so every deliberation showcases all 4 approved ModelScope models live:
     1. Prosecutor / Strict Rule-Checker (`role_id="prosecutor"`, "LEX-01", Crimson `#ef4444`): Routed to `Qwen/Qwen3.8-27B` for rapid literal clause extraction and citation matching.
     2. Defense / Contextual & Intent Analyst (`role_id="defense"`, "CTX-02", Teal `#14b8a6`): Routed to `stepfun-ai/Step-3.5-Flash` for low-latency analysis of mitigating factors, intent vs. accident, and policy ambiguity.
     3. Ethics & Precedent Evaluator (`role_id="ethics"`, "ETH-03", Amber `#f59e0b`): Routed to `zai-org/GLM-5.2` for nuanced evaluation of proportionality, organizational values, and precedent consistency.
     4. Board Chair / Chief Synthesizer (`role_id="chair"`, "CHR-04", Gold `#eab308`): Routed to `deepseek-ai/DeepSeek-V4-Pro-0813` for generating 2 clarifying questions for the user and locking in the Conclusive Final Verdict + Primary Recommended Action/Punishment + Policy Vulnerability Patch in strict JSON format.
   - Wrap each model call in a try/except fallback handler so if an endpoint times out or rate-limits, it automatically falls back to `zai-org/GLM-5.2` or `Qwen/Qwen3.8-27B` without crashing.

2. LOCK IN THE "FLOATING-LIMB CHIBI ASTRO-BOT" PURE SVG & CSS TEMPLATE (NO FREEHAND PATHS):
   - FORBIDDEN: Remove any freehand SVG `<path>` coordinates used for robot arms, elbows, or legs.
   - REQUIRED: Replace the bot avatar renderer with this exact parameterized Python helper function using deterministic geometric SVG primitives (`<rect rx="...">`, `<circle>`, `<ellipse>`, `<radialGradient>`, `<filter>`):

```python
def render_chibi_bot_svg(role_id: str, name: str, accent_color: str, state: str, speech_text: str = "") -> str:
    """
    role_id: 'prosecutor' (Crimson #ef4444), 'defense' (Teal #14b8a6),
             'ethics' (Amber #f59e0b), 'chair' (Gold #eab308)
    state: 'idle' | 'scanning' | 'speaking' | 'objecting' | 'verdict'
    """
    # Role-specific LED eye expressions inside the visor
    eyes_svg = {
        "prosecutor": f'<rect class="led-eye" x="54" y="58" width="18" height="8" rx="4" fill="{accent_color}" transform="rotate(12 63 62)"/><rect class="led-eye" x="88" y="58" width="18" height="8" rx="4" fill="{accent_color}" transform="rotate(-12 97 62)"/>',
        "defense": f'<ellipse class="led-eye" cx="63" cy="62" rx="9" ry="10" fill="{accent_color}"/><ellipse class="led-eye" cx="97" cy="62" rx="9" ry="10" fill="{accent_color}"/><circle cx="66" cy="59" r="3" fill="#ffffff"/><circle cx="100" cy="59" r="3" fill="#ffffff"/>',
        "ethics": f'<circle class="led-eye" cx="63" cy="62" r="8" stroke="{accent_color}" stroke-width="3" fill="none"/><circle class="led-eye" cx="97" cy="62" r="8" stroke="{accent_color}" stroke-width="3" fill="none"/><circle cx="63" cy="62" r="3" fill="{accent_color}"/><circle cx="97" cy="62" r="3" fill="{accent_color}"/>',
        "chair": f'<rect class="led-eye" x="54" y="56" width="18" height="11" rx="5" fill="{accent_color}"/><rect class="led-eye" x="88" y="56" width="18" height="11" rx="5" fill="{accent_color}"/><g class="chair-gavel"><rect x="128" y="88" width="6" height="32" rx="3" fill="#d97706"/><rect x="118" y="82" width="26" height="12" rx="4" fill="{accent_color}"/></g>'
    }.get(role_id, "")

    speech_html = f'<div class="speech-cloud" style="border-color:{accent_color};">{speech_text}</div>' if speech_text else ''

    return f'''
    <div class="bot-unit bot-{role_id} state-{state}" style="--accent: {accent_color};">
      {speech_html}
      <svg class="chibi-svg" viewBox="0 0 160 185" width="145" height="165" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="shell-{role_id}" cx="35%" cy="25%" r="70%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="65%" stop-color="#e2e8f0"/>
            <stop offset="100%" stop-color="#94a3b8"/>
          </radialGradient>
          <filter id="glow-{role_id}" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="{accent_color}" flood-opacity="0.45"/>
          </filter>
        </defs>
        <!-- Ground Shadow -->
        <ellipse class="bot-shadow" cx="80" cy="172" rx="34" ry="7" fill="rgba(0,0,0,0.28)"/>
        <!-- Antenna -->
        <g class="bot-head-group">
          <line x1="80" y1="26" x2="80" y2="12" stroke="#cbd5e1" stroke-width="4" stroke-linecap="round"/>
          <circle class="antenna-tip" cx="80" cy="10" r="6" fill="{accent_color}" filter="url(#glow-{role_id})"/>
          <!-- Glossy Chibi Head -->
          <rect x="34" y="24" width="92" height="68" rx="32" fill="url(#shell-{role_id})" stroke="#cbd5e1" stroke-width="2"/>
          <!-- Side Ear Pods -->
          <rect x="24" y="46" width="10" height="24" rx="5" fill="{accent_color}"/>
          <rect x="126" y="46" width="10" height="24" rx="5" fill="{accent_color}"/>
          <!-- Dark Glass Visor -->
          <rect x="44" y="38" width="72" height="42" rx="18" fill="#0f172a" stroke="{accent_color}" stroke-width="1.5"/>
          <!-- Visor Gloss Reflection -->
          <ellipse cx="62" cy="45" rx="16" ry="4" fill="rgba(255,255,255,0.18)" transform="rotate(-8 62 45)"/>
          <!-- Role LED Eyes -->
          {eyes_svg}
        </g>
        <!-- Glossy Chibi Torso -->
        <g class="bot-torso-group">
          <rect x="52" y="98" width="56" height="52" rx="24" fill="url(#shell-{role_id})" stroke="#cbd5e1" stroke-width="2"/>
          <!-- Core Emblem -->
          <circle class="core-badge" cx="80" cy="122" r="10" fill="#0f172a" stroke="{accent_color}" stroke-width="2"/>
          <circle cx="80" cy="122" r="5" fill="{accent_color}" filter="url(#glow-{role_id})"/>
        </g>
        <!-- Floating Sphere Hands (No Stick Limbs) -->
        <circle class="hand-left" cx="30" cy="120" r="11" fill="url(#shell-{role_id})" stroke="{accent_color}" stroke-width="2"/>
        <circle class="hand-right" cx="130" cy="120" r="11" fill="url(#shell-{role_id})" stroke="{accent_color}" stroke-width="2"/>
      </svg>
      <div class="bot-label">{name}</div>
      <div class="bot-state-badge">{state.upper()}</div>
    </div>
    '''
```

   - Required CSS Keyframe Animations to Include:
     * `.state-idle .bot-head-group, .state-idle .bot-torso-group`: smooth vertical hover (`translateY(-5px)` over `2.4s ease-in-out infinite`) + `.led-eye` blink (`scaleY(0.1)` at 92% keyframe).
     * `.state-scanning .antenna-tip`: fast neon pulse (`scale(1.4)`) + scanning visor sweep.
     * `.state-speaking`: energetic bounce (`translateY(-10px) scale(1.04)`), glowing aura border around the bot unit, and pop-in `.speech-cloud` animation (`cubic-bezier(0.34, 1.56, 0.64, 1)`).
     * `.state-objecting`: rapid horizontal shake (`translateX(-5px)` to `translateX(5px)`), `.hand-left` and `.hand-right` raised high (`translateY(-22px)`).
     * `.state-verdict .chair-gavel`: gavel strike rotation (`rotate(-38deg)` to `rotate(12deg)`).

3. INTERACTIVE STAGE CONTROLS & CUTSCENE DELIBERATION FLOW (`yield`):
   - Top of Center Column Controls on `.council-stage`:
     1. Room Theme Selector: Switches CSS variables on `.council-stage` between `Classic Tribunal` (warm mahogany/amber gold), `Cyber War Room` (deep slate/neon cyan grid), and `Zen Boardroom` (frosted glass/emerald slate).
     2. Seating Orientation Selector: Switches layout between `Semicircle Tribunal` (all 4 bots arranged in an arc facing the user) and `Adversarial Arena` (Strict Rule-Checker and Contextual Analyst facing each other on opposite sides, with Ethics and the Board Chair centered).
     3. Phase 2 Roadmap Preview Badge: A clickable accordion/modal showing the v2.0 Three.js/WebGL 3D Courtroom upgrade path.
   - Cutscene Deliberation Flow (`yield`): Convert `convene_board` into a Python generator that yields HTML stage updates sequentially as each bot finishes its inference call:
     * Active bot switches to `.state-speaking` or `.state-objecting`, displaying a comic-style `<div class="speech-cloud">` directly above its head with its live argument and clause citation (`[Clause X.Y]`).
     * An animated SVG overlay draws glowing dashed connection lines (`stroke-dasharray: 8 6; animation: dash-flow 0.8s linear infinite`) linking the active bot to the bot it is challenging or synthesizing.
   - Ensure the 3 built-in one-click Demo Scenarios are named `"Campus Academic Integrity"`, `"Corporate Data Security"`, and `"E-Commerce Seller Policy"`.

4. PERMANENT DARK THEME & CYBER GLASSMORPHISM FIX (ELIMINATE STARK WHITE CARDS):
   - Force dark mode in Gradio by passing `js="() => { document.body.classList.add('dark'); }"` to `gr.Blocks(...)`.
   - Inject comprehensive CSS overrides for `.gradio-container`, `.block`, `.form`, `.accordion`, `input`, `textarea`, `select`, and `.wrap` so all native Gradio widgets use sleek dark slate backgrounds (`#0f172a` / `rgba(16, 20, 38, 0.88)`), subtle borders (`rgba(148, 163, 184, 0.22)`), and crisp light text (`#f1f5f9`), completely eliminating stark white light-mode boxes.
   - Launch with `demo.queue().launch()` so generator `yield` streaming works smoothly on ModelScope Studio Free CPU.
````

---

## 7. [Step 4] Local Testing Checklist (Before Publishing)

Run your app locally in your terminal:
```bash
pip install -r requirements.txt
python app.py
```
Open the local URL shown in the terminal (typically `http://127.0.0.1:7860`) and verify:
- [ ] **Dual-Gate Intake Check:** Try clicking "Convene Advisory Board" with an empty manual explanation box or missing policy $\rightarrow$ Confirm it blocks execution and displays the validation warning banner.
- [ ] **Cutscene `yield` & Multi-Model Check:** Load one of the 3 Demo Scenarios (*Campus Academic Integrity*, *Corporate Data Security*, or *E-Commerce Seller Policy*) and click "Convene Advisory Board" $\rightarrow$ Confirm the 4 Floating-Limb Chibi Bots animate sequentially one-by-one via `yield`, display their comic `<div class="speech-cloud">` with `[Clause X.Y]` citations, highlight clauses in the Left Panel, and lock in the Right Panel **Conclusive Verdict**, **Primary Action**, and **Policy Vulnerability Patch**.
- [ ] **Chibi Bot Geometry Check:** Confirm all 4 bots render with symmetric glossy heads, LED visor expressions, and floating sphere hands (no distorted stick-figure `<path>` limbs).
- [ ] **Stage Controls Check:** Switch the Room Theme (*Classic Tribunal*, *Cyber War Room*, *Zen Boardroom*), toggle Seating Orientation (*Semicircle Tribunal* vs. *Adversarial Arena*), and open the *Phase 2 Roadmap Preview Badge* $\rightarrow$ Confirm all stage visuals update cleanly.
- [ ] **Unified Dark Theme Check:** Confirm the entire interface renders in a cohesive dark glassmorphic aesthetic with zero stark white light-mode boxes.
- [ ] **Interactive Consultation Check:** Type an answer to the Board Chair's clarifying questions and click "Submit Follow-Up Context" $\rightarrow$ Confirm the board re-deliberates and updates the final verdict.
- [ ] **Security Check:** Run `grep -rn "ms-" .` or search `app.py` to be 100% sure your personal ModelScope access token is **NOT** written inside any file.

---

## 8. [Step 5] Step-by-Step ModelScope Studio Deployment (STEP E from Guidebook)

*(Executed by Member 2)*

1. Go to [https://modelscope.ai](https://modelscope.ai), click **Studios** in the top navigation bar $\rightarrow$ click **New Studio** (or click your top-right Avatar $\rightarrow$ **New Studio**).
2. **Fill in the New Studio Form:**
   * **Name:** `AegisBoard-Policy-Tribunal` *(letters, numbers, hyphens, and underscores only; remember this exact title for the Google Form!)*
   * **ChineseName:** *(Leave empty so it falls back to the English Name)*
   * **Visibility:** Select **Public** *(CRITICAL: Judges must be able to open your link without logging in!)*
   * **License:** `Apache License 2.0`
   * **Description:** `Gamified Multi-Agent Policy & Rulebook Advisory Tribunal powered by ModelScope API-Inference.`
   * Click **Create**.
3. **Upload Your Project Files:**
   * On the Studio's **Contents / Files and versions** page, drag and drop your clean project files:
     * `app.py`
     * `requirements.txt`
     * `README.md`
     * `.gitignore`
   * Click the blue button **"Next step: Deployment setup"**.
4. **Configure Deployment Settings (CRITICAL):**
   * **Deployment Framework:** Select **Gradio**.
   * **Main Entry File:** Ensure it points to `app.py`.
   * **Resources:** Select **Free CPU (allocated on demand)**. *(Do NOT select GPU or xGPU—it is against the rules!)*
   * **Environment:** Select the recommended CPU Ubuntu / Python 3.10 environment.
   * **Secrets / Variables (PROTECT YOUR TOKEN HERE):**
     * Under **Secrets** (or Environment Variables), add a Secret named:
       * Key: `MODELSCOPE_API_KEY`
       * Value: `your_modelscope_token` *(paste your token from Step B here)*
   * Click **Save**, then click **Confirm and deploy**.
5. **Wait for Publishing (~5 to 10 Minutes):**
   * Click **View log** to watch the container build and launch.
   * Once the status badge turns to **Running**, open your public URL (`https://modelscope.ai/studios/<your-username>/AegisBoard-Policy-Tribunal`) in an Incognito browser window and run 1 full test deliberation to verify everything works publicly!

---

## 9. [Step 6] Final Submission Package & Report Template (STEP F — Wed, 4 Nov 2026, 16:00–23:59 WIB)

*(Compiled and submitted by Member 2 with Member 1's verification)*

While your Studio is deploying, prepare these exact items in a folder on your desktop so you can submit immediately when the admin posts the Google Form link in the WhatsApp group on **Wednesday, 4 November 2026 (16:00 – 23:59 WIB)**:

### 9.1 Required Google Form Fields & Attachments Checklist (STEP F)
1. **Team Info:** Full names, emails, university/school, and WhatsApp contact info for both team members.
2. **Work Title:** `AegisBoard-Policy-Tribunal` *(Must be 100% identical to your ModelScope Studio title!)*
3. **Studio Share Link:** `https://modelscope.ai/studios/<your-username>/AegisBoard-Policy-Tribunal`
4. **Your Coding Work (`.zip` archive):** Zip up `app.py`, `requirements.txt`, and `README.md` into `AegisBoard_Code.zip`. *(Double-check one last time that no API token is inside the zip!)*
5. **Key Prompts Used for Coding (2–3 Most Important Prompts):** Copy and paste **Master Prompt 1, Master Prompt 2, and Master Prompt 3** from Section 6 above.
6. **Screenshots of Your AI Coding Agent (WORTH 50% OF SCORE):**
   * Upload your screenshots of **OpenCode** taken by Member 1 and Member 2 during development.
   * Verify that every screenshot clearly shows:
     1. One of the 4 approved models (`DeepSeek V4 Pro`, `GLM-5.2`, `Step 3.5 Flash`, or `Qwen3.8 27B`) in the top-right corner of the UI.
     2. Your prompt and the iterative code generation rounds.
7. **Proof of Submission:** After clicking Submit on the Google Form, **take a screenshot of the Google Form confirmation screen** and save it!

---

### 9.2 Project Report & Finalist Presentation Outline (Copy-Paste Ready)
Use this structured text for your project report, README, and Finalist Pitch Deck (for the Top 5 Final Round):

#### 1. Background & Problem Statement
Organizations—ranging from university disciplinary boards and corporate security teams to e-commerce marketplace moderators—rely on dense policy rulebooks to evaluate incident reports. However, single-pass AI summaries or manual reviews suffer from two major flaws:
1. **Literal vs. Contextual Blind Spots:** A literal reading of a rulebook may demand harsh punishment for an honest procedural mistake, ignoring intent (*mens rea*), mitigating factors, or ethical proportionality.
2. **Opaque "Black-Box" Decisions:** Users cannot see *how* conflicting clauses were weighed or whether the rulebook itself contains poorly written loopholes.

#### 2. Our Solution: AegisBoard (Interactive Multi-Agent Advisory Tribunal)
**AegisBoard** transforms static policy enforcement into an interactive, gamified **4-Agent Compliance & Ethics Advisory Board** powered by Multi-Model Runtime Routing across all 4 approved ModelScope models:
* **Mandatory Dual-Gate Intake:** Blocks execution unless both the official policy document and a manual human narrative prompt are provided, ensuring deliberate, context-rich case submission.
* **4 Specialized AI Characters & Dedicated ModelScope Routing:**
  * **LEX-01 (Strict Rule-Checker — `Qwen/Qwen3.8-27B`):** Rapid literal clause extraction and citation matching.
  * **CTX-02 (Contextual & Intent Analyst — `stepfun-ai/Step-3.5-Flash`):** Low-latency analysis of intent vs. accident, mitigating circumstances, and rule ambiguity.
  * **ETH-03 (Ethics & Precedent Evaluator — `zai-org/GLM-5.2`):** Nuanced evaluation of proportionality, fairness, and organizational values.
  * **CHR-04 (Chief Board Chair — `deepseek-ai/DeepSeek-V4-Pro-0813`):** Moderates the debate, consults the human user with clarifying questions, and synthesizes a **Conclusive Final Verdict**, **Primary Recommended Action/Sanction**, and **Policy Vulnerability Patch** in strict JSON format.
* **Grounded Citations & Policy Vulnerability Detection:** Highlights cited policy clauses (`[Clause X.Y]`) in real time and automatically generates clause rewrite patches whenever an incident exposes a loophole in the organization's handbook.

#### 3. Visual Innovation: "Floating-Limb Chibi Astro-Bots" & Step-by-Step Cutscene Stage
To make complex multi-agent reasoning intuitive and engaging without brittle external asset packs:
* **Current Implementation (Phase 1 MVP):** A customizable 2D courtroom arena (*Classic Tribunal*, *Cyber War Room*, *Zen Boardroom*) with *Semicircle Tribunal* and *Adversarial Arena* seating layouts. The 4 agents are rendered as symmetric **Floating-Limb Chibi Bots** using pure geometric SVG primitives (`render_chibi_bot_svg`) and animated sequentially via a Python `yield` cutscene generator with state-driven kinesics (`idle`, `scanning`, `speaking`, `objecting`, `verdict`), comic speech clouds, and glowing dashed workflow beams.
* **Future Roadmap (Phase 2):** Because our underlying deliberation engine outputs structured agent kinesic states and interaction graphs, the 2D SVG viewport maps directly to our v2.0 Three.js/WebGL 3D Spatial Courtroom upgrade path.

#### 4. 2-Member Development Process & ModelScope AI Usage (1,000 Combined Magic Cubes/Day)
* **AI Coding Tool:** Built 100% via **OpenCode** connected to ModelScope API-Inference (`https://api-inference.modelscope.ai/v1`).
* **2-Member Quota & Model Strategy:**
  * **Member 1 (Lead Architect & Backend Logic):** Used `deepseek-ai/DeepSeek-V4-Pro-0813` (Prompt 1) to architect the multi-model backend, dual-gate validator, `yield` cutscene generator, and parameterized SVG bot renderer, followed by `zai-org/GLM-5.2` (Prompt 3) for fallback resilience and dark glassmorphism polish.
  * **Member 2 (UI/UX Stage Director, Demo Creator & Deployment Lead):** Used `zai-org/GLM-5.2` (Prompt 2) to refine CSS keyframe kinesics, courtroom themes/orientations, the 3 built-in Demo Scenarios, ModelScope Studio CPU deployment (STEP E), and final submission packaging (STEP F).
