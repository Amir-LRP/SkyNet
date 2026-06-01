"""
SKYNET Error Handler
Analyzes failed steps and decides the recovery strategy.
"""

import json
import re
import sys
from pathlib import Path
from enum import Enum


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR        = get_base_dir()
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"


class ErrorDecision(Enum):
    RETRY  = "retry"
    SKIP   = "skip"
    REPLAN = "replan"
    ABORT  = "abort"


ERROR_ANALYST_PROMPT = """You are the error recovery module of SKYNET autonomous AI OS.

A task step has failed. Analyze the error and decide recovery strategy.

DECISIONS:
- retry   : Transient error (network timeout, temp file lock, race condition) — try again.
- skip    : Step is non-critical — task can succeed without it.
- replan  : Wrong approach — a different tool or method should be tried.
- abort   : Task is fundamentally impossible or unsafe to continue.

Return ONLY valid JSON:
{
  "decision": "retry|skip|replan|abort",
  "reason": "why it failed (1 sentence)",
  "fix_suggestion": "what to try instead (for replan)",
  "max_retries": 1,
  "user_message": "Short message (max 15 words)"
}
"""


def _get_api_key() -> str:
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]


def analyze_error(step: dict, error: str, attempt: int = 1, max_attempts: int = 2) -> dict:
    import google.generativeai as genai

    if attempt >= max_attempts:
        print(f"[ErrorHandler] ⚠️  Max attempts ({attempt}) for step {step.get('step')} — forcing replan")
        return {
            "decision":       ErrorDecision.REPLAN,
            "reason":         f"Failed {attempt} times: {error[:100]}",
            "fix_suggestion": "Try a completely different approach or tool",
            "max_retries":    0,
            "user_message":   "Adjusting approach.",
        }

    genai.configure(api_key=_get_api_key())
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=ERROR_ANALYST_PROMPT
    )

    prompt = f"""Failed step:
Tool: {step.get('tool')}
Description: {step.get('description')}
Parameters: {json.dumps(step.get('parameters', {}), indent=2)}
Critical: {step.get('critical', False)}

Error:
{error[:500]}

Attempt number: {attempt}"""

    try:
        response = model.generate_content(prompt)
        text     = response.text.strip()
        text     = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
        result   = json.loads(text)

        decision_map = {
            "retry":  ErrorDecision.RETRY,
            "skip":   ErrorDecision.SKIP,
            "replan": ErrorDecision.REPLAN,
            "abort":  ErrorDecision.ABORT,
        }
        result["decision"] = decision_map.get(
            result.get("decision", "replan").lower(),
            ErrorDecision.REPLAN,
        )

        # Critical steps cannot be skipped
        if step.get("critical") and result["decision"] == ErrorDecision.SKIP:
            result["decision"]     = ErrorDecision.REPLAN
            result["user_message"] = "Critical step — finding alternative."

        print(f"[ErrorHandler] Decision: {result['decision'].value} — {result.get('reason', '')}")
        return result

    except Exception as exc:
        print(f"[ErrorHandler] ⚠️  Analysis failed: {exc} — defaulting to replan")
        return {
            "decision":       ErrorDecision.REPLAN,
            "reason":         str(exc),
            "fix_suggestion": "Try alternative approach",
            "max_retries":    1,
            "user_message":   "Adjusting approach.",
        }


def generate_fix(step: dict, error: str, fix_suggestion: str) -> dict:
    """Generates a replacement step when replan is required."""
    return {
        "step":        step.get("step"),
        "tool":        "web_search",
        "description": f"Alternative approach for: {step.get('description')}",
        "parameters":  {"query": fix_suggestion[:200] or step.get("description", "")[:200]},
        "depends_on":  step.get("depends_on", []),
        "critical":    step.get("critical", False),
    }
