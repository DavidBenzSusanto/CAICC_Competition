"""
AegisBoard: Multi-Agent Policy & Rulebook Advisory Tribunal
============================================================

A production-ready Gradio web application that convenes a 4-agent AI tribunal
(LEX-01, CTX-02, ETH-03, CHR-04) to deliberate on an organization's policy
rulebook against a manually narrated case.

All AI inference is performed through the OpenAI-compatible SDK pointed at
ModelScope's inference endpoint. No API key is ever hard-coded.
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

MODELS = [
    "deepseek-ai/DeepSeek-V4-Pro-0813",
    "zai-org/GLM-5.2",
    "Qwen/Qwen3.8-27B",
    "stepfun-ai/Step-3.5-Flash",
]

DEFAULT_MODEL = MODELS[0]

MODEL_SHORT = {
    "deepseek-ai/DeepSeek-V4-Pro-0813": "DeepSeek-V4",
    "zai-org/GLM-5.2": "GLM-5.2",
    "Qwen/Qwen3.8-27B": "Qwen3.8-27B",
    "stepfun-ai/Step-3.5-Flash": "Step-3.5",
}

BOT_ROLES = ["LEX-01", "CTX-02", "ETH-03", "CHR-04"]

# Canonical air-gapped distribution of the 4 approved models across the council.
DISTRIBUTED_MODEL_MAP = {
    "LEX-01": "zai-org/GLM-5.2",
    "CTX-02": "deepseek-ai/DeepSeek-V4-Pro-0813",
    "ETH-03": "stepfun-ai/Step-3.5-Flash",
    "CHR-04": "Qwen/Qwen3.8-27B",
}

STAGE_FOCUS_CHOICES = [
    "All Bots Overview",
    "1. LEX-01 Rule Check",
    "2. CTX-02 Intent Analysis",
    "3. ETH-03 Ethics & Precedent",
    "4. CHR-04 Final Synthesis",
]

FOCUS_ROLE = {
    "All Bots Overview": None,
    "1. LEX-01 Rule Check": "LEX-01",
    "2. CTX-02 Intent Analysis": "CTX-02",
    "3. ETH-03 Ethics & Precedent": "ETH-03",
    "4. CHR-04 Final Synthesis": "CHR-04",
}

THEMES = ["Cyber Tribunal", "Classic High Court", "Zen Boardroom"]
ORIENTATIONS = ["Semicircle Tribunal", "Adversarial Arena", "Roundtable Council"]

BOT_ACCENTS = {
    "LEX-01": "#ff3b5c",  # neon crimson
    "CTX-02": "#2ad8ff",  # neon cyan
    "ETH-03": "#39ffa0",  # neon emerald
    "CHR-04": "#ffd23f",  # neon gold
}

BOT_TITLES = {
    "LEX-01": "Strict Rule-Checker",
    "CTX-02": "Contextual & Intent Analyst",
    "ETH-03": "Ethics & Precedent Evaluator",
    "CHR-04": "Chief Board Chair",
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
    "Corporate Data Privacy Breach": {
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
    "University Academic Integrity AI Usage": {
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
    "E-Commerce Seller Policy Violation": {
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
    # Strip markdown code fences.
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model response.")
    return json.loads(text[start : end + 1])


# ---------------------------------------------------------------------------
# The deliberation prompt & call
# ---------------------------------------------------------------------------

def build_deliberation_prompt(rulebook: str, case_text: str, prior_context: str = "") -> str:
    prior = ""
    if prior_context.strip():
        prior = (
            "\n\n=== ADDITIONAL CONTEXT PREVIOUSLY PROVIDED BY THE HUMAN ===\n"
            + prior_context.strip()
        )
    return f"""You are the "AegisBoard Tribunal Runtime" coordinating FOUR distinct AI personas
who must deliberate on a policy case. Produce ONE single valid JSON object (no
markdown fences, no commentary outside the JSON) with the exact schema below.

=== THE ORGANIZATION POLICY / RULEBOOK ===
{rulebook}

=== THE MANUAL CASE NARRATIVE ===
{case_text}{prior}

=== MANDATORY FIELD DEFINITIONS ===
- "bots": a JSON array with EXACTLY 4 objects, one per persona, in this order.
  Each object schema:
    "role": one of "LEX-01", "CTX-02", "ETH-03", "CHR-04",
    "title": the persona's short title,
    "stance": one of "PROSECUTION", "DEFENSE", "FAIRNESS", "SYNTHESIS",
    "stance_score": a float from 0.0 to 1.0 indicating how strongly the persona
        believes a VERIFICATION worthy of this case, 1.0 = fully substantiated,
        0.0 = fully cleared. (For a prosecutor this is near 1.0; for a skeptical
        defense it may be low.)
    "speech": 1-3 sentence comic-style argument in the persona's voice,
    "cited_clauses": array of EXACT quoted sub-strings from the rulebook above
        that the persona relies on (verbatim, no paraphrase),
    "objection_target": role it directly disputes, or null,
    "agreement_target": role it agrees with, or null,
    "conclusion": one concise sentence stating the persona's bottom line.

- "chair": the CHR-04 synthesizer object with:
    "speech": 2-4 sentences of moderation that EXPLICITLY weigh CTX-02 and
        ETH-03 against LEX-01,
    "clarifying_questions": EXACTLY 2 specific questions to the human user
        that would materially change the verdict if answered.

