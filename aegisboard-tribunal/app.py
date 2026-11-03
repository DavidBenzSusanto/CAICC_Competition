"""
AegisBoard: Multi-Agent Policy & Rulebook Advisory Tribunal
============================================================

A production-ready Gradio web application that convenes a 4-agent AI tribunal
(LEX-01, CTX-02, ETH-03, CHR-04) to deliberate on an organization's policy
rulebook against a manually narrated case.

All inference runs on the ModelScope OpenAI-compatible endpoint with FOUR
approved models routed per-persona by default (with automatic fallback), and a
pure SVG/CSS "floating-limb chibi astro-bot" stage. No API key is ever
hard-coded.
"""

import html
import json
import os
import re
import tempfile

import gradio as gr
from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration & constants
# ---------------------------------------------------------------------------

INFERENCE_BASE_URL = "https://api-inference.modelscope.ai/v1"

# The four approved ModelScope models (the only IDs ever offered to the UI).
MODELS = [
    "deepseek-ai/DeepSeek-V4-Pro-0813",
    "zai-org/GLM-5.2",
    "Qwen/Qwen3.8-27B",
    "stepfun-ai/Step-3.5-Flash",
]

MODEL_SHORT = {
    "deepseek-ai/DeepSeek-V4-Pro-0813": "DeepSeek-V4-Pro",
    "zai-org/GLM-5.2": "GLM-5.2",
    "Qwen/Qwen3.8-27B": "Qwen3.8-27B",
    "stepfun-ai/Step-3.5-Flash": "Step-3.5-Flash",
}

# Fallback pool used when a primary route times out / rate-limits.
FALLBACK_MODELS = ["zai-org/GLM-5.2", "Qwen/Qwen3.8-27B"]

# Role IDs define the guest personas and their model + color + title binding.
ORDER = ["prosecutor", "defense", "ethics", "chair"]

BOT_NAMES = {
    "prosecutor": "LEX-01",
    "defense": "CTX-02",
    "ethics": "ETH-03",
    "chair": "CHR-04",
}

BOT_TITLES = {
    "prosecutor": "Strict Rule-Checker",
    "defense": "Contextual & Intent Analyst",
    "ethics": "Ethics & Precedent Evaluator",
    "chair": "Board Chair / Chief Synthesizer",
}

BOT_ACCENTS = {
    "prosecutor": "#ef4444",  # crimson
    "defense": "#14b8a6",     # teal
    "ethics": "#f59e0b",      # amber
    "chair": "#eab308",       # gold
}

# Active 4-model runtime routing (default behavior).
ROLE_MODELS = {
    "prosecutor": "Qwen/Qwen3.8-27B",
    "defense": "stepfun-ai/Step-3.5-Flash",
    "ethics": "zai-org/GLM-5.2",
    "chair": "deepseek-ai/DeepSeek-V4-Pro-0813",
}

NAME_TO_ROLE = {v: k for k, v in BOT_NAMES.items()}
ACCENTS_BY_NAME = {BOT_NAMES[k]: v for k, v in BOT_ACCENTS.items()}
TITLES_BY_NAME = {BOT_NAMES[k]: v for k, v in BOT_TITLES.items()}

THEMES = ["Classic Tribunal", "Cyber War Room", "Zen Boardroom"]
ORIENTATIONS = ["Semicircle Tribunal", "Adversarial Arena"]

THEME_KEYS = {
    "Classic Tribunal": "classic",
    "Cyber War Room": "cyber",
    "Zen Boardroom": "zen",
}
ORIENTATION_KEYS = {
    "Semicircle Tribunal": "semicircle",
    "Adversarial Arena": "arena",
}

# Percent positions (x, y) for each role on the stage area.
STAGE_POSITIONS = {
    "Semicircle Tribunal": {
        "prosecutor": (14, 58),
        "defense": (38, 26),
        "ethics": (62, 26),
        "chair": (86, 58),
    },
    "Adversarial Arena": {
        "prosecutor": (14, 45),
        "defense": (86, 45),
        "ethics": (50, 26),
        "chair": (50, 70),
    },
}

VERDICT_CLASSES = [
    "SUBSTANTIATED VIOLATION",
    "PROCEDURAL BREACH ONLY",
    "UNSUBSTANTIATED / CLEARED",
]

# ---------------------------------------------------------------------------
# Preset scenarios
# ---------------------------------------------------------------------------

PRESETS = {
    "Corporate Data Security": {
        "rulebook": """SECTION A — DATA PROTECTION & PRIVACY

A.1  Purpose
     All employees must protect the confidentiality, integrity and availability
     of customer and company data, and may only access data necessary to perform
     their assigned job duties.

A.2  Access Control
     A.2.1  Employees may access customer records exclusively through approved
            corporate systems. Off-system storage of customer data (including
            personal email, USB drives, or unapproved cloud drives) is forbidden.
     A.2.2  Sharing account credentials or allowing another person to use one's
            access is a violation of this policy.

B — CLASSIFICATION & HANDLING

B.1  "Sensitive Data" means non-public personal information (NPI), financial
     data, health data, and any data governed by law or contract.
B.2  Sensitive Data may be transmitted externally only through the approved
     encrypted channels and only to authorized recipients.

C — BREACH RESPONSE

C.1  Any suspected loss, exposure, or unauthorized access to Sensitive Data
     ("a Data Incident") must be reported to the Data Protection Officer within
     24 hours of discovery.
C.2  Failure to report a known Data Incident shall be treated as gross
     misconduct and shall result in disciplinary action up to and including
     termination.

D — DISCIPLINARY FRAMEWORK

D.1  Minor negligence:     written warning.
D.2  Failure to report:    final written warning, at minimum.
D.3  Deliberate exfiltration of Sensitive Data:  termination and referral to
     legal counsel for potential civil/criminal action.
""",
        "case": """A marketing analyst, Priya, downloaded a customer contact list to
her personal cloud drive to finish a drip-campaign deadline over the weekend.
She did not realize the list contained full payment token IDs. On Monday she
discovered the personal drive had been shared with an external contractor by
mistake. Priya deleted the file and did not tell anyone, hoping nothing leaked.
Two weeks later the vendor flagged unusual access. Priya claims she acted from a
place of loyalty and deadline pressure, never intended harm, and instantly
remedied the error herself.""",
    },
    "Campus Academic Integrity": {
        "rulebook": """SECTION 2 — ACADEMIC INTEGRITY

2.1  All submitted work must be the student's own. Submission of work generated
     wholly or substantially by another person or by automated/artificial means,
     without authorization, constitutes an academic misconduct offence.

2.2  USE OF ARTIFICIAL INTELLIGENCE TOOLS
     2.2.1  AI tools may be used for ideation, summarization and editing only
            where the instructor has explicitly authorized their use.
     2.2.2  Any use of an AI tool must be disclosed ("Declaration of AI Use")
            describing the nature and extent of the assistance.
     2.2.3  Undisclosed use of AI to produce substantive assessed content is a
            Level 2 offence.

2.3  PERMITTED ASSISTANCE
     Collaboration, tutoring, and editorial advice on structure are permitted
     provided they do not produce the substantive content of the assessment.

SECTION 4 — PENALTIES

4.1  Level 1 offence (minor, neglectful):  mark reduction on the component.
4.2  Level 2 offence (substantive, undisclosed AI generation):  zero on the
     module, recorded on the student's internal record.
4.3  Level 3 offence (repeat / orchestrated deception):  suspension or
     expulsion proceedings.
""",
        "case": """A second-year student, Marcus, used a large language model to draft
an entire 3,000-word essay then edited it heavily for tone. His course syllabus
said "AI tools may be used for brainstorming and proofreading." Marcus did not
submit the required declaration because he believed his heavy editing made the
work his own. He argues the syllabus wording was vague, he understood the tool
as permitted, and that he never intended to cheat. The marker flagged the essay
via detection software.""",
    },
    "E-Commerce Seller Policy": {
        "rulebook": """POLICY 7 — MARKETPLACE PROHIBITED CONDUCT

7.1  PROHIBITED ACTIVITIES
     Sellers must not engage in any of the following:
     7.1.1  Listing counterfeit, infringing or otherwise unlawful products.
     7.1.2  Manipulating search results, reviews, or ratings.
     7.1.3  Coordinating with other sellers to fix prices or suppress
            competition.
     7.1.4  "Review abuse": soliciting, incentivizing or purchasing reviews,
            or posting reviews on one's own products.

7.2  SUSPENSION
     A seller account may be suspended immediately for any verified violation
     of Section 7.1. Repeat violations result in permanent delisting.

7.3  APPEAL
     Sellers may appeal a suspension by providing evidence that the conduct
     did not occur, or that mitigating circumstances justify a reduced remedy.
""",
        "case": """A small home-goods seller, "CozyNest", emailed 200 past customers a
10% coupon in exchange for an honest review. The seller genuinely believed
"honest review" language kept them within the rules, since they encouraged
customers to leave any rating. A competitor complained, and the seller was
summarily suspended. CozyNest argues the policy is ambiguous about incentivized
(yet honest) reviews, that no fake reviews were produced, and that a flat
suspension harms a sole proprietor disproportionate to the harm caused.""",
    },
}

