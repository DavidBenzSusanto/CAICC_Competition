# CAICC 2026 Track 2 — Master Build & Vibecoding Playbook
**Project Title:** AegisBoard — Gamified Multi-Agent Policy & Rulebook Advisory Tribunal  
**Competition:** Campus AI Co-Creation Competition (CAICC 2026) — Track 2: Prompt to App  
**Submission Window:** Wednesday, 4 November 2026, 16:00 – 23:59 WIB (via WhatsApp Group Google Form)

---

> ### Document Partition Map
> * **PART I — Initial Rules, General Shape & 2-Member Team Plan (Sections 1–3):** Competition guardrails, finalized application architecture/UI blueprint, and the 2-member workload split & schedule.
> * **PART II — Step-by-Step Execution Guide from First to Last Step (Sections 4–9):** Chronological walkthrough from initial account/environment setup, project initialization, and the 3 Master Vibecoding Prompts to local testing, ModelScope Studio deployment, and final submission.

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
   * The **approved model name** (e.g., `DeepSeek V4 Pro` or `GLM-5.2`) in the top right/status bar.
   * Your prompt and the AI's multi-round code generation/refinement.
6. **Magic Cubes Quota Management:** Every account receives **500 Magic Cubes per day** (350 daily login + 150 bonus) which expire at midnight each day. Because we have pre-engineered the exact prompts in this file, you will only need **3–4 prompting rounds total** to build the entire app.

---

## 2. Finalized Application Blueprint (UI/UX & Architecture Lock-In)

### 2.1 Core Purpose & Decisive Output
**AegisBoard** is an interactive **Compliance & Ethics Advisory Board** where organizations upload their official policy/rulebook and consult a 4-agent AI tribunal on incident reports.
* Unlike passive RAG tools, AegisBoard runs a structured adversarial & analytical debate and locks in a **Conclusive Final Suggestion**:
  1. **Definitive Verdict Badge:** (`SUBSTANTIATED VIOLATION`, `PROCEDURAL BREACH ONLY`, or `UNSUBSTANTIATED / CLEARED`) + Consensus Confidence Score (%).
  2. **Primary Conclusive Action / Sanction:** One decisive, actionable punishment or remediation step grounded directly in the rulebook's penalty schedule.
  3. **Policy Vulnerability & Loophole Alert:** Highlights ambiguous clauses in the organization's rulebook that caused debate and suggests exact rewrites.

### 2.2 The 4 Debating AI Characters (Mandatory Roles)
1. ** Bot 1 — Strict Rule-Checker ("LEX-01" / Prosecutor):** Crimson visor. Evaluates literal compliance, matching incident facts strictly against clauses and penalty tables.
2. ** Bot 2 — Contextual / Intent Analyst ("CTX-02" / Defense & Nuance):** Teal visor. Evaluates *mens rea* (intent vs. honest mistake), mitigating circumstances, situational pressure, and rulebook ambiguity.
3. ** Bot 3 — Ethics & Precedent Evaluator ("ETH-03" / Fairness Officer):** Amber visor. Evaluates proportionality, organizational core values, spirit of the policy, and precedent fairness.
4. ** Bot 4 — Chief Board Chair ("CHR-04" / Synthesizer):** Gold/Royal visor. Moderates the debate, asks the human user clarifying "Missing Fact" questions, weighs inputs from the Contextual/Intent Analyst and Ethics/Precedent Evaluator against the Rule-Checker, and locks in the **Conclusive Final Verdict & Action**.

### 2.3 Mandatory Dual-Requirement Case Intake
* The **"Convene Advisory Board"** button is **strictly locked/disabled** unless the user provides **BOTH**:
  1. **Rulebook / Context Document:** Uploaded via file picker (`.pdf`, `.txt`, `.md`) or loaded via a built-in preset selector (for judges testing quickly).
  2. **Manual Case Explanation Prompt:** A written narrative in the prompt box explaining what happened, who was involved, and the context of the case (minimum 20 characters).

### 2.4 3-Column Gamified Interface (Phase 1 MVP + Phase 2 Roadmap Preview)
Built as a single self-contained **Gradio (`gr.Blocks`)** web app with custom CSS/HTML/SVG injection:
* **Left Column — Grounded Rulebook & Case Intake:**
  * File Upload + Preset Case Loader (for instant judge testing).
  * Mandatory Narrative Prompt Textbox + Validation Gate Banner.
  * **Grounded Policy Viewer:** Scrollable document viewer that automatically highlights cited clauses (e.g., `Section 4.2`) in glowing yellow/amber when the bots reference them.