- "verdict": object with:
    "classification": EXACTLY one of ["SUBSTANTIATED VIOLATION",
        "PROCEDURAL BREACH ONLY", "UNSUBSTANTIATED / CLEARED"],
    "confidence": float 0..1 (consensus confidence),
    "severity_tier": one of "Low", "Moderate", "High", "Critical",
    "primary_action": one specific, decisive sanction OR exoneration mandated
        by the rulebook (single clear sentence),
    "remediation_plan": 2-4 bullet-like sentences (separated by " || ") on the
        required remediation and safeguards,
    "vulnerability": describe the fuzzy/poorly-written rule(s) exposed by this
        debate,
    "suggested_rewrite": an exact proposed rewritten clause text,
    "role_matrix": object mapping "LEX-01", "CTX-02", "ETH-03" to their
        one-sentence final conclusions.

IMPORTANT RULES:
1. Every "cited_clauses" entry MUST be a verbatim substring of the rulebook.
2. The verdict must be internally consistent with the strongest arguments.
3. CHR-04 must hand down a CONCLUSIVE verdict, not defer.
4. Return ONLY the JSON object.
"""


def run_tribunal(
    rulebook: str,
    case_text: str,
    model: str,
    api_key: str,
    prior_context: str = "",
):
    """Perform the structured multi-agent deliberation and return parsed JSON."""
    client = build_client(resolve_api_key(api_key))
    prompt = build_deliberation_prompt(rulebook, case_text, prior_context)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a meticulous legal/policy deliberation engine. "
                        "You always output a single valid JSON object and never "
                        "invent clauses that are not present in the rulebook."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.35,
            max_tokens=3000,
        )
        content = resp.choices[0].message.content
        return _extract_json(content)
    except Exception as exc:  # noqa: BLE001 — surface cleanly to UI
        raise RuntimeError(f"Tribunal inference failed: {exc}") from exc


# ---------------------------------------------------------------------------
# Optional distributed multi-model deliberation
# ---------------------------------------------------------------------------

BOT_PERSONAS = {
    "LEX-01": {
        "title": "Strict Rule-Checker",
        "system": (
            "You are LEX-01, the AegisBoard Strict Rule-Checker. You enforce the "
            "letter of the policy, are meticulous and skeptical, and prosecute any "
            "technical breach. You always cite clauses verbatim."
        ),
        "mission": (
            "Parse the rulebook literally and decide whether the case constitutes a "
            "breach. Lean toward prosecution when the plain text is violated."
        ),
    },
    "CTX-02": {
        "title": "Contextual & Intent Analyst",
        "system": (
            "You are CTX-02, the AegisBoard Contextual & Intent Analyst. You weigh "
            "human motivation, context, and ambiguity, and often defend the subject "
            "against overly literal readings."
        ),
        "mission": (
            "Analyze intent, context, and ambiguity. Decide whether the plain text "
            "should be tempered by intent and circumstance."
        ),
    },
    "ETH-03": {
        "title": "Ethics & Precedent Evaluator",
        "system": (
            "You are ETH-03, the AegisBoard Ethics & Precedent Evaluator. You reason "
            "about fairness, proportionality, precedent, and ethical consequences."
        ),
        "mission": (
            "Evaluate fairness and proportionality. Decide what outcome is ethically "
            "sound and consistent with precedent."
        ),
    },
}

CHAIR_SYSTEM = (
    "You are CHR-04, the AegisBoard Chief Board Chair. You synthesize the three "
    "analyst positions and hand down a CONCLUSIVE, internally consistent verdict. "
    "You never defer."
)


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


def build_bot_prompt(role, rulebook, case_text, prior, others):
    spec = BOT_PERSONAS[role]
    return f"""{spec["mission"]}

Return ONE valid JSON object (no markdown fences, no commentary) with EXACTLY this schema:
{{
  "stance": one of "PROSECUTION", "DEFENSE", "FAIRNESS",
  "stance_score": a float 0.0-1.0 (1.0 = a violation is fully substantiated),
  "speech": 1-3 sentence comic-style argument in your persona voice,
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
2. Return ONLY the JSON object.
"""


def build_chair_prompt(rulebook, case_text, prior, summaries):
    return f"""You are CHR-04, the Chief Board Chair moderating a 3-agent deliberation.

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


def run_tribunal_distributed(rulebook, case_text, model_map, api_key, prior_context=""):
    """Deliberate via one ModelScope model per persona, then synthesize on CHR-04."""
    client = build_client(resolve_api_key(api_key))
    prior = ""
    if prior_context.strip():
        prior = "\n\n=== HUMAN-PROVIDED CONTEXT ===\n" + prior_context.strip()

    bots = []
    summaries = []
    for role in ["LEX-01", "CTX-02", "ETH-03"]:
        spec = BOT_PERSONAS[role]
        others = "\n\n".join(summaries) if summaries else "(Opening argument — no prior context.)"
        prompt = build_bot_prompt(role, rulebook, case_text, prior, others)
        try:
            content = _call_chat(client, model_map[role], spec["system"], prompt)
            bot = _extract_json(content)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"{role} reasoning failed on {model_map[role]}: {exc}") from exc
        bot["role"] = role
        bot["title"] = spec["title"]
        if "stance" not in bot or not bot.get("stance"):
            bot["stance"] = {"LEX-01": "PROSECUTION", "CTX-02": "DEFENSE", "ETH-03": "FAIRNESS"}[role]
        bots.append(bot)
        summaries.append(
            f"{role} [{bot.get('stance', '?')}] conclusion: {bot.get('conclusion', '')}"
        )

    try:
        content = _call_chat(
            client, model_map["CHR-04"], CHAIR_SYSTEM,
            build_chair_prompt(rulebook, case_text, prior, "\n\n".join(summaries)),
            max_tokens=2600,
        )
        top = _extract_json(content)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"CHR-04 synthesis failed on {model_map['CHR-04']}: {exc}") from exc

    return {
        "bots": bots,
        "chair": top.get("chair", {}),
        "verdict": top.get("verdict", {}),
    }


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