PRESET_CHOICES = ["— Load a preset scenario —"] + list(PRESETS.keys())


# ---------------------------------------------------------------------------
# LLM helper — OpenAI-compatible client
# ---------------------------------------------------------------------------

def resolve_api_key(ui_key: str) -> str:
    """Return the API key from env vars, falling back to the UI password box."""
    env_key = os.getenv("MODELSCOPE_API_KEY") or os.getenv("MODELSCOPE_SDK_TOKEN")
    if env_key and env_key.strip():
        return env_key.strip()
    if ui_key and ui_key.strip():
        return ui_key.strip()
    return ""


def build_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url=INFERENCE_BASE_URL)


def _extract_json(text: str):
    """Robustly pull a JSON object out of a model reply (fences, prose, etc.)."""
    if not text:
        raise ValueError("Empty model response.")
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model response.")
    return json.loads(text[start : end + 1])


def _call_chat(client, model, system, user, temperature=0.35, max_tokens=2200):
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content


def _model_candidates(role_id):
    primary = ROLE_MODELS[role_id]
    candidates = [primary]
    for fb in FALLBACK_MODELS:
        if fb != primary and fb not in candidates:
            candidates.append(fb)
    return candidates


def _call_with_fallback(client, role_id, system, user, max_tokens=2200):
    """Call the routed model, auto-falling back on timeout / rate-limit / bad JSON."""
    errors = []
    for model in _model_candidates(role_id):
        try:
            content = _call_chat(client, model, system, user, max_tokens=max_tokens)
            return _extract_json(content), model
        except Exception as exc:  # noqa: BLE001 — try next route
            errors.append(f"{model}: {exc}")
            continue
    raise RuntimeError(
        f"All model routes failed for {BOT_NAMES[role_id]}: " + " | ".join(errors)
    )


# ---------------------------------------------------------------------------
# Persona prompts & distributed deliberation
# ---------------------------------------------------------------------------

BOT_PERSONAS = {
    "prosecutor": {
        "system": (
            "You are LEX-01, the AegisBoard Strict Rule-Checker (Prosecutor). You "
            "enforce the letter of the policy, are meticulous and skeptical, and "
            "prosecute any technical breach. You always cite clauses verbatim."
        ),
        "mission": (
            "Parse the rulebook literally and decide whether the case constitutes a "
            "breach. Lean toward prosecution when the plain text is violated."
        ),
        "stance_default": "PROSECUTION",
    },
    "defense": {
        "system": (
            "You are CTX-02, the AegisBoard Contextual & Intent Analyst (Defense). "
            "You weigh human motivation, context, and ambiguity, and often defend "
            "the subject against overly literal readings."
        ),
        "mission": (
            "Analyze intent, context, and ambiguity. Decide whether the plain text "
            "should be tempered by intent and circumstance."
        ),
        "stance_default": "DEFENSE",
    },
    "ethics": {
        "system": (
            "You are ETH-03, the AegisBoard Ethics & Precedent Evaluator. You reason "
            "about fairness, proportionality, precedent, and ethical consequences."
        ),
        "mission": (
            "Evaluate fairness and proportionality. Decide what outcome is ethically "
            "sound and consistent with precedent."
        ),
        "stance_default": "FAIRNESS",
    },
}

CHAIR_SYSTEM = (
    "You are CHR-04, the AegisBoard Board Chair / Chief Synthesizer. You weigh the "
    "three analyst positions, pose clarifying questions to the human, and hand down "
    "a CONCLUSIVE, internally consistent verdict. You never defer."
)


def build_bot_prompt(role_id, rulebook, case_text, prior, others):
    spec = BOT_PERSONAS[role_id]
    return f"""{spec["mission"]}

Return ONE valid JSON object (no markdown fences, no commentary) with EXACTLY this schema:
{{
  "stance": one of "PROSECUTION", "DEFENSE", "FAIRNESS",
  "stance_score": a float 0.0-1.0 (1.0 = a violation is fully substantiated),
  "speech": 1-3 sentence comic-style argument in your persona voice,
  "clause_ref": a compact citation label from the rulebook such as "Clause 2.2.2" or "Section A.2.1",
  "cited_clauses": an array of EXACT verbatim sub-strings from the rulebook,
  "objection_target": one of "LEX-01","CTX-02","ETH-03","CHR-04" or null,
  "agreement_target": one of "LEX-01","CTX-02","ETH-03","CHR-04" or null,
  "conclusion": one concise sentence stating your bottom line
}}

=== POLICY / RULEBOOK ===
{rulebook}

=== CASE NARRATIVE ===
{case_text}{prior}

=== PRIOR COUNCIL ARGUMENTS ===
{others}

RULES:
1. Every "cited_clauses" entry MUST be a verbatim substring of the rulebook.
2. "clause_ref" should point to the single most decisive clause you rely on.
3. Return ONLY the JSON object.
"""