* **Center Column — The 2D Astro-Bot Style Council Stage:**
  * **Courtroom Theme Customizer:** Dropdown to switch the live stage visuals between *Cyber Tribunal*, *Classic High Courtroom*, and *Zen Executive Boardroom*, plus Seating Layout toggle (*Semicircle Tribunal* vs. *Roundtable*).
  * **Animated 2D Cute Robot Characters (Astro Bot-inspired SVG Sprites):** Four glossy white-and-neon robot characters with CSS keyframe kinesics (`idle-bob`, `visor-scan`, `objection-jump`, `speaking-pulse`).
  * **Real-Time Speech Clouds & Workflow Lines:** Dynamic comic speech bubbles appear above each bot showing their live argument, connected by animated SVG workflow beams showing who is countering or synthesizing whom.
  * **Interactive Board Consultation Bar:** Below the stage, the Board Chair poses 2 clarifying questions to the human user. The user can type additional facts or answers to trigger a **Follow-up Re-Deliberation**.
  * **Phase 2 (3D Spatial Arena) Blueprint Tab:** A toggleable preview badge showing how the exact state machine (`scanning`, `objecting`, `synthesizing`, `verdict_locked`) maps to the future Three.js 3D Astro Bot update.
* **Right Column — The Conclusive Verdict & Action Dossier:**
  * **Conclusive Verdict Card:** High-impact badge with confidence meter.
  * **Primary Recommended Action / Sanction Box:** Clear, decisive enforcement action.
  * **Role Fulfillment Breakdown:** Dedicated cards showing how the *Strict Rule-Checker*, *Contextual/Intent Analyst*, and *Ethics/Precedent Evaluator* shaped the decision.
  * **Policy Vulnerability Patch:** Specific clause rewrite recommendation + Export Case Brief (`.md`) button.

---

## 3. Team Workload Split (2 Members) & Timeline (Nov 2 – Nov 4, 2026)

As a 2-person team, divide responsibilities 50/50 as follows so no one steps on each other's toes and you pool your daily 500 Magic Cubes effectively:

| Role | Responsibility | Key Deliverables |
| :--- | :--- | :--- |
| **Member 1: Lead Vibecoder, Architect & Submission Packager (You)** | Setup Alibaba Cloud + OpenCode, run the 3 Master Prompts in OpenCode, test locally, deploy to ModelScope Studio, and compile key prompt logs, screenshot evidence pack, and code archive. | `app.py`, `requirements.txt`, `README.md`, live ModelScope Studio URL, **OpenCode Screenshots** showing the approved model name, Screenshot Proof Folder, and Submission ZIP archive. |
| **Member 2: Policy Dataset, QA Engineer & Documentation/Report Lead** | Create 3 realistic test cases (Rulebook `.txt`/`.pdf` + Incident Narratives), test every button/edge case on local & deployed Studio, and compile the final project report and presentation deck (for top 5 finalists). | `sample_policies.py` (embedded via Prompt 2), bug reports for Prompt 3, verification that token secrets work cleanly, Final Project Report, and Final Pitch Deck. |

### Master Schedule
* **Monday Night (2 Nov):** Complete Steps A, B, and C (Account Binding + OpenCode Config). Run **Master Prompt 1** in OpenCode before midnight WIB to use Monday's 500 Magic Cubes!
* **Tuesday (3 Nov):** Run **Master Prompt 2** (Visual Stage + Sample Presets + Grounded Highlighting) and **Master Prompt 3** (UI Polish + Edge-Case Hardening). Deploy initial build to ModelScope Studio.
* **Wednesday Morning (4 Nov, 09:00 – 15:00 WIB):** Final QA test on the public ModelScope Studio link, package the `.zip` archive, verify all OpenCode screenshots, and finalize the report.
* **Wednesday Afternoon (4 Nov, 16:00 – 20:00 WIB):** Submit early via the WhatsApp Group Google Form (window closes strictly at **23:59 WIB**). Screenshot the submission confirmation page!

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