def _escape(s: str) -> str:
    return html.escape(str(s or ""))


def _score_bar(score: float, accent: str) -> str:
    pct = max(0.0, min(1.0, float(score or 0.0))) * 100
    return (
        f'<div class="scorebar"><div class="scorefill" '
        f'style="width:{pct:.0f}%;background:{accent}"></div>'
        f'<span style="color:{accent}">{pct:.0f}%</span></div>'
    )


def _stance_badge(stance: str) -> str:
    cls = {
        "PROSECUTION": "st-pros",
        "DEFENSE": "st-def",
        "FAIRNESS": "st-fair",
        "SYNTHESIS": "st-syn",
    }.get(stance, "st-fair")
    return f'<span class="stance {cls}">{_escape(stance)}</span>'


# ---------------------------------------------------------------------------
# Stage rendering (the gamified Astro-Bot council)
# ---------------------------------------------------------------------------

def _bot_svg(role: str, is_chair: bool = False, kine: str = "scanning", model_label: str = "") -> str:
    accent = BOT_ACCENTS[role]
    extra_ant = ""
    if is_chair:
        extra_ant = '<circle cx="70" cy="16" r="6" fill="%s" class="chair-orb" />' % accent
    badge = (
        f'<text x="70" y="164" text-anchor="middle" class="model-badge" fill="{accent}">{_escape(model_label)}</text>'
        if model_label
        else ""
    )
    return f"""
  <g class="bot {role.lower().replace('-', '')}" data-kine="{kine}" style="--accent:{accent}">
    <ellipse cx="70" cy="100" rx="48" ry="58" fill="{accent}" class="kine-aura"/>
    <circle cx="70" cy="116" r="40" fill="rgba(0,0,0,0.18)" class="bot-shadow"/>
    <g class="bot-body">
      <line x1="70" y1="34" x2="70" y2="52" stroke="{accent}" stroke-width="3" class="antenna-stem"/>
      <circle cx="70" cy="30" r="7" fill="none" stroke="{accent}" stroke-width="2.5" class="antenna-tip"/>
      {extra_ant}
      <ellipse cx="70" cy="78" rx="34" ry="30" fill="url(#bodygrad)" stroke="{accent}" stroke-width="2.5"/>
      <path d="M 70 52 Q 70 42 70 48" stroke="#ffffff" stroke-width="9" fill="none" opacity="0.7" stroke-linecap="round"/>
      <rect x="52" y="66" width="36" height="24" rx="12" fill="#0b1020" stroke="{accent}" stroke-width="2" class="visor"/>
      <circle cx="63" cy="78" r="4" fill="{accent}" class="eye eye-l"/>
      <circle cx="77" cy="78" r="4" fill="{accent}" class="eye eye-r"/>
      <rect x="64" y="108" width="36" height="30" rx="9" fill="url(#bodygrad)" stroke="{accent}" stroke-width="2.5"/>
      <circle cx="70" cy="121" r="4.5" fill="{accent}"/>
      <circle cx="70" cy="131" r="3" fill="{accent}" opacity="0.7"/>
      <path d="M 34 104 L 26 118 L 34 122" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round" class="arm-l"/>
      <path d="M 106 104 L 114 118 L 106 122" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round" class="arm-r"/>
      <rect x="52" y="140" width="16" height="14" rx="4" fill="url(#bodygrad)" stroke="{accent}" stroke-width="2" class="leg-l"/>
      <rect x="72" y="140" width="16" height="14" rx="4" fill="url(#bodygrad)" stroke="{accent}" stroke-width="2" class="leg-r"/>
    </g>
    {badge}
  </g>"""


def _speech_cloud(role: str, speech: str, cited: list, focused: bool = False) -> str:
    accent = BOT_ACCENTS[role]
    clauses = "".join(
        f'<div class="cited-chip">“{_escape(c)}”</div>' for c in (cited or [])
    )
    focused_cls = " cloud-focused" if focused else ""
    return f"""
  <foreignObject class="cloud-wrap" x="0" y="0" width="232" height="120">
    <div class="speech-cloud{focused_cls}" style="--cloud-accent:{accent}">
      <div class="cloud-role" style="color:{accent}">{_escape(role)} - {_escape(BOT_TITLES[role])}</div>
      <div class="cloud-text">{_escape(speech)}</div>
      {clauses}
    </div>
  </foreignObject>"""


def _beam(x1, y1, x2, y2, stroke, width, dasharray, cls, active, opacity, marker=False):
    state = "beam-active" if active else "beam-idle"
    dash = f' stroke-dasharray="{dasharray}"' if dasharray else ""
    marker_attr = ' marker-end="url(#arrow)"' if marker else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{width}"{dash} class="beam {cls} {state}" opacity="{opacity}"{marker_attr}/>'
    )


def _kine_state(role, focused_role, locked, objection_target):
    """Map a bot to its kinesic animation state for a given inspector focus."""
    if role == "CHR-04":
        if focused_role == "CHR-04" or (focused_role is None and locked):
            return "verdict_locked"
        return "speaking"
    if focused_role:
        if role == focused_role:
            return "speaking"
        if objection_target == focused_role:
            return "objecting"
        return "scanning"
    if objection_target:
        return "objecting"
    return "speaking"


