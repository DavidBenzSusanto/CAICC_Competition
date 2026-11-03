# CAICC 2026 Track 2 — AI Usage & Evidence Collection Dossier
**Project Title:** AegisBoard — Gamified Multi-Agent Policy & Rulebook Advisory Tribunal  
**Competition:** Campus AI Co-Creation Competition (CAICC 2026) — Track 2: Prompt to App  
**Team Account:** davidbenzsus@gmail.com  
**Target Studio Work Title:** AegisBoard-Policy-Tribunal  
**Target Studio Share Link:** `https://modelscope.ai/studios/<username>/AegisBoard-Policy-Tribunal`  
**Submission Window:** Wednesday, 4 November 2026, 16:00 – 23:59 WIB  

---

## 1. Executive Summary & Scoring Alignment
According to the CAICC 2026 Participant Guidebook, **"ModelScope AI Usage" accounts for 50% of the total score**. This document compiles full-fidelity proof of:
1. Strict adherence to the 4 approved ModelScope models (`DeepSeek-V4-Pro-0813`, `GLM-5.2`, `Step-3.5-Flash`, `Qwen3.8-27B`).
2. Multi-turn AI-assisted code generation through **OpenCode** connected directly to `api-inference.modelscope.ai`.
3. Zero-human-code compliance (<30 human lines).
4. Evidence log of environment setup, prompts, outputs, and runtime verification.

---

## 2. Approved Model & Platform Verification
* **Coding Environment:** OpenCode CLI (v1.19.5) running in WSL Ubuntu targeting the project directory `/aegisboard-tribunal`.
* **Inference Endpoint:** `https://api-inference.modelscope.ai/v1`
* **Default Active Model:** `deepseek-ai/DeepSeek-V4-Pro-0813` (DeepSeek V4 Pro)
* **Approved Backup Models Configured:**
  * `zai-org/GLM-5.2` (GLM-5.2)
  * `stepfun-ai/Step-3.5-Flash` (Step 3.5 Flash)
  * `Qwen/Qwen3.8-27B` (Qwen3.8 27B)

---

## 3. Evidence Screenshot Log

### Screenshot Item 1: OpenCode Environment & ModelScope Model Binding
* **Description:** OpenCode terminal session running in `/aegisboard-tribunal` showing the active model `Build · DeepSeek V4 Pro ModelScope International` in the status footer, Master Prompt 1 input, and ModelScope account endpoint binding.
* **Local File:** `screenshots_for_submission/opencode_prompt1_environment.png`
* **Key Verification Points for Judges:**
  * Window Title: OpenCode
  * Active Model: `DeepSeek V4 Pro`
  * Provider: `ModelScope International`
  * Working Directory: `.../CAICC_Competition/aegisboard-tribunal`

### Screenshot Item 2: Master Prompt 1 Generation & Code Artifacts
* **Description:** OpenCode generating the core multi-agent system (`app.py`, `requirements.txt`, `.gitignore`).
* **Status:** Generated locally (`app.py` 44KB+ self-contained Gradio tribunal application).

### Screenshot Item 3: Master Prompt 2 (Visual Stage & Enhancements)
* **Description:** Execution of Master Prompt 2 for stage inspection, multi-model council options, and markdown dossier export.
* **Placeholder:** *To be captured during Prompt 2 execution.*

### Screenshot Item 4: Master Prompt 3 (Polish & Resilience)
* **Description:** Execution of Master Prompt 3 for robust error handling, JSON parsing safeguards, and CPU deployment verification.
* **Placeholder:** *To be captured during Prompt 3 execution.*

### Screenshot Item 5: Local Gradio Tribunal UI Test
* **Description:** Full-screen browser screenshot of `http://127.0.0.1:7860` showing the 3-column UI:
  * Left: Policy/Rulebook upload and manual case explanation intake.
  * Center: Animated 2D Astro-Bot council stage (LEX-01, CTX-02, ETH-03, CHR-04) with real-time speech clouds.
  * Right: Conclusive final verdict badge, confidence score, primary action, and loophole alerts.
* **Placeholder:** *To be captured during `python app.py` local verification.*

### Screenshot Item 6: ModelScope Studio Public Deployment & Verification
* **Description:** ModelScope Studio deployment page showing:
  * Public visibility status
  * Free CPU configuration (no GPU/xGPU)
  * Secrets configuration (`MODELSCOPE_API_KEY`)
  * Live running app preview on `https://modelscope.ai/studios/...`
* **Placeholder:** *To be captured upon Studio publishing.*

---

## 4. Key Prompts Submitted to OpenCode

### Prompt 1: Core Multi-Agent Architecture & Intake Gate
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
```

### Prompt 2: Interactive Playback & Model Matrix
```text
Enhance `app.py` with the following high-impact interactive UX features while strictly preserving the 4 approved ModelScope models (`deepseek-ai/DeepSeek-V4-Pro-0813`, `zai-org/GLM-5.2`, `Qwen/Qwen3.8-27B`, `stepfun-ai/Step-3.5-Flash`) and environment-variable token security:
1. STEP-BY-STEP DEBATE STAGE INSPECTOR & KINESICS STATES
2. MULTI-MODEL COUNCIL OPTION
3. EXPORTABLE OFFICIAL CASE DOSSIER & README
```

### Prompt 3: Quality Pass, JSON Guardrails & Studio Startup
```text
Perform a comprehensive quality, resilience, and UI polish pass on `app.py` and `requirements.txt`:
1. Robust JSON Parsing & Fallback
2. Clear Loading & Status Feedback
3. Verify ModelScope Studio Compatibility (`demo.launch()` without hardcoded local ports)
```

---

## 5. Submission Checklist (Google Form)
- [ ] Team Info: Names, emails, institution, WhatsApp contact
- [ ] Work Title: `AegisBoard-Policy-Tribunal` (exact match)
- [ ] Public Studio Link: `https://modelscope.ai/studios/<username>/AegisBoard-Policy-Tribunal`
- [ ] Code ZIP: `AegisBoard_Code.zip` (`app.py`, `requirements.txt`, `README.md`)
- [ ] Key Prompts pasted into form
- [ ] Evidence Screenshots uploaded
- [ ] Final Confirmation Screen Screenshot captured