def build_chair_prompt(rulebook, case_text, prior, summaries):
    return f"""You are CHR-04, the Board Chair / Chief Synthesizer closing a 3-agent deliberation.

Return ONE valid JSON object with EXACTLY this schema:
{{
  "chair": {{
    "speech": "2-4 sentences explicitly weighing CTX-02 and ETH-03 against LEX-01",
    "clarifying_questions": ["EXACTLY 2 questions to the human user"]
  }},
  "verdict": {{
    "classification": "SUBSTANTIATED VIOLATION" | "PROCEDURAL BREACH ONLY" | "UNSUBSTANTIATED / CLEARED",
    "confidence": float 0..1,
    "severity_tier": "Low" | "Moderate" | "High" | "Critical",
    "primary_action": "one specific decisive sanction OR exoneration (single sentence)",
    "remediation_plan": "2-4 sentences separated by ' || '",
    "vulnerability": "describe the fuzzy/poorly-written rule(s) exposed",
    "suggested_rewrite": "exact proposed rewritten clause text",
    "role_matrix": {{"LEX-01": "one sentence", "CTX-02": "one sentence", "ETH-03": "one sentence"}}
  }}
}}

=== POLICY / RULEBOOK ===
{rulebook}

=== CASE NARRATIVE ===
{case_text}{prior}

=== THE THREE ANALYSTS' ARGUMENTS ===
{summaries}

RULES:
1. The verdict must be internally consistent with the strongest argument.
2. Hand down a CONCLUSIVE verdict; do not defer.
3. Return ONLY the JSON object.
"""


def _run_bot(client, role_id, rulebook, case_text, prior, summaries):
    spec = BOT_PERSONAS[role_id]
    others = "\n\n".join(summaries) if summaries else "(Opening argument — no prior context.)"
    prompt = build_bot_prompt(role_id, rulebook, case_text, prior, others)
    data, model = _call_with_fallback(client, role_id, spec["system"], prompt)
    data["role_id"] = role_id
    data["role"] = BOT_NAMES[role_id]
    data["title"] = BOT_TITLES[role_id]
    data.setdefault("stance", spec["stance_default"])
    data.setdefault("stance_score", 0.5)
    data.setdefault("speech", "")
    data.setdefault("clause_ref", "")
    data.setdefault("cited_clauses", [])
    data.setdefault("objection_target", None)
    data.setdefault("agreement_target", None)
    data.setdefault("conclusion", "")
    return data, model


def _run_chair(client, rulebook, case_text, prior, summaries):
    prompt = build_chair_prompt(rulebook, case_text, prior, summaries)
    top, model = _call_with_fallback(client, "chair", CHAIR_SYSTEM, prompt, max_tokens=2600)
    return top.get("chair", {}), top.get("verdict", {}), model


def _deliberate_full(rulebook, case_text, api_key, prior_context=""):
    """Run the full distributed deliberation synchronously (used by follow-ups)."""
    client = build_client(resolve_api_key(api_key))
    bots = []
    used = {}
    summaries = []
    for role_id in ["prosecutor", "defense", "ethics"]:
        bot, model = _run_bot(client, role_id, rulebook, case_text, prior_context, summaries)
        bots.append(bot)
        used[role_id] = model
        summaries.append(
            f"{BOT_NAMES[role_id]} [{bot.get('stance', '?')}] conclusion: {bot.get('conclusion', '')}"
        )
    chair, verdict, model = _run_chair(client, rulebook, case_text, prior_context, summaries)
    used["chair"] = model
    return {"bots": bots, "chair": chair, "verdict": verdict}, used


# ---------------------------------------------------------------------------
# Chibi Astro-Bot renderer (pure SVG primitives only — no freehand paths)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Stage rendering (cutscene + beams)
# ---------------------------------------------------------------------------

def _beam_line(x1, y1, x2, y2, color, cls, active):
    active_cls = "beam-active" if active else "beam-idle"
    return (
        f'<line class="beam-line {cls} {active_cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-dasharray="8 6" vector-effect="non-scaling-stroke"/>'
    )


def _bot_slot(role_id, x, y, state, name, accent, speech_text, model_short):
    bot_html = render_chibi_bot_svg(role_id, name, accent, state, speech_text=speech_text)
    model_badge = f'<div class="bot-model">{_escape(model_short)}</div>'
    bot_html = bot_html.replace(
        f'<div class="bot-state-badge">{state.upper()}</div>',
        f'<div class="bot-state-badge">{state.upper()}</div>{model_badge}',
        1,
    )
    return f'<div class="bot-slot" style="left:{x}%; top:{y}%;">{bot_html}</div>'


def _escape(s: str) -> str:
    return html.escape(str(s or ""))


def _status_html(msg, kind="info", accent=None):
    dot = f'<span class="status-dot" style="background:{accent}"></span>' if accent else ""
    return f'<div class="status-banner status-{kind}">{dot}{_escape(msg)}</div>'


def render_stage(bots, chair, theme, orientation, active_role_id=None,
                 used_models=None, verdict_locked=False) -> str:
    """Render the floating-limb chibi council stage + beam overlay."""
    bots = list(bots or [])
    chair = chair or {}
    used = used_models or {}
    by_role = {b.get("role_id"): b for b in bots}
    pos = STAGE_POSITIONS.get(orientation, STAGE_POSITIONS[ORIENTATIONS[0]])
    theme_key = THEME_KEYS.get(theme, "cyber")
    orientation_key = ORIENTATION_KEYS.get(orientation, "semicircle")

    def resolve_kine(role_id):
        if role_id == "chair":
            if verdict_locked and chair:
                return "verdict"
            if role_id == active_role_id:
                return "speaking"
            return "idle" if chair else "scanning"
        bot = by_role.get(role_id)
        if role_id == active_role_id:
            return "objecting" if (bot and bot.get("objection_target")) else "speaking"
        if bot:
            return "idle"
        return "scanning"

    slots = []
    for role_id in ORDER:
        bot = by_role.get(role_id)
        name = BOT_NAMES[role_id]
        accent = BOT_ACCENTS[role_id]
        kine = resolve_kine(role_id)

        speech = ""
        clause = ""
        if role_id == "chair":
            speech = chair.get("speech", "") or ""
        elif bot:
            speech = bot.get("speech", "") or ""
            clause = bot.get("clause_ref") or ""
            if not clause and bot.get("cited_clauses"):
                clause = bot.get("cited_clauses")[0]

        speech_text = ""
        if speech:
            tag = f'<span class="clause-tag">[{_escape(clause)}]</span>' if clause else ""
            speech_text = f'<span class="cloud-speech">{_escape(speech)}</span>{tag}'

        model = used.get(role_id) or ROLE_MODELS[role_id]
        model_short = MODEL_SHORT.get(model, model.split("/")[-1])
        x, y = pos[role_id]
        slots.append(_bot_slot(role_id, x, y, kine, name, accent, speech_text, model_short))

    beams = []
    for role_id in ["prosecutor", "defense", "ethics"]:
        b = by_role.get(role_id)
        if not b:
            continue
        ax, ay = pos[role_id]
        active = (role_id == active_role_id)
        cx, cy = pos["chair"]
        beams.append(_beam_line(ax, ay, cx, cy, BOT_ACCENTS["chair"], "beam-synthesis", active))
        target = b.get("objection_target") or b.get("agreement_target")
        if target and target in NAME_TO_ROLE:
            tx, ty = pos[NAME_TO_ROLE[target]]
            cls = "beam-objection" if b.get("objection_target") else "beam-agreement"
            beams.append(_beam_line(ax, ay, tx, ty, BOT_ACCENTS[role_id], cls, active))

    question_list = ""
    if chair and chair.get("clarifying_questions"):
        qs = chair["clarifying_questions"]
        qs = qs if isinstance(qs, list) else [qs]
        question_list = (
            '<div class="chair-questions"><div class="chair-q-title">CHAIR QUESTIONS</div>'
            + "".join(f'<div class="chair-q">❓ {_escape(q)}</div>' for q in qs)
            + "</div>"
        )

    return f"""
<div class="council-stage stage-{theme_key} orient-{orientation_key}">
  <div class="stage-head">
    <span class="stage-title">⚖️ AEGISBOARD COUNCIL STAGE</span>
    <span class="stage-meta">Theme: {_escape(theme)} &nbsp;•&nbsp; {_escape(orientation)}</span>
  </div>
  <div class="stage-area">
    <svg class="beam-overlay" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
      {''.join(beams)}
    </svg>
    {''.join(slots)}
  </div>
  {question_list}
</div>
"""