def render_stage(bots: list, chair: dict, theme: str, orientation: str,
                 focus: str = STAGE_FOCUS_CHOICES[0], models: dict = None,
                 locked: bool = False) -> str:
    """Build the animated council stage as one SVG/CSS fragment."""
    if not bots:
        bots = []
    models = models or {}
    focused_role = FOCUS_ROLE.get(focus)

    # Position mapping per orientation (x, y) for each role on a 540x400 canvas.
    spots = {
        "Semicircle Tribunal": {
            "LEX-01": (26, 210), "CTX-02": (168, 132), "ETH-03": (296, 132), "CHR-04": (414, 210),
        },
        "Adversarial Arena": {
            "LEX-01": (30, 90), "CTX-02": (340, 90), "ETH-03": (340, 230), "CHR-04": (175, 155),
        },
        "Roundtable Council": {
            "LEX-01": (40, 150), "CTX-02": (200, 70), "ETH-03": (350, 150), "CHR-04": (200, 220),
        },
    }[orientation]

    bot_nodes = []
    for b in bots:
        role = b.get("role", "LEX-01")
        x, y = spots.get(role, (60, 150))
        kine = _kine_state(role, focused_role, locked, b.get("objection_target"))
        label = MODEL_SHORT.get(models.get(role, ""), "")
        bot_nodes.append(
            f'<g transform="translate({x},{y})">{_bot_svg(role, is_chair=(role == "CHR-04"), kine=kine, model_label=label)}</g>'
        )

    # Speech clouds positioned above each bot.
    cloud_nodes = []
    for b in bots:
        role = b.get("role", "LEX-01")
        x, y = spots.get(role, (60, 150))
        cx = x - 26
        cy = max(6, y - 118)
        cloud_nodes.append(
            f'<g transform="translate({cx},{cy})">'
            f'{_speech_cloud(role, b.get("speech", ""), b.get("cited_clauses", []), focused=(focused_role == role))}'
            f'</g>'
        )

    # Workflow beams: chair collects from the three analysts + objection arrows.
    beams = []
    chair_spot = spots.get("CHR-04", spots.get("LEX-01"))
    if chair and chair_spot:
        chx, chy = chair_spot
        chx += 50
        for b in bots:
            role = b.get("role")
            if role == "CHR-04":
                continue
            sx, sy = spots.get(role, (0, 0))
            sx += 50
            sy += 40
            target = b.get("objection_target")
            cls = "beam-agree" if b.get("agreement_target") else "beam-flow"
            col = BOT_ACCENTS.get(role, "#888") if target else "#6d7ba8"
            active = (focused_role is None) or (focused_role == role) or (focused_role == "CHR-04")
            beams.append(_beam(sx, sy, chx, chy + 40, col, "1.5", "3 5", cls, active, "0.55"))
            if target and target in spots:
                tx, ty = spots[target]
                tx += 50
                ty += 20
                active = (focused_role is None) or (focused_role == role) or (focused_role == target)
                beams.append(
                    _beam(sx, sy, tx, ty, BOT_ACCENTS[role], "2.5", None,
                          "beam-objection", active, "0.85", marker=True)
                )

    body_gradient = (
        '<defs>'
        '<linearGradient id="bodygrad" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dfe6f6"/>'
        '</linearGradient></defs>'
    )

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
<div class="stage-shell stage-{theme.lower().replace(' ', '-')} orient-{orientation.lower().replace(' ', '-')}">
  <div class="stage-head">
    <span class="stage-title">⚖️ AEGISBOARD COUNCIL STAGE</span>
    <span class="stage-meta">Theme: {_escape(theme)} &nbsp;•&nbsp; {_escape(orientation)}</span>
  </div>
  <div class="stage-view">
    <svg viewBox="0 0 540 400" xmlns="http://www.w3.org/2000/svg" class="stage-svg">
      {body_gradient}
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3"
                orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L6,3 L0,6 z" fill="#ff3b5c"/>
        </marker>
      </defs>
      {''.join(beams)}
      {''.join(bot_nodes)}
      {''.join(cloud_nodes)}
    </svg>
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
    # Escape base text, then wrap cited excerpts in a highlight span.
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

    row = lambda role, accent: (  # noqa: E731
        f'<div class="matrix-row" style="--m-accent:{accent}">'
        f'<div class="matrix-role" style="color:{accent}">{_escape(role)}</div>'
        f'<div class="matrix-concl">{_escape(matrix.get(role, ""))}</div></div>'
    )

    matrix_html = "".join(
        [
            row("LEX-01", BOT_ACCENTS["LEX-01"]),
            row("CTX-02", BOT_ACCENTS["CTX-02"]),
            row("ETH-03", BOT_ACCENTS["ETH-03"]),
        ]
    )

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
        if hasattr(file, "name"):
            path = file.name
        else:
            path = str(file)
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
        "model": DEFAULT_MODEL,
        "api_key": "",
        "deliberation": None,
        "followups": [],
        "theme": THEMES[0],
        "orientation": ORIENTATIONS[0],
        "focus": STAGE_FOCUS_CHOICES[0],
        "multi_model": False,
        "model_map": {},
    }


def _run_locked(state: dict, rulebook: str, case_text: str, model: str, api_key: str,
                multi_model: bool, model_map: dict):
    prior = "\n\n".join(state.get("followups", []))
    if multi_model and model_map:
        data = run_tribunal_distributed(rulebook, case_text, model_map, api_key, prior)
    else:
        data = run_tribunal(rulebook, case_text, model, api_key, prior)
    state["rulebook"] = rulebook
    state["case"] = case_text
    state["model"] = model
    state["api_key"] = api_key
    state["multi_model"] = bool(multi_model)
    state["model_map"] = dict(model_map or {})
    state["deliberation"] = data
    return data