#### Option 1: OpenCode (Recommended — Shows Model Name Clearly in UI for Screenshots)
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
6. Tip: Inside OpenCode, you can type `/models` at any time to switch between `DeepSeek V4 Pro`, `GLM-5.2`, `Step 3.5 Flash`, and `Qwen3.8 27B`.

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
4. **Connectivity Check:** Type `"Verify connectivity by listing files in the current directory"` and take your first screenshot showing the approved model name in the corner!

---

## 6. [Step 3] The 3 Master Vibecoding Prompts (Copy-Paste into OpenCode)

> **CRITICAL REMINDER:** Copy and paste these prompts one at a time into OpenCode. After each prompt finishes generating the files, **TAKE A SCREENSHOT** of the OpenCode window (showing both your prompt and the approved model name in the corner) and save it to a separate `screenshots_for_submission` folder outside your project directory! Also save these 3 prompts for the Google Form submission.

---

###  MASTER PROMPT 1: Core Multi-Agent Architecture, Dual-Gate Intake & 2D Astro-Bot Stage
*(Paste this into OpenCode first. It builds the complete working `app.py` and `requirements.txt`.)*

```text
Build a complete, production-ready Python Gradio web application in `app.py` and generate `requirements.txt` (plus `.gitignore`) for a project called "AegisBoard: Multi-Agent Policy & Rulebook Advisory Tribunal".

STRICT COMPETITION CONSTRAINTS (MUST FOLLOW):
1. All AI inference calls inside `app.py` MUST use the OpenAI-compatible client (`openai` Python SDK) pointing strictly to `base_url="https://api-inference.modelscope.ai/v1"`.
2. NEVER hardcode any API key or token in the source code. Read the API key strictly from environment variables (`os.getenv("MODELSCOPE_API_KEY") or os.getenv("MODELSCOPE_SDK_TOKEN")`), with an optional password-masked fallback textbox in a collapsible top settings bar ONLY if the environment variable is not set.
3. The user must be able to choose ONLY from these 4 approved ModelScope models in a dropdown:
   - `deepseek-ai/DeepSeek-V4-Pro-0813` (default)
   - `zai-org/GLM-5.2`
   - `Qwen/Qwen3.8-27B`
   - `stepfun-ai/Step-3.5-Flash`
4. Do NOT use any other models or external paid APIs. Ensure it runs smoothly on CPU-only environments.

APPLICATION ARCHITECTURE & WORKFLOW:
1. MANDATORY DUAL-REQUIREMENT CASE INTAKE:
   - Users must provide BOTH:
     (a) Organization Policy/Rulebook & Context Report: via file upload (supporting `.txt`, `.md`, `.pdf` using `pypdf`) OR by loading one of 3 rich built-in preset scenarios (Corporate Data Privacy Breach, University Academic Integrity AI Usage, E-Commerce Seller Policy Violation).
     (b) Mandatory Manual Case Explanation Prompt: A narrative textbox where the user manually explains what happened, who was involved, and the dilemma.
   - Validation Gate: If EITHER the Policy/Rulebook text OR the Manual Case Explanation (minimum 20 characters) is missing, block deliberation and display a clear warning banner instructing the user to provide both inputs.

2. THE 4 DEBATING AI CHARACTERS (MANDATORY ROLES):
   Implement a multi-agent deliberation workflow where 4 distinct AI personas analyze the policy and the case narrative:
   - Bot 1: "LEX-01: Strict Rule-Checker" (Prosecutor role — literal clause matching, violations, and strict penalty lookup).
   - Bot 2: "CTX-02: Contextual & Intent Analyst" (Defense/Nuance role — evaluates intent vs. accident, mitigating factors, situational pressures, and policy ambiguity).
   - Bot 3: "ETH-03: Ethics & Precedent Evaluator" (Fairness role — evaluates proportionality, organizational ethics, spirit vs. letter of the rule, and precedent consistency).
   - Bot 4: "CHR-04: Chief Board Chair" (Synthesizer role — moderates the debate, explicitly weighs the Contextual/Intent Analyst and Ethics/Precedent Evaluator arguments against the Strict Rule-Checker, poses 2 clarifying questions to the human user, and locks in the CONCLUSIVE FINAL VERDICT & PRIMARY RECOMMENDED ACTION).
   - To optimize speed and API quota while remaining 100% genuine, execute a structured multi-turn or JSON-structured LLM call that returns each bot's speech bubble, exact cited clause quotes from the uploaded rulebook, stance score, inter-bot agreement/objection target, clarifying questions for the user, and the final conclusive verdict package.

3. 3-COLUMN GAMIFIED UI/UX LAYOUT (`gr.Blocks` with custom CSS):
   - LEFT COLUMN (Rulebook & Intake Locker):
     * Preset Scenario Loader dropdown + File Upload (`.pdf`, `.txt`, `.md`) + editable/viewable Rulebook Textbox.
     * Mandatory Manual Case Narrative Prompt Textbox.
     * "Convene Advisory Board" primary button.
     * Grounded Policy Viewer (HTML panel) that displays the rulebook and highlights exact clauses or quotes cited by the bots in glowing yellow/amber.
   - CENTER COLUMN (The Gamified 2D Astro-Bot Style Council Stage):
     * Courtroom Customizer Controls: Dropdowns to switch Room Theme ("Cyber Tribunal", "Classic High Court", "Zen Boardroom") and Seating Orientation ("Semicircle Tribunal", "Adversarial Arena", "Roundtable Council").
     * Custom HTML/SVG/CSS Animated Stage rendering 4 cute, glossy white-and-neon robot characters inspired by Astro Bot (with expressive glowing visor eyes, floating antenna, and CSS keyframe animations for idle bobbing, visor scanning, leaning forward, and objection bounce).
     * Real-Time Speech Clouds & Workflow Lines: Above each bot, render dynamic comic-style speech bubbles displaying their live argument and cited clause, plus animated SVG connecting beams showing workflow interactions between bots.
     * Interactive Consultation Bar below the stage: Displays the Board Chair's clarifying questions to the user, a textbox for the user to reply or add new facts ("Submit Follow-Up Context to Board"), and a button that re-runs/updates the tribunal verdict based on the user's answer.
   - RIGHT COLUMN (Conclusive Final Verdict & Action Dossier):
     * Conclusive Final Verdict Banner: Unambiguous verdict classification ("SUBSTANTIATED VIOLATION", "PROCEDURAL BREACH ONLY", or "UNSUBSTANTIATED / CLEARED"), Consensus Confidence %, and Severity Tier.
     * Conclusive Primary Action / Sanction Card: One specific, decisive punishment and remediation plan mandated by the rulebook.
     * Role Fulfillment Matrix: Expandable/structured breakdown of Strict Rule-Checker vs. Contextual/Intent Analyst vs. Ethics/Precedent Evaluator conclusions.
     * Policy Vulnerability & Loophole Alert: Identifies fuzzy or poorly written rules exposed by the debate and provides an exact suggested rewrite.

Ensure `requirements.txt` contains clean, standard packages (`gradio`, `openai`, `pypdf`) so it deploys without build errors on ModelScope Studio CPU.
```