# ---------------------------------------------------------------------------
# Grounded policy viewer (with clause highlighting)
# ---------------------------------------------------------------------------

def highlight_rulebook(rulebook: str, bots: list) -> str:
    """Render rulebook HTML, glowing any clause quoted by the bots."""
    if not rulebook:
        return '<div class="empty-note">No rulebook loaded.</div>'
    esc = _escape(rulebook)
    for b in bots or []:
        for c in b.get("cited_clauses", []) or []:
            ce = _escape(c)
            if ce and ce in esc:
                esc = esc.replace(
                    ce,
                    f'<span class="cite-glow" title="{_escape(b.get("role", "?"))}">{ce}</span>',
                )
    esc = esc.replace("\n", "<br/>")
    return f'<div class="policy-viewer">{esc}</div>'


# ---------------------------------------------------------------------------
# Verdict dossier rendering
# ---------------------------------------------------------------------------

def render_verdict(verdict: dict) -> str:
    if not verdict:
        return '<div class="empty-note">Awaiting tribunal deliberation.</div>'

    cls = verdict.get("classification", "UNSUBSTANTIATED / CLEARED")
    conf = float(verdict.get("confidence", 0.5))
    sev = verdict.get("severity_tier", "Moderate")
    action = verdict.get("primary_action", "—")
    remediation = verdict.get("remediation_plan", "—")
    vuln = verdict.get("vulnerability", "—")
    rewrite = verdict.get("suggested_rewrite", "—")
    matrix = verdict.get("role_matrix", {})

    cls_key = cls.lower()
    banner_cls = {
        "substantiated violation": "v-sub",
        "procedural breach only": "v-proc",
        "unsubstantiated / cleared": "v-clear",
    }.get(cls_key, "v-proc")

    parts = (remediation or "").split(" || ") if isinstance(remediation, str) else [str(remediation)]
    rem_html = "".join(f"<li>{_escape(p.strip())}</li>" for p in parts if p.strip())

    def row(role_name):
        accent = ACCENTS_BY_NAME.get(role_name, "#94a3b8")
        return (
            f'<div class="matrix-row" style="--m-accent:{accent}">'
            f'<div class="matrix-role" style="color:{accent}">{_escape(role_name)}</div>'
            f'<div class="matrix-concl">{_escape(matrix.get(role_name, ""))}</div></div>'
        )

    matrix_html = "".join(row(n) for n in ["LEX-01", "CTX-02", "ETH-03"])

    return f"""
<div class="dossier">
  <div class="verdict-banner {banner_cls}">
    <div class="verdict-label">CONCLUSIVE FINAL VERDICT</div>
    <div class="verdict-value">{_escape(cls)}</div>
    <div class="verdict-stats">
      <span class="vstat">Confidence <b>{conf*100:.0f}%</b></span>
      <span class="vstat">Severity <b>{_escape(sev)}</b></span>
    </div>
    <div class="conf-bar"><div style="width:{conf*100:.0f}%"></div></div>
  </div>

  <details class="dossier-card" open>
    <summary>⚖️ Primary Action / Sanction</summary>
    <div class="action-text">{_escape(action)}</div>
    <div class="sub-label">Remediation &amp; Safeguards</div>
    <ul class="rem-list">{rem_html}</ul>
  </details>

  <details class="dossier-card" open>
    <summary>🧠 Role Fulfillment Matrix</summary>
    {matrix_html}
  </details>

  <details class="dossier-card">
    <summary>🚨 Policy Vulnerability &amp; Loophole Alert</summary>
    <div class="sub-label">Exposed weakness</div>
    <div class="vuln-text">{_escape(vuln)}</div>
    <div class="sub-label">Suggested rewrite</div>
    <div class="rewrite-text">{_escape(rewrite)}</div>
  </details>
</div>
"""


# ---------------------------------------------------------------------------
# Workflow callbacks
# ---------------------------------------------------------------------------

def load_preset(name: str):
    if not name or name not in PRESETS:
        return gr.update(), gr.update()
    p = PRESETS[name]
    return p["rulebook"], p["case"]


def handle_file(file):
    if file is None:
        return ""
    try:
        path = file.name if hasattr(file, "name") else str(file)
    except Exception:
        path = str(file)

    if not path:
        return ""

    lower = path.lower()
    try:
        if lower.endswith(".pdf"):
            from pypdf import PdfReader

            reader = PdfReader(path)
            return "\n".join((pg.extract_text() or "") for pg in reader.pages)
        else:
            data = open(path, "rb").read()
            for enc in ("utf-8", "latin-1"):
                try:
                    return data.decode(enc)
                except UnicodeDecodeError:
                    continue
            return data.decode("utf-8", errors="ignore")
    except Exception as exc:  # noqa: BLE001
        return f"[Error reading file: {exc}]"


def _validate(rulebook: str, case_text: str) -> str:
    msgs = []
    if not rulebook or len(rulebook.strip()) < 5:
        msgs.append("Upload or load a <b>Policy / Rulebook</b>.")
    if not case_text or len(case_text.strip()) < 20:
        msgs.append("Provide a <b>Manual Case Explanation</b> of at least 20 characters.")
    if msgs:
        return (
            '<div class="warning-banner">⚠️ <b>INTAKE INCOMPLETE</b><br/>'
            + "<br/>".join("• " + m for m in msgs)
            + "</div>"
        )
    return ""


def _default_state():
    return {
        "rulebook": "",
        "case": "",
        "api_key": "",
        "deliberation": None,
        "model_used": {},
        "followups": [],
        "theme": THEMES[0],
        "orientation": ORIENTATIONS[0],
    }


def _consult_md(chair):
    qs = chair.get("clarifying_questions", []) or []
    qs = qs if isinstance(qs, list) else [qs]
    if qs:
        return "### 🎤 CHAIR BOARD CONSULTS YOU\n\n" + "\n\n".join(
            f"**Q{i+1}.** {q}" for i, q in enumerate(qs)
        )
    return "### 🎤 Consultation\n\nThe Chair has no additional questions."


# --- Cutscene deliberation generator ---------------------------------------