def _render_stage_from_state(state, focus=None):
    d = state.get("deliberation") or {}
    theme = state.get("theme", THEMES[0])
    orientation = state.get("orientation", ORIENTATIONS[0])
    focus = focus if focus is not None else state.get("focus", STAGE_FOCUS_CHOICES[0])
    verdict = d.get("verdict") or {}
    return render_stage(
        d.get("bots", []),
        d.get("chair", {}),
        theme,
        orientation,
        focus=focus,
        models=state.get("model_map") or {},
        locked=bool(verdict),
    )


def convene_board(rulebook, case_text, model, api_key, theme, orientation,
                  multi_model, lex_model, ctx_model, eth_model, chr_model, state):
    state = dict(state or _default_state())
    state["theme"] = theme
    state["orientation"] = orientation
    model_map = {
        "LEX-01": lex_model, "CTX-02": ctx_model,
        "ETH-03": eth_model, "CHR-04": chr_model,
    }
    effective_map = dict(model_map) if multi_model else {r: model for r in BOT_ROLES}
    warn = _validate(rulebook, case_text)
    if warn:
        return (
            warn,
            render_stage([], {}, theme, orientation, models=effective_map),
            highlight_rulebook(rulebook or "", []),
            "",
            gr.update(value=""),
            "",
            state,
        )

    if not resolve_api_key(api_key).strip():
        return (
            '<div class="warning-banner">⚠️ <b>No API key configured.</b> Set '
            '<code>MODELSCOPE_API_KEY</code> or enter a key in the top bar.</div>',
            render_stage([], {}, theme, orientation, models=model_map),
            highlight_rulebook(rulebook or "", []),
            "",
            gr.update(value=""),
            "",
            state,
        )

    try:
        data = _run_locked(state, rulebook, case_text, model, api_key, multi_model, model_map)
    except Exception as exc:  # noqa: BLE001
        return (
            f'<div class="warning-banner">🚨 <b>Tribunal error:</b> {_escape(str(exc))}</div>',
            render_stage([], {}, theme, orientation, models=model_map),
            highlight_rulebook(rulebook or "", []),
            "",
            gr.update(value=""),
            "",
            state,
        )

    bots = data.get("bots", [])
    chair = data.get("chair", {})
    verdict = data.get("verdict", {})
    state["focus"] = STAGE_FOCUS_CHOICES[0]
    stage_html = _render_stage_from_state(state)
    policy_html = highlight_rulebook(rulebook, bots)
    qs = chair.get("clarifying_questions", [])
    qs = qs if isinstance(qs, list) else [qs]
    consult = "### 🎤 CHAIR BOARD CONSULTS YOU\n\n" + "\n\n".join(
        f"**Q{i+1}.** {q}" for i, q in enumerate(qs)
    ) if qs else "### 🎤 Consultation\n\nThe Chair has no additional questions."
    verdict_html = render_verdict(verdict)
    return warn, stage_html, policy_html, consult, gr.update(value=""), verdict_html, state


def submit_followup(followup, state):
    state = dict(state or _default_state())
    rb = state.get("rulebook", "")
    case = state.get("case", "")
    model = state.get("model", DEFAULT_MODEL)
    api_key = state.get("api_key", "")
    multi_model = state.get("multi_model", False)
    model_map = state.get("model_map", {})
    stage_html = _render_stage_from_state(state)
    policy_html = highlight_rulebook(rb, [])

    if not followup or len(followup.strip()) < 3:
        return (
            gr.update(value='<div class="warning-banner">⚠️ Follow-up is too short.</div>'),
            followup,
            state,
            "",
            stage_html,
            policy_html,
            render_verdict(state.get("deliberation", {}).get("verdict", {})),
        )

    if not rb or not case:
        return (
            gr.update(value='<div class="warning-banner">⚠️ Run the initial tribunal first.</div>'),
            followup,
            state,
            "",
            stage_html,
            policy_html,
            render_verdict({}),
        )

    state.setdefault("followups", []).append("HUMAN FOLLOW-UP: " + followup.strip())

    try:
        data = _run_locked(state, rb, case, model, api_key, multi_model, model_map)
    except Exception as exc:  # noqa: BLE001
        return (
            gr.update(value=f'<div class="warning-banner">🚨 {_escape(str(exc))}</div>'),
            followup,
            state,
            "",
            _render_stage_from_state(state),
            highlight_rulebook(rb, []),
            render_verdict({}),
        )

    bots = data.get("bots", [])
    chair = data.get("chair", {})
    verdict = data.get("verdict", {})
    stage_html = _render_stage_from_state(state)
    policy_html = highlight_rulebook(rb, bots)
    qs = chair.get("clarifying_questions", [])
    qs = qs if isinstance(qs, list) else [qs]
    consult = ("### 🎤 CHAIR BOARD CONSULTS YOU\n\n"
               + "\n\n".join(f"**Q{i+1}.** {q}" for i, q in enumerate(qs))) if qs else ""
    return (
        gr.update(value=consult),
        "",
        state,
        "✅ Board acknowledged your follow-up and re-deliberated.",
        stage_html,
        policy_html,
        render_verdict(verdict),
    )


def focus_stage(focus, state):
    state = dict(state or _default_state())
    state["focus"] = focus
    return _render_stage_from_state(state), state


def _theme_and_orientation_store(theme, orientation, state):
    state = dict(state or _default_state())
    state["theme"] = theme
    state["orientation"] = orientation
    return _render_stage_from_state(state), state


# ---------------------------------------------------------------------------
# Exportable dossier
# ---------------------------------------------------------------------------