---

###  MASTER PROMPT 2: Interactive Playback, Phase 2 3D Preview & Markdown Export
*(After testing `python app.py` from Prompt 1, run this second prompt in OpenCode to add step-by-step debate playback, downloadable reports, and the Phase 2 3D Roadmap showcase. Take Screenshot #2!)*

```text
Enhance `app.py` with the following high-impact interactive UX features while strictly preserving the 4 approved ModelScope models (`deepseek-ai/DeepSeek-V4-Pro-0813`, `zai-org/GLM-5.2`, `Qwen/Qwen3.8-27B`, `stepfun-ai/Step-3.5-Flash`) and environment-variable token security:

1. STEP-BY-STEP DEBATE STAGE INSPECTOR & KINESICS STATES:
   - Add a radio/segmented control above or below the 2D Astro-Bot Council Stage allowing the user to focus on specific stages of the workflow ("All Bots Overview", "1. LEX-01 Rule Check", "2. CTX-02 Intent Analysis", "3. ETH-03 Ethics & Precedent", "4. CHR-04 Final Synthesis").
   - When a stage is selected or when deliberation completes, dynamically update the SVG bots' kinesic animation states (`scanning`, `speaking`, `objecting`, `verdict_locked`) and highlight the active workflow beam on the courtroom canvas.

2. MULTI-MODEL COUNCIL OPTION:
   - Allow an optional "Assign Different Approved Models per Bot" mode where LEX-01, CTX-02, ETH-03, and CHR-04 can either all use the selected primary model OR distribute reasoning across the 4 approved ModelScope models (`zai-org/GLM-5.2`, `deepseek-ai/DeepSeek-V4-Pro-0813`, `stepfun-ai/Step-3.5-Flash`, `Qwen/Qwen3.8-27B`), displaying the active model badge underneath each robot avatar on the stage.

3. EXPORTABLE OFFICIAL CASE DOSSIER & README:
   - Add a "Download Official Advisory Dossier (.md)" button in the Right Column that generates a formatted Markdown compliance report containing the case summary, each bot's argument, cited policy clauses, user consultation Q&A, the Conclusive Verdict, the Primary Sanction, and the Policy Loophole Rewrite.
   - Generate a comprehensive `README.md` documenting the project architecture, the 4 approved ModelScope models used, setup instructions, and how to run locally and on ModelScope Studio.
```

---

###  MASTER PROMPT 3: Final Polish, Error Handling & Studio Readiness
*(Run this third prompt in OpenCode to guarantee zero crashes during live judging. Take Screenshot #3!)*

```text
Perform a comprehensive quality, resilience, and UI polish pass on `app.py` and `requirements.txt`:
1. Robust JSON Parsing & Fallback: If an LLM response contains markdown code fences around JSON or slightly malformed formatting, strip fences and parse safely with regex/fallback extraction so the UI never crashes or throws an unhandled exception during live judging.
2. Clear Loading & Status Feedback: Ensure that clicking "Convene Advisory Board" or "Submit Follow-Up Context" immediately updates the Center Stage to a "Council in Session — Scanning Policy & Deliberating..." animated state before rendering the final speech clouds and verdict.
3. Verify ModelScope Studio Compatibility: Ensure `app.py` launches cleanly with `demo.launch()` at the bottom without hardcoded ports or local-only paths that would block ModelScope Studio container startup.
```

---

## 7. [Step 4] Local Testing Checklist (Before Publishing)

Run your app locally in your terminal:
```bash
pip install -r requirements.txt
python app.py
```
Open the local URL shown in the terminal (typically `http://127.0.0.1:7860`) and verify:
- [ ] **Gate Check:** Try clicking "Convene Advisory Board" with an empty manual explanation box $\rightarrow$ Confirm it blocks execution and asks for both the policy and manual explanation.
- [ ] **Preset Check:** Load a preset policy + narrative and click "Convene Advisory Board" $\rightarrow$ Confirm all 4 cute 2D robot avatars display their speech clouds, cited clauses highlight in the left panel, and the Right Panel locks in a **Conclusive Verdict** and **Primary Action**.
- [ ] **Room Customization Check:** Switch the courtroom theme (*Cyber Tribunal*, *Classic High Court*, *Zen Boardroom*) and seating layout $\rightarrow$ Confirm the 2D stage updates visually.
- [ ] **Interactive Consultation Check:** Type an answer to the Board Chair's clarifying question in the bottom consultation bar and click "Submit Follow-Up Context" $\rightarrow$ Confirm the board updates its deliberation and verdict.
- [ ] **Security Check:** Run `grep -rn "ms-" .` or search `app.py` to be 100% sure your personal ModelScope access token is **NOT** written inside any file.

---

## 8. [Step 5] Step-by-Step ModelScope Studio Deployment (STEP E from Guidebook)

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

While your Studio is deploying, prepare these exact items in a folder on your desktop so you can submit immediately when the admin posts the Google Form link in the WhatsApp group on **Wednesday, 4 November 2026 (16:00 – 23:59 WIB)**:

### 9.1 Required Google Form Fields & Attachments Checklist
1. **Team Info:** Full names, emails, university/school, and WhatsApp contact info for all team members.
2. **Work Title:** `AegisBoard-Policy-Tribunal` *(Must be 100% identical to your ModelScope Studio title!)*
3. **Studio Share Link:** `https://modelscope.ai/studios/<your-username>/AegisBoard-Policy-Tribunal`
4. **Your Coding Work (`.zip` archive):** Zip up `app.py`, `requirements.txt`, and `README.md` into `AegisBoard_Code.zip`. *(Double-check one last time that no API token is inside the zip!)*
5. **Key Prompts Used for Coding (2–3 Most Important Prompts):** Copy and paste **Master Prompt 1, Master Prompt 2, and Master Prompt 3** from Section 6 above.
6. **Screenshots of Your AI Coding Agent (WORTH 50% OF SCORE):**
   * Upload your screenshots of **OpenCode** taken during development.
   * Verify that every screenshot clearly shows:
     1. One of the 4 approved models (`DeepSeek V4 Pro`, `GLM-5.2`, `Step 3.5 Flash`, or `Qwen3.8 27B`) in the UI.
     2. Your prompt and the iterative code generation rounds.
7. **Proof of Submission:** After clicking Submit on the Google Form, **take a screenshot of the Google Form confirmation screen** and save it!

---

### 9.2 Project Report & Finalist Presentation Outline (Copy-Paste Ready)
Use this structured text for your project report, README, and Finalist Pitch Deck (for the Top 5 Final Round):

#### 1. Background & Problem Statement
Organizations—ranging from university disciplinary boards and corporate HR teams to digital marketplace moderators—rely on dense policy rulebooks to evaluate incident reports. However, single-pass AI summaries or manual reviews suffer from two major flaws:
1. **Literal vs. Contextual Blind Spots:** A literal reading of a rulebook may demand harsh punishment for an honest procedural mistake, ignoring intent (*mens rea*), mitigating factors, or ethical proportionality.
2. **Opaque "Black-Box" Decisions:** Users cannot see *how* conflicting clauses were weighed or whether the rulebook itself contains poorly written loopholes.

#### 2. Our Solution: AegisBoard (Interactive Multi-Agent Advisory Tribunal)
**AegisBoard** transforms static policy enforcement into an interactive, gamified **4-Agent Compliance & Ethics Advisory Board**:
* **Mandatory Dual-Gate Intake:** Requires both the official policy document and a manual human narrative prompt to ensure deliberate, context-rich case submission.
* **4 Specialized AI Characters:**
  * **LEX-01 (Strict Rule-Checker):** Literal compliance and clause matching.
  * **CTX-02 (Contextual & Intent Analyst):** Evaluates intent, mitigating circumstances, and rule ambiguity.
  * **ETH-03 (Ethics & Precedent Evaluator):** Evaluates proportionality, fairness, and organizational values.
  * **CHR-04 (Chief Board Chair):** Moderates the debate, consults the human user with clarifying questions, and synthesizes a **Conclusive Final Verdict** and **One Primary Recommended Action**.
* **Grounded Citations & Policy Vulnerability Detection:** Highlights cited policy clauses in real time and automatically generates rewrite patches whenever an incident exposes a vague rule in the organization's handbook.

#### 3. Visual Innovation: Phase 1 (2D Expressive Stage) to Phase 2 (3D Spatial Courtroom)
To make complex multi-agent reasoning intuitive and engaging:
* **Current Implementation (Phase 1 MVP):** A customizable 2D courtroom arena (*Cyber Tribunal*, *Classic High Court*, *Zen Boardroom*) featuring cute, Astro Bot-inspired animated robot sprites with state-driven kinesics (`scanning`, `speaking`, `objecting`, `verdict_locked`), real-time comic speech clouds, and animated workflow beams.
* **Future Roadmap (Phase 2):** Because our underlying deliberation engine outputs structured agent kinesic states and interaction graphs, the 2D SVG viewport can be seamlessly swapped for a full 3D Three.js customizable courtroom with skeletal 3D bot animations.

#### 4. Development Process & ModelScope AI Usage
* **AI Coding Tool:** Built using **OpenCode** connected to ModelScope API-Inference (`https://api-inference.modelscope.ai/v1`).
* **Approved Models Utilized:** `deepseek-ai/DeepSeek-V4-Pro-0813`, `zai-org/GLM-5.2`, `Qwen/Qwen3.8-27B`, and `stepfun-ai/Step-3.5-Flash`.
* **Iterative Vibecoding Workflow:**
  * *Round 1:* Architected the core 4-agent deliberation pipeline, dual-requirement intake gate, grounded clause highlighter, and 2D SVG courtroom stage.
  * *Round 2:* Added step-by-step stage inspection, multi-model per-bot assignment across the 4 approved models, and official Markdown dossier export.
  * *Round 3:* Hardened JSON parsing resilience, loading animations, and ModelScope Studio CPU container deployment settings.