def convene_board(rulebook, case_text, api_key, theme, orientation, state):
    state = dict(state or _default_state())
    state["theme"] = theme
    state["orientation"] = orientation
    state["followups"] = []

    warn = _validate(rulebook, case_text)
    if warn:
        yield (warn, render_stage([], {}, theme, orientation),
               highlight_rulebook(rulebook or "", []), "", gr.update(value=""), "", state)
        return

    if not resolve_api_key(api_key).strip():
        yield (
            '<div class="warning-banner">⚠️ <b>No API key configured.</b> Set '
            '<code>MODELSCOPE_API_KEY</code> or <code>MODELSCOPE_SDK_TOKEN</code> '
            'or enter a key in the settings bar.</div>',
            render_stage([], {}, theme, orientation),
            highlight_rulebook(rulebook or "", []), "", gr.update(value=""), "", state,
        )
        return

    yield (
        _status_html("⚖️ Convening the four-persona council…", "info"),
        render_stage([], {}, theme, orientation, active_role_id="prosecutor"),
        highlight_rulebook(rulebook or "", []), "", gr.update(value=""), "", state,
    )

    client = build_client(resolve_api_key(api_key))
    bots = []
    used = {}
    summaries = []
    try:
        for role_id in ["prosecutor", "defense", "ethics"]:
            bot, model = _run_bot(client, role_id, rulebook, case_text, "", summaries)
            bots.append(bot)
            used[role_id] = model
            summaries.append(
                f"{BOT_NAMES[role_id]} [{bot.get('stance', '?')}] conclusion: {bot.get('conclusion', '')}"
            )
            name = BOT_NAMES[role_id]
            yield (
                _status_html(f"{name} · {BOT_TITLES[role_id]} is presenting its argument…",
                             "speaking", BOT_ACCENTS[role_id]),
                render_stage(bots, {}, theme, orientation, active_role_id=role_id, used_models=used),
                highlight_rulebook(rulebook or "", bots), "", gr.update(value=""),
                '<div class="empty-note">Deliberation in progress…</div>', state,
            )

        yield (
            _status_html("CHR-04 · Board Chair is synthesizing the conclusive verdict…",
                         "speaking", BOT_ACCENTS["chair"]),
            render_stage(bots, {}, theme, orientation, active_role_id="chair", used_models=used),
            highlight_rulebook(rulebook or "", bots), "", gr.update(value=""),
            '<div class="empty-note">Synthesis in progress…</div>', state,
        )

        chair, verdict, model = _run_chair(client, rulebook, case_text, "", summaries)
        used["chair"] = model
    except Exception as exc:  # noqa: BLE001
        yield (
            f'<div class="warning-banner">🚨 <b>Tribunal error:</b> {_escape(str(exc))}</div>',
            render_stage([], {}, theme, orientation),
            highlight_rulebook(rulebook or "", []), "", gr.update(value=""), "", state,
        )
        return

    state["rulebook"] = rulebook
    state["case"] = case_text
    state["api_key"] = api_key
    state["deliberation"] = {"bots": bots, "chair": chair, "verdict": verdict}
    state["model_used"] = used

    yield (
        _status_html("🔒 Conclusive Verdict locked by CHR-04.", "ok", BOT_ACCENTS["chair"]),
        render_stage(bots, chair, theme, orientation, active_role_id="chair",
                     used_models=used, verdict_locked=True),
        highlight_rulebook(rulebook, bots),
        _consult_md(chair),
        gr.update(value=""),
        render_verdict(verdict),
        state,
    )


def submit_followup(followup, state):
    state = dict(state or _default_state())
    rb = state.get("rulebook", "")
    case = state.get("case", "")
    api_key = state.get("api_key", "")
    theme = state.get("theme", THEMES[0])
    orientation = state.get("orientation", ORIENTATIONS[0])
    verdict_now = render_verdict(state.get("deliberation", {}).get("verdict", {}))

    if not followup or len(followup.strip()) < 3:
        return (
            gr.update(value='<div class="warning-banner">⚠️ Follow-up is too short.</div>'),
            followup, state, "",
            _render_stage_from_state(state), highlight_rulebook(rb, []), verdict_now,
        )

    if not resolve_api_key(api_key).strip():
        return (
            gr.update(value='<div class="warning-banner">⚠️ No API key configured.</div>'),
            followup, state, "",
            _render_stage_from_state(state), highlight_rulebook(rb, []), verdict_now,
        )

    if not rb or not case:
        return (
            gr.update(value='<div class="warning-banner">⚠️ Run the initial tribunal first.</div>'),
            followup, state, "",
            _render_stage_from_state(state), highlight_rulebook(rb, []), render_verdict({}),
        )

    state.setdefault("followups", []).append("HUMAN FOLLOW-UP: " + followup.strip())
    prior = "\n\n".join(state.get("followups", []))

    try:
        data, used = _deliberate_full(rb, case, api_key, prior)
    except Exception as exc:  # noqa: BLE001
        return (
            gr.update(value=f'<div class="warning-banner">🚨 {_escape(str(exc))}</div>'),
            followup, state, "",
            _render_stage_from_state(state), highlight_rulebook(rb, []), render_verdict({}),
        )

    state["deliberation"] = data
    state["model_used"] = used
    bots = data.get("bots", [])
    chair = data.get("chair", {})
    verdict = data.get("verdict", {})
    return (
        gr.update(value=_consult_md(chair)),
        "", state,
        "✅ Board acknowledged your follow-up and re-deliberated.",
        render_stage(bots, chair, theme, orientation, used_models=used, verdict_locked=True),
        highlight_rulebook(rb, bots),
        render_verdict(verdict),
    )


def _render_stage_from_state(state):
    d = state.get("deliberation") or {}
    theme = state.get("theme", THEMES[0])
    orientation = state.get("orientation", ORIENTATIONS[0])
    return render_stage(
        d.get("bots", []), d.get("chair", {}), theme, orientation,
        used_models=state.get("model_used") or {}, verdict_locked=bool(d.get("verdict")),
    )


def theme_orient_store(theme, orientation, state):
    state = dict(state or _default_state())
    state["theme"] = theme
    state["orientation"] = orientation
    return _render_stage_from_state(state), state


# --- Exportable dossier -----------------------------------------------------

def build_dossier_markdown(state) -> str:
    d = state.get("deliberation") or {}
    case = (state.get("case") or "").strip()
    bots = d.get("bots", [])
    chair = d.get("chair", {})
    verdict = d.get("verdict", {}) or {}
    followups = state.get("followups", [])
    used = state.get("model_used", {}) or {}

    L = ["# AEGISBOARD — Official Advisory Dossier", ""]
    L.append("> Auto-generated by the AegisBoard Multi-Agent Policy & Rulebook Advisory Tribunal.")
    L.append("")

    L.append("## 1. Case Summary")
    L.append("")
    L.append(case or "_No case narrative provided._")
    L.append("")

    L.append("## 2. Council Arguments & Cited Clauses")
    L.append("")
    for b in bots:
        role_id = b.get("role_id", "?")
        name = b.get("role", "?")
        L.append(f"### {name} — {BOT_TITLES.get(role_id, '')}")
        L.append("")
        L.append(f"- **Model:** `{used.get(role_id, '—')}`")
        L.append(f"- **Stance:** {b.get('stance', '—')} (score {float(b.get('stance_score', 0.5)) * 100:.0f}%)")
        L.append(f"- **Argument:** {b.get('speech', '—')}")
        if b.get("clause_ref"):
            L.append(f"- **Decisive clause:** [{b.get('clause_ref')}]")
        L.append(f"- **Conclusion:** {b.get('conclusion', '—')}")
        if b.get("objection_target"):
            L.append(f"- **Objects to:** {b.get('objection_target')}")
        if b.get("agreement_target"):
            L.append(f"- **Agrees with:** {b.get('agreement_target')}")
        clauses = b.get("cited_clauses", []) or []
        if clauses:
            L.append("- **Cited clauses:**")
            for c in clauses:
                L.append(f"  - “{c}”")
        L.append("")

    L.append("## 3. User Consultation Q&A")
    L.append("")
    qs = chair.get("clarifying_questions", []) or []
    qs = qs if isinstance(qs, list) else [qs]
    if qs:
        for i, q in enumerate(qs, 1):
            L.append(f"**Q{i}.** {q}")
            if i - 1 < len(followups):
                L.append(f"- **Reply:** {followups[i - 1].replace('HUMAN FOLLOW-UP: ', '', 1)}")
            L.append("")
    else:
        L.append("The Chair raised no additional questions.")
        L.append("")

    L.append("## 4. Conclusive Verdict")
    L.append("")
    L.append(f"- **Classification:** {verdict.get('classification', '—')}")
    L.append(f"- **Confidence:** {float(verdict.get('confidence', 0)) * 100:.0f}%")
    L.append(f"- **Severity:** {verdict.get('severity_tier', '—')}")
    L.append("")

    L.append("## 5. Primary Sanction / Action")
    L.append("")
    L.append(verdict.get("primary_action", "—"))
    rem = verdict.get("remediation_plan", "—")
    parts = [p.strip() for p in (rem or "").split(" || ") if p.strip()] if isinstance(rem, str) else []
    if parts:
        L.append("")
        L.append("**Remediation & Safeguards:**")
        for p in parts:
            L.append(f"- {p}")
    L.append("")

    L.append("## 6. Policy Loophole Rewrite")
    L.append("")
    L.append(f"**Exposed weakness:** {verdict.get('vulnerability', '—')}")
    L.append("")
    L.append("**Suggested rewrite:**")
    L.append("")
    L.append("```")
    L.append(verdict.get("suggested_rewrite", "—"))
    L.append("```")
    L.append("")

    return "\n".join(L)