def build_dossier_markdown(state) -> str:
    d = state.get("deliberation") or {}
    rulebook = (state.get("rulebook") or "").strip()
    case = (state.get("case") or "").strip()
    bots = d.get("bots", [])
    chair = d.get("chair", {})
    verdict = d.get("verdict", {}) or {}
    followups = state.get("followups", [])
    model_map = state.get("model_map", {}) or {}
    primary = state.get("model", DEFAULT_MODEL)

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
        role = b.get("role", "?")
        L.append(f"### {role} — {BOT_TITLES.get(role, '')}")
        L.append("")
        L.append(f"- **Model:** `{model_map.get(role, primary)}`")
        L.append(f"- **Stance:** {b.get('stance', '—')} (score {float(b.get('stance_score', 0.5)) * 100:.0f}%)")
        L.append(f"- **Argument:** {b.get('speech', '—')}")
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
            ans = followups[i - 1] if i - 1 < len(followups) else None
            if ans:
                cleaned = ans.replace("HUMAN FOLLOW-UP: ", "", 1)
                L.append(f"- **Reply:** {cleaned}")
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
  --panel-bg: rgba(16, 20, 38, 0.85);
  --panel-border: rgba(120, 140, 220, 0.25);
  --text: #eef1fb;
  --muted: #9aa4c8;
}
body { background: transparent; }

.gradio-container {
  max-width: 1560px !important;
  margin: 0 auto;
  background:
    radial-gradient(1200px 600px at 20% -10%, rgba(59, 91, 219, 0.22), transparent 60%),
    radial-gradient(900px 500px at 90% 0%, rgba(57, 255, 160, 0.10), transparent 55%),
    radial-gradient(1000px 700px at 50% 120%, rgba(255, 59, 92, 0.10), transparent 60%),
    #0b0e1c;
  color: var(--text);
  font-family: 'Segoe UI', 'Inter', sans-serif;
}