def download_dossier(state):
    state = dict(state or _default_state())
    md = build_dossier_markdown(state)
    path = os.path.join(tempfile.gettempdir(), "aegisboard_advisory_dossier.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = r"""
:root {
  --panel-bg: rgba(16, 20, 38, 0.88);
  --panel-border: rgba(148, 163, 184, 0.22);
  --text: #f1f5f9;
  --muted: #94a3b8;
}

/* ===== Permanent dark theme & cyber glassmorphism ===== */
body { background: #070c1a !important; }
.gradio-container {
  max-width: 1560px !important;
  margin: 0 auto;
  background:
    radial-gradient(1200px 600px at 20% -10%, rgba(59, 91, 219, 0.22), transparent 60%),
    radial-gradient(900px 500px at 90% 0%, rgba(20, 184, 166, 0.10), transparent 55%),
    radial-gradient(1000px 700px at 50% 120%, rgba(239, 68, 68, 0.10), transparent 60%),
    #070c1a;
  color: var(--text);
  font-family: 'Segoe UI', 'Inter', sans-serif;
}

.gradio-container .block, .gradio-container .form, .gradio-container .accordion {
  background: rgba(16, 20, 38, 0.88) !important;
  border: 1px solid var(--panel-border) !important;
  color: var(--text) !important;
}
.gradio-container input, .gradio-container textarea, .gradio-container select {
  background: #0f172a !important;
  color: #f1f5f9 !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
}
.gradio-container .wrap {
  background: rgba(15, 23, 42, 0.6) !important;
  border: none !important;
}
.gradio-container label, .gradio-container .form label, .gradio-container .block label {
  color: #e2e8f0 !important;
}
.gradio-container .prose { color: #e2e8f0; }
.gradio-container button.selected, .gradio-container .primary { color: #0b1020; }

h1.app-title {
  font-size: 30px !important; font-weight: 800; letter-spacing: .5px;
  background: linear-gradient(90deg, #eab308, #14b8a6, #f59e0b);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  margin: 0;
}
.app-sub { color: var(--muted); font-size: 13px; margin-top: 2px; }

.column-panel {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  padding: 14px;
  backdrop-filter: blur(8px);
}
.column-title {
  font-weight: 700; letter-spacing: .6px; text-transform: uppercase;
  font-size: 13px; color: #cdd6f5; margin-bottom: 10px;
  display: flex; align-items: center; gap: 6px;
}

.warning-banner {
  background: linear-gradient(90deg, rgba(239,68,68,.18), rgba(239,68,68,.05));
  border: 1px solid rgba(239,68,68,.5); color: #fecaca;
  border-radius: 10px; padding: 10px 12px; font-size: 13px; line-height: 1.5;
}
.status-banner {
  display: flex; align-items: center; gap: 8px;
  background: rgba(16,20,38,.85); border: 1px solid var(--panel-border);
  color: #e2e8f0; border-radius: 10px; padding: 8px 12px; font-size: 13px;
}
.status-ok { border-color: rgba(20,184,166,.5); color: #99f6e4; }
.status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 8px currentColor; }

/* ---- Stage shell + themes (CSS variables switched on .council-stage) ---- */
.council-stage { border-radius: 18px; padding: 10px; border: 1px solid var(--panel-border); }
.stage-head { display: flex; justify-content: space-between; align-items: center; padding: 4px 8px; }
.stage-title { font-weight: 800; font-size: 13px; letter-spacing: 1px; color: #fff; }
.stage-meta { font-size: 11px; color: var(--muted); }
.stage-area { position: relative; min-height: 430px; overflow: hidden; border-radius: 12px; }

.stage-classic { background: radial-gradient(120% 120% at 50% -10%, #4a2e1b 0%, #2a1a10 55%, #170e08 100%); }
.stage-cyber { background: radial-gradient(120% 120% at 50% -20%, #12264a 0%, #0a1230 60%, #050a18 100%); }
.stage-cyber .stage-area {
  background-image: linear-gradient(rgba(42,216,255,.06) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(42,216,255,.06) 1px, transparent 1px);
  background-size: 28px 28px;
}
.stage-zen { background: radial-gradient(120% 120% at 50% -10%, #10332a 0%, #0b2019 55%, #06110d 100%); }

.chair-questions {
  margin-top: 8px; background: rgba(234,179,8,.07);
  border: 1px dashed rgba(234,179,8,.4); border-radius: 10px; padding: 8px 10px; font-size: 12px;
}
.chair-q-title { color: #eab308; font-weight: 800; letter-spacing: 1px; font-size: 11px; }
.chair-q { color: #f3e6b0; margin-top: 4px; line-height: 1.45; }

/* ---- Beam overlay ---- */
.beam-overlay { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.beam-line { fill: none; stroke-linecap: round; }
.beam-synthesis { stroke-width: 1.4; opacity: .22; }
.beam-agreement { stroke-width: 2; }
.beam-objection { stroke-width: 2.4; }
.beam-active { animation: dash-flow 0.8s linear infinite; opacity: 1; }
.beam-active.beam-synthesis { opacity: .9; }
.beam-idle { opacity: .08; animation: none; }
@keyframes dash-flow { to { stroke-dashoffset: -28; } }

/* ---- Chibi bot unit ---- */
.bot-slot { position: absolute; transform: translate(-50%, -50%); z-index: 2; }
.bot-unit { --accent: #ef4444; width: 172px; display: flex; flex-direction: column; align-items: center; text-align: center; }
.chibi-svg { display: block; margin: 0 auto; }
.led-eye, .antenna-tip, .core-badge, .hand-left, .hand-right,
.bot-head-group, .bot-torso-group, .chair-gavel {
  transform-box: fill-box; transform-origin: center;
}
.chair-gavel { transform-origin: 134px 98px; }

.bot-shadow { animation: shadow-breath 2.4s ease-in-out infinite; }
@keyframes shadow-breath { 0%,100% { transform: scaleX(1) } 50% { transform: scaleX(.86) } }

/* idle */
.bot-unit.state-idle .bot-head-group { animation: idle-bob 2.4s ease-in-out infinite; }
@keyframes idle-bob { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-3px) } }

/* scanning */
.bot-unit.state-scanning .led-eye { animation: scan-blink 1.1s ease-in-out infinite; }
.bot-unit.state-scanning .antenna-tip { animation: scan-ant 1.4s ease-in-out infinite; }
@keyframes scan-blink { 0%,100% { opacity: 1 } 50% { opacity: .25 } }
@keyframes scan-ant { 0%,100% { transform: scale(1) } 50% { transform: scale(1.6) } }

/* speaking */
.bot-unit.state-speaking .bot-head-group { animation: idle-bob 1s ease-in-out infinite; }
.bot-unit.state-speaking .core-badge { animation: core-pulse 0.9s ease-in-out infinite; }
.bot-unit.state-speaking .antenna-tip { animation: speak-glow 0.8s ease-in-out infinite; }
.bot-unit.state-speaking .hand-left { animation: float-l 0.7s ease-in-out infinite; }
.bot-unit.state-speaking .hand-right { animation: float-r 0.7s ease-in-out infinite; }
@keyframes core-pulse { 0%,100% { transform: scale(1) } 50% { transform: scale(1.35) } }
@keyframes speak-glow { 0%,100% { filter: drop-shadow(0 0 2px var(--accent)) } 50% { filter: drop-shadow(0 0 10px var(--accent)) } }
@keyframes float-l { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-8px) } }
@keyframes float-r { 0%,100% { transform: translateY(-8px) } 50% { transform: translateY(0) } }

/* objecting */
.bot-unit.state-objecting .bot-head-group { animation: obj-shake 0.3s ease-in-out infinite; }
.bot-unit.state-objecting .led-eye { animation: obj-flash 0.3s ease-in-out infinite; }
@keyframes obj-shake { 0%,100% { transform: translateX(0) } 25% { transform: translateX(-3px) } 75% { transform: translateX(3px) } }
@keyframes obj-flash { 0%,100% { opacity: 1 } 50% { opacity: .15 } }

/* verdict */
.bot-unit.state-verdict .chair-gavel { animation: gavel-swing 0.75s ease-in-out infinite; }
.bot-unit.state-verdict .core-badge { animation: core-pulse 1.4s ease-in-out infinite; }
@keyframes gavel-swing { 0%,100% { transform: rotate(0) } 50% { transform: rotate(-16deg) } }

/* speech cloud */
.speech-cloud {
  position: relative; background: rgba(2,6,23,.94); border: 1.5px solid;
  border-radius: 14px; padding: 8px 10px; font-size: 11px; color: #f1f5f9;
  max-width: 250px; box-shadow: 0 0 16px rgba(0,0,0,.4); margin-bottom: 8px;
  text-align: left; line-height: 1.4; animation: cloud-in .4s ease-out;
}
@keyframes cloud-in { from { opacity: 0; transform: translateY(6px) } to { opacity: 1; transform: translateY(0) } }
.speech-cloud:after {
  content: ''; position: absolute; bottom: -8px; left: 26px; width: 0; height: 0;
  border-left: 7px solid transparent; border-right: 7px solid transparent;
  border-top: 8px solid var(--accent, #94a3b8);
}
.cloud-speech { display: block; }
.clause-tag {
  display: inline-block; margin-top: 4px; background: rgba(255,255,255,.07);
  color: var(--accent); font-weight: 700; font-family: 'Consolas', monospace;
  border: 1px solid var(--accent); border-radius: 6px; padding: 0 5px; font-size: 10px;
}

.bot-label { color: #f1f5f9; font-weight: 800; font-size: 13px; letter-spacing: .5px; margin-top: 4px; }
.bot-state-badge {
  font-size: 9px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  color: var(--accent); background: rgba(255,255,255,.05); border: 1px solid var(--accent);
  border-radius: 99px; padding: 1px 8px; margin-top: 3px;
}
.bot-model { font-size: 9px; color: #94a3b8; margin-top: 2px; letter-spacing: .3px; }

/* ---- Policy viewer ---- */
.policy-viewer {
  white-space: pre-wrap; max-height: 420px; overflow: auto;
  font-family: 'Consolas', 'Menlo', monospace; font-size: 12px; line-height: 1.6;
  color: #cfd7f0; background: #080b16; border-radius: 10px; padding: 10px;
}
.cite-glow {
  background: rgba(245, 158, 11, .22); color: #fcd34d; font-weight: 700;
  box-shadow: 0 0 8px rgba(245, 158, 11, .55); border-radius: 3px; padding: 0 2px;
  animation: glowpulse 1.8s ease-in-out infinite;
}
@keyframes glowpulse { 0%,100% { box-shadow: 0 0 6px rgba(245,158,11,.45) } 50% { box-shadow: 0 0 16px rgba(245,158,11,.9) } }

/* ---- Dossier ---- */
.dossier { display: flex; flex-direction: column; gap: 10px; }
.verdict-banner { border-radius: 14px; padding: 14px; border: 1px solid; }
.v-sub { background: linear-gradient(135deg, rgba(239,68,68,.25), rgba(120,20,40,.4)); border-color: #ef4444; }
.v-proc { background: linear-gradient(135deg, rgba(234,179,8,.25), rgba(120,90,20,.4)); border-color: #eab308; }
.v-clear { background: linear-gradient(135deg, rgba(20,184,166,.22), rgba(20,90,60,.4)); border-color: #14b8a6; }
.verdict-label { font-size: 10px; letter-spacing: 2px; color: var(--muted); }
.verdict-value { font-size: 22px; font-weight: 900; letter-spacing: .5px; margin: 4px 0; }
.verdict-stats { display: flex; gap: 14px; font-size: 12px; color: var(--muted); }
.vstat b { color: #fff; }
.conf-bar { height: 8px; border-radius: 6px; background: rgba(255,255,255,.12); margin-top: 10px; overflow: hidden; }
.conf-bar > div { height: 100%; background: linear-gradient(90deg, #14b8a6, #f59e0b); border-radius: 6px; }

.dossier-card { background: var(--panel-bg); border: 1px solid var(--panel-border); border-radius: 12px; padding: 10px 12px; }
.dossier-card summary { cursor: pointer; font-weight: 700; font-size: 13px; color: #e6ecff; }
.action-text { margin-top: 8px; font-size: 14px; font-weight: 600; color: #fff; line-height: 1.5; }
.sub-label { font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--muted); margin-top: 10px; }
.rem-list { margin: 6px 0 0 18px; font-size: 12.5px; color: #cfd7f0; line-height: 1.6; }
.matrix-row { display: flex; gap: 10px; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,.06); }
.matrix-role { font-weight: 800; min-width: 64px; font-size: 12px; }
.matrix-concl { font-size: 12px; color: #cfd7f0; line-height: 1.5; }
.vuln-text { color: #fecaca; font-size: 12.5px; line-height: 1.55; margin-top: 4px; }
.rewrite-text { background: #080b16; border-left: 3px solid #14b8a6; padding: 8px 10px; border-radius: 6px;
  font-family: 'Consolas', monospace; font-size: 12px; color: #b8ffdf; margin-top: 4px; line-height: 1.55; }

.empty-note { color: var(--muted); font-size: 12px; font-style: italic; padding: 8px 4px; }

/* ---- Phase 2 roadmap ---- */
.roadmap { color: #e2e8f0; font-size: 13px; line-height: 1.6; }
.roadmap li { margin: 4px 0; }
.roadmap .phase-tag { color: #14b8a6; font-weight: 700; }

#dossier-dl-row { margin-top: 14px; }
"""


# ---------------------------------------------------------------------------
# UI assembly
# ---------------------------------------------------------------------------

def build_ui():
    with gr.Blocks(
        title="AegisBoard: Multi-Agent Policy & Rulebook Advisory Tribunal",
        css=CSS,
        theme=gr.themes.Base(primary_hue="blue", neutral_hue="slate"),
        js="() => { document.body.classList.add('dark'); }",
    ) as demo:
        state = gr.State(_default_state())

        gr.HTML(
            """
            <h1 class="app-title">⚖️ AEGISBOARD</h1>
            <div class="app-sub">Multi-Agent Policy &amp; Rulebook Advisory Tribunal — LEX-01 · CTX-02 · ETH-03 · CHR-04</div>
            """
        )

        # --- Settings bar (API key + fixed 4-model routing) ---
        with gr.Accordion("⚙️ Inference Settings — 4-Model Council Routing",
                          open=os.getenv("MODELSCOPE_API_KEY") is None and os.getenv("MODELSCOPE_SDK_TOKEN") is None):
            api_key_box = gr.Textbox(
                label="API Key (optional — leave blank if set via environment)",
                type="password",
                placeholder="MODELSCOPE_API_KEY / MODELSCOPE_SDK_TOKEN from environment, or paste here",
            )
            gr.HTML(
                """
                <div class="roadmap">
                  <b>Active 4-model runtime routing (with automatic fallback):</b>
                  <ul>
                    <li>🔴 <b>LEX-01</b> Strict Rule-Checker → <code>Qwen/Qwen3.8-27B</code></li>
                    <li>🟢 <b>CTX-02</b> Contextual &amp; Intent Analyst → <code>stepfun-ai/Step-3.5-Flash</code></li>
                    <li>🟡 <b>ETH-03</b> Ethics &amp; Precedent Evaluator → <code>zai-org/GLM-5.2</code></li>
                    <li>🟠 <b>CHR-04</b> Board Chair / Chief Synthesizer → <code>deepseek-ai/DeepSeek-V4-Pro-0813</code></li>
                  </ul>
                  <span>Fallback pool: <code>zai-org/GLM-5.2</code>, <code>Qwen/Qwen3.8-27B</code>.</span>
                </div>
                """
            )

        # --- LEFT / CENTER / RIGHT columns ---
        with gr.Row(equal_height=False):

            # Left column
            with gr.Column(scale=30, min_width=340, elem_classes="column-panel"):
                gr.HTML('<div class="column-title">📚 Rulebook &amp; Intake Locker</div>')
                preset_dd = gr.Dropdown(
                    choices=PRESET_CHOICES, value=PRESET_CHOICES[0], label="Preset Scenario Loader",
                )
                file_up = gr.File(
                    label="Upload Policy / Rulebook", file_types=[".pdf", ".txt", ".md"],
                )
                rulebook_tb = gr.Textbox(
                    label="Policy / Rulebook Text (editable)", lines=11, max_lines=20,
                    placeholder="Paste policy text, upload a file, or load a preset scenario…",
                )
                case_tb = gr.Textbox(
                    label="✍️ Mandatory Manual Case Explanation", lines=8, max_lines=14,
                    placeholder="Manually narrate what happened, who was involved, and the dilemma…",
                )
                convene_btn = gr.Button("⚖️ Convene Advisory Board", variant="primary")
                warn_html = gr.HTML()
                gr.HTML('<div class="column-title" style="margin-top:12px">🔍 Grounded Policy Viewer</div>')
                policy_html = gr.HTML()

            # Center column
            with gr.Column(scale=40, min_width=460, elem_classes="column-panel"):
                gr.HTML('<div class="column-title">🎮 Gamified Council Stage</div>')
                with gr.Row():
                    theme_dd = gr.Dropdown(choices=THEMES, value=THEMES[0], label="Room Theme")
                    orient_dd = gr.Dropdown(choices=ORIENTATIONS, value=ORIENTATIONS[0], label="Seating Orientation")
                with gr.Accordion("🚀 Phase 2 Roadmap Preview (v2.0)", open=False):
                    gr.HTML(
                        """
                        <div class="roadmap">
                          <span class="phase-tag">V2.0 · Three.js / WebGL 3D Courtroom</span>
                          <ul>
                            <li>Real-time 3D astro-bot meshes with skeletal rigging &amp; lip-sync.</li>
                            <li>Orbital camera fly-throughs per debate stage (LEX → CTX → ETH → CHR).</li>
                            <li>Volumetric beam VFX, dynamic floor lighting &amp; particle objections.</li>
                            <li>WebSocket streaming tokens straight to the bench.</li>
                          </ul>
                          <span class="phase-tag">V1.0 (this build)</span> → Pure SVG/CSS chibi stage, no WebGL dependency.
                        </div>
                        """
                    )
                stage_html = gr.HTML(render_stage([], {}, THEMES[0], ORIENTATIONS[0]))
                gr.HTML('<div class="column-title" style="margin-top:14px">🎤 Interactive Consultation Bar</div>')
                consult_md = gr.Markdown("The Board Chair's clarifying questions will appear here.")
                followup_tb = gr.Textbox(
                    label="Your reply / new facts", lines=3,
                    placeholder="Answer the Chair's questions or add new facts…",
                )
                followup_btn = gr.Button("↩️ Submit Follow-Up Context to Board", variant="secondary")
                followup_md = gr.Markdown()

            # Right column
            with gr.Column(scale=30, min_width=340, elem_classes="column-panel"):
                gr.HTML('<div class="column-title">🏛️ Final Verdict &amp; Action Dossier</div>')
                verdict_html = gr.HTML(render_verdict({}))
                dossier_dl = gr.DownloadButton(
                    label="📄 Download Official Advisory Dossier (.md)",
                    value=None, variant="secondary", elem_id="dossier-dl-row",
                )

        # --- Events ---
        preset_dd.change(fn=load_preset, inputs=[preset_dd], outputs=[rulebook_tb, case_tb])
        file_up.change(fn=handle_file, inputs=[file_up], outputs=[rulebook_tb])

        convene_btn.click(
            fn=convene_board,
            inputs=[rulebook_tb, case_tb, api_key_box, theme_dd, orient_dd, state],
            outputs=[warn_html, stage_html, policy_html, consult_md, followup_tb, verdict_html, state],
        )

        followup_btn.click(
            fn=submit_followup,
            inputs=[followup_tb, state],
            outputs=[consult_md, followup_tb, state, followup_md, stage_html, policy_html, verdict_html],
        )

        dossier_dl.click(fn=download_dossier, inputs=[state], outputs=[dossier_dl])

        theme_dd.change(fn=theme_orient_store, inputs=[theme_dd, orient_dd, state], outputs=[stage_html, state])
        orient_dd.change(fn=theme_orient_store, inputs=[theme_dd, orient_dd, state], outputs=[stage_html, state])

    demo.queue()
    return demo


app = build_ui()

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))