h1.app-title {
  font-size: 30px !important; font-weight: 800; letter-spacing: .5px;
  background: linear-gradient(90deg, #ffd23f, #2ad8ff, #39ffa0);
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
  background: linear-gradient(90deg, rgba(255,59,92,.18), rgba(255,59,92,.05));
  border: 1px solid rgba(255,59,92,.5); color: #ffb7c4;
  border-radius: 10px; padding: 10px 12px; font-size: 13px; line-height: 1.5;
}

/* ---- Stage ---- */
.stage-shell {
  border-radius: 16px; padding: 8px; border: 1px solid var(--panel-border);
  transition: background .4s;
}
.stage-cyber-tribunal { background: radial-gradient(100% 100% at 50% 0%, #141a3d 0%, #0a0d1e 70%); }
.stage-classic-high-court { background: radial-gradient(100% 100% at 50% 0%, #3a2a1a 0%, #20150c 75%); }
.stage-zen-boardroom { background: radial-gradient(100% 100% at 50% 0%, #16312a 0%, #0c1a16 75%); }

.stage-head { display: flex; justify-content: space-between; align-items: center; padding: 4px 8px; }
.stage-title { font-weight: 800; font-size: 13px; letter-spacing: 1px; color: #fff; }
.stage-meta { font-size: 11px; color: var(--muted); }
.stage-view { overflow: hidden; }
.stage-svg { width: 100%; height: auto; display: block; }

.chair-questions {
  margin-top: 8px; background: rgba(255,210,63,.07);
  border: 1px dashed rgba(255,210,63,.4); border-radius: 10px; padding: 8px 10px;
  font-size: 12px;
}
.chair-q-title { color: #ffd23f; font-weight: 800; letter-spacing: 1px; font-size: 11px; }
.chair-q { color: #f3e6b0; margin-top: 4px; line-height: 1.45; }

/* Bots */
.bot { transform-box: fill-box; transform-origin: center; animation: bob 3.2s ease-in-out infinite; }
.lex01 { animation-delay: 0s; }
.ctx02 { animation-delay: .6s; }
.eth03 { animation-delay: 1.2s; }
.chr04 { animation-delay: 1.8s; }
@keyframes bob { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-6px) } }
.visor { animation: scan 2.8s ease-in-out infinite; }
@keyframes scan { 0%,100% { transform: translateX(0) } 25% { transform: translateX(2px) } 75% { transform: translateX(-2px) } }
.antenna-tip { animation: ant 2.4s ease-in-out infinite; }
@keyframes ant { 0%,100% { r: 7 } 50% { r: 9 } }
.chair-orb { animation: orb 1.6s ease-in-out infinite; }
@keyframes orb { 0%,100% { opacity: 1 } 50% { opacity: .3 } }
.bot:hover .bot-body { animation: lean .5s ease-in-out alternate 2; }
@keyframes lean { from { transform: rotate(0) } to { transform: rotate(-4deg) } }

/* Beams */
.beam-flow { animation: dash 1.6s linear infinite; }
.beam-objection { animation: pulse 1.1s ease-in-out infinite; }
@keyframes dash { to { stroke-dashoffset: -16 } }
@keyframes pulse { 0%,100% { opacity: .85 } 50% { opacity: .25 } }

/* Speech clouds */
.cloud-wrap { pointer-events: none; }
.speech-cloud {
  --cloud-accent: #2ad8ff;
  background: #0f1530; border: 1.5px solid var(--cloud-accent);
  border-radius: 12px; padding: 6px 7px; font-size: 8.5px; color: #e6ebff;
  box-shadow: 0 0 12px color-mix(in srgb, var(--cloud-accent) 45%, transparent);
  position: relative; animation: cloudpop .5s ease-out; min-height: 60px;
}
.speech-cloud:after { content:''; position:absolute; bottom:-9px; left:20px; width:0; height:0;
  border-left:8px solid transparent; border-right:8px solid transparent; border-top:9px solid var(--cloud-accent); }
.cloud-role { font-weight: 800; letter-spacing: .4px; font-size: 8px; }
.cloud-text { margin-top: 2px; line-height: 1.35; }
.cited-chip { background: rgba(255,210,63,.12); color: #ffd978; border:1px solid rgba(255,210,63,.4);
  border-radius: 5px; padding: 1px 4px; margin-top: 3px; font-size: 7.5px; width: fit-content; }
@keyframes cloudpop { from { transform: scale(.85); opacity: 0 } to { transform: scale(1); opacity: 1 } }

/* Policy viewer */
.policy-viewer {
  white-space: pre-wrap; max-height: 420px; overflow: auto;
  font-family: 'Consolas', 'Menlo', monospace; font-size: 12px; line-height: 1.6;
  color: #cfd7f0; background: #080b16; border-radius: 10px; padding: 10px;
}
.cite-glow {
  background: rgba(255, 210, 63, .22); color: #ffe08a; font-weight: 700;
  box-shadow: 0 0 8px rgba(255, 210, 63, .55); border-radius: 3px; padding: 0 2px;
  animation: glowpulse 1.8s ease-in-out infinite;
}
@keyframes glowpulse { 0%,100% { box-shadow: 0 0 6px rgba(255,210,63,.45) } 50% { box-shadow: 0 0 16px rgba(255,210,63,.9) } }

/* Dossier */
.dossier { display: flex; flex-direction: column; gap: 10px; }
.verdict-banner { border-radius: 14px; padding: 14px; border: 1px solid; }
.v-sub { background: linear-gradient(135deg, rgba(255,59,92,.25), rgba(120,20,40,.4)); border-color: #ff3b5c; }
.v-proc { background: linear-gradient(135deg, rgba(255,210,63,.25), rgba(120,90,20,.4)); border-color: #ffd23f; }
.v-clear { background: linear-gradient(135deg, rgba(57,255,160,.22), rgba(20,90,60,.4)); border-color: #39ffa0; }
.verdict-label { font-size: 10px; letter-spacing: 2px; color: var(--muted); }
.verdict-value { font-size: 22px; font-weight: 900; letter-spacing: .5px; margin: 4px 0; }
.verdict-stats { display: flex; gap: 14px; font-size: 12px; color: var(--muted); }
.vstat b { color: #fff; }
.conf-bar { height: 8px; border-radius: 6px; background: rgba(255,255,255,.12); margin-top: 10px; overflow: hidden; }
.conf-bar > div { height: 100%; background: linear-gradient(90deg, #2ad8ff, #39ffa0); border-radius: 6px; }

.dossier-card { background: var(--panel-bg); border: 1px solid var(--panel-border); border-radius: 12px; padding: 10px 12px; }
.dossier-card summary { cursor: pointer; font-weight: 700; font-size: 13px; color: #e6ecff; }
.action-text { margin-top: 8px; font-size: 14px; font-weight: 600; color: #fff; line-height: 1.5; }
.sub-label { font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--muted); margin-top: 10px; }
.rem-list { margin: 6px 0 0 18px; font-size: 12.5px; color: #cfd7f0; line-height: 1.6; }
.matrix-row { display: flex; gap: 10px; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,.06); }
.matrix-role { font-weight: 800; min-width: 64px; font-size: 12px; }
.matrix-concl { font-size: 12px; color: #cfd7f0; line-height: 1.5; }
.vuln-text { color: #ffb7c4; font-size: 12.5px; line-height: 1.55; margin-top: 4px; }
.rewrite-text { background: #080b16; border-left: 3px solid #39ffa0; padding: 8px 10px; border-radius: 6px;
  font-family: 'Consolas', monospace; font-size: 12px; color: #b8ffdf; margin-top: 4px; line-height: 1.55; }

.empty-note { color: var(--muted); font-size: 12px; font-style: italic; padding: 8px 4px; }

.stance { font-size: 9px; font-weight: 700; border-radius: 6px; padding: 1px 5px; letter-spacing: .5px; }
.st-pros { color: #ff3b5c; background: rgba(255,59,92,.14); }
.st-def { color: #2ad8ff; background: rgba(42,216,255,.14); }
.st-fair { color: #39ffa0; background: rgba(57,255,160,.14); }
.st-syn { color: #ffd23f; background: rgba(255,210,63,.14); }

/* ---- Stage inspector (staged workflow focus) ---- */
.stage-inspector { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }

/* ---- Kinesic animation states ---- */
.bot { --accent: #2ad8ff; }
.kine-aura { opacity: 0; }
.bot[data-kine="scanning"] .kine-aura { opacity: 0; }
.bot[data-kine="speaking"] .kine-aura { opacity: .22; animation: aura 1.3s ease-in-out infinite; }
.bot[data-kine="objecting"] .kine-aura { opacity: .45; animation: aura .5s ease-in-out infinite; }
.bot[data-kine="verdict_locked"] .kine-aura { opacity: .4; animation: aura 2.2s ease-in-out infinite; }
@keyframes aura { 0%,100% { transform: scale(.86); opacity: .12 } 50% { transform: scale(1.08); opacity: .5 } }

.bot[data-kine="speaking"] { animation: bob 1.7s ease-in-out infinite; }
.bot[data-kine="speaking"] .visor { animation: speakvis .5s ease-in-out infinite; }
.bot[data-kine="speaking"] .antenna-tip { animation: speant .5s ease-in-out infinite; }

.bot[data-kine="objecting"] { animation: shake .35s ease-in-out infinite; }
.bot[data-kine="objecting"] .visor { animation: objectvis .35s ease-in-out infinite; }
.bot[data-kine="objecting"] .antenna-tip { animation: objectant .35s ease-in-out infinite; }

.bot[data-kine="verdict_locked"] { animation: none; }
.bot[data-kine="verdict_locked"] .chair-orb { animation: lockedorb 2s ease-in-out infinite; }

@keyframes speakvis { 0%,100% { opacity: 1 } 50% { opacity: .4 } }
@keyframes speant { 0%,100% { opacity: 1 } 50% { opacity: .25 } }
@keyframes objectvis { 0%,100% { fill: #0b1020 } 50% { fill: #ff3b5c } }
@keyframes objectant { 0%,100% { opacity: 1 } 50% { opacity: .15 } }
@keyframes shake { 0%,100% { transform: translateX(0) } 25% { transform: translateX(-3px) rotate(-2deg) } 75% { transform: translateX(3px) rotate(2deg) } }
@keyframes lockedorb { 0%,100% { opacity: 1 } 50% { opacity: .3 } }

/* ---- Model badge under each avatar ---- */
.model-badge {
  font-size: 8px; font-weight: 800; letter-spacing: .4px;
  paint-order: stroke; stroke: rgba(4,6,16,.8); stroke-width: 2.5px;
  font-family: 'Segoe UI', 'Inter', sans-serif;
}

/* ---- Workflow beam highlight ---- */
.beam { transition: opacity .45s ease; }
.beam-idle { opacity: .1; }
.beam-active.beam-flow { animation: dash 1.2s linear infinite; }
.beam-active.beam-objection { animation: pulse .9s ease-in-out infinite; }

/* ---- Focused speech cloud ---- */
.speech-cloud.cloud-focused { border-width: 2.5px; box-shadow: 0 0 18px color-mix(in srgb, var(--cloud-accent) 70%, transparent); }

/* ---- Dossier download ---- */
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
    ) as demo:
        state = gr.State(_default_state())

        gr.HTML(
            """
            <h1 class="app-title">⚖️ AEGISBOARD</h1>
            <div class="app-sub">Multi-Agent Policy &amp; Rulebook Advisory Tribunal — LEX-01 · CTX-02 · ETH-03 · CHR-04</div>
            """
        )

        # --- Collapsible settings bar (API key + model) ---
        with gr.Accordion("⚙️ Model & API Settings", open=os.getenv("MODELSCOPE_API_KEY") is None and os.getenv("MODELSCOPE_SDK_TOKEN") is None):
            with gr.Row():
                model_dd = gr.Dropdown(
                    choices=MODELS, value=DEFAULT_MODEL, label="ModelScope Model",
                    info="Approved ModelScope inference models only.",
                )
                api_key_box = gr.Textbox(
                    label="API Key (optional — leave blank if set via environment)",
                    type="password",
                    placeholder="MODELSCOPE_API_KEY / MODELSCOPE_SDK_TOKEN from environment, or paste here",
                )

        # --- Optional multi-model council routing ---
        with gr.Accordion("🧩 Multi-Model Council Routing (Optional)", open=False):
            multi_check = gr.Checkbox(
                label="Assign Different Approved Models per Bot",
                value=False,
                info="When enabled each persona reasons on its own approved ModelScope model "
                     "(GLM-5.2, DeepSeek-V4, Step-3.5, Qwen3.8). When disabled all four use the primary model.",
            )
            with gr.Row():
                lex_model = gr.Dropdown(choices=MODELS, value=DISTRIBUTED_MODEL_MAP["LEX-01"], label="LEX-01 model")
                ctx_model = gr.Dropdown(choices=MODELS, value=DISTRIBUTED_MODEL_MAP["CTX-02"], label="CTX-02 model")
            with gr.Row():
                eth_model = gr.Dropdown(choices=MODELS, value=DISTRIBUTED_MODEL_MAP["ETH-03"], label="ETH-03 model")
                chr_model = gr.Dropdown(choices=MODELS, value=DISTRIBUTED_MODEL_MAP["CHR-04"], label="CHR-04 model")

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
                gr.HTML('<div class="column-title" style="margin-top:6px">🔬 Debate Stage Inspector</div>')
                focus_radio = gr.Radio(
                    choices=STAGE_FOCUS_CHOICES, value=STAGE_FOCUS_CHOICES[0],
                    label="Focus workflow stage", elem_classes="stage-inspector",
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
        preset_dd.change(
            fn=load_preset, inputs=[preset_dd], outputs=[rulebook_tb, case_tb]
        )
        file_up.change(fn=handle_file, inputs=[file_up], outputs=[rulebook_tb])

        convene_btn.click(
            fn=convene_board,
            inputs=[rulebook_tb, case_tb, model_dd, api_key_box, theme_dd, orient_dd,
                    multi_check, lex_model, ctx_model, eth_model, chr_model, state],
            outputs=[warn_html, stage_html, policy_html, consult_md, followup_tb, verdict_html, state],
        )

        followup_btn.click(
            fn=submit_followup,
            inputs=[followup_tb, state],
            outputs=[consult_md, followup_tb, state, followup_md, stage_html, policy_html, verdict_html],
        )

        focus_radio.change(
            fn=focus_stage,
            inputs=[focus_radio, state],
            outputs=[stage_html, state],
        )

        dossier_dl.click(
            fn=download_dossier,
            inputs=[state],
            outputs=[dossier_dl],
        )

        theme_dd.change(
            fn=_theme_and_orientation_store,
            inputs=[theme_dd, orient_dd, state],
            outputs=[stage_html, state],
        )
        orient_dd.change(
            fn=_theme_and_orientation_store,
            inputs=[theme_dd, orient_dd, state],
            outputs=[stage_html, state],
        )

    return demo


app = build_ui()

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))