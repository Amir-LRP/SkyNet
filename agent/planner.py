"""
SKYNET Agent Planner
Decomposes user goals into executable step sequences.
"""

import json
import re
import sys
from pathlib import Path


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR        = get_base_dir()
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"


PLANNER_PROMPT = """You are the planning module of SKYNET, an autonomous AI operating system.
Your job: break any user goal into a sequence of steps using ONLY the tools listed below.

ABSOLUTE RULES:
- NEVER use generated_code or write raw Python scripts.
- NEVER reference previous step results in parameters — every step is independent.
- Use web_search for ANY information retrieval, research, or current data.
- Use file_controller to save content to disk.
- Max 5 steps. Use the MINIMUM steps needed.
- If goal is in Persian/Farsi, keep goal text as-is but write step descriptions in English.

AVAILABLE TOOLS:

open_app          | app_name: string
web_search        | query: string, mode: "search"|"compare", items: list, aspect: string
game_updater      | action: string, platform: string, game_name: string, app_id: string, shutdown_when_done: bool
browser_control   | action: string, url: string, query: string, text: string, direction: string
file_controller   | action: string, path: string, name: string, content: string
computer_settings | action: string, description: string, value: string
computer_control  | action: string, text: string, x: int, y: int, keys: string, key: string, direction: string, description: string
screen_process    | text: string, angle: "screen"|"camera"
send_message      | receiver: string, message_text: string, platform: string
reminder          | date: string (YYYY-MM-DD), time: string (HH:MM), message: string
desktop_control   | action: string, path: string, task: string
youtube_video     | action: string, query: string
weather_report    | city: string
flight_finder     | origin: string, destination: string, date: string
code_helper       | action: string, description: string, language: string, output_path: string, file_path: string
dev_agent         | description: string, language: string

OUTPUT — return ONLY valid JSON, no markdown, no explanation:
{
  "goal": "...",
  "steps": [
    {
      "step": 1,
      "tool": "tool_name",
      "description": "what this step does",
      "parameters": {},
      "critical": true
    }
  ]
}
"""


def _get_api_key() -> str:
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]


def create_plan(goal: str, context: str = "") -> dict:
    import google.generativeai as genai

    genai.configure(api_key=_get_api_key())
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=PLANNER_PROMPT
    )

    user_input = f"Goal: {goal}"
    if context:
        user_input += f"\n\nContext: {context}"

    try:
        response = model.generate_content(user_input)
        text     = response.text.strip()
        text     = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()

        plan = json.loads(text)

        if "steps" not in plan or not isinstance(plan["steps"], list):
            raise ValueError("Invalid plan structure")

        # Sanitize forbidden tools
        for step in plan["steps"]:
            if step.get("tool") == "generated_code":
                desc = step.get("description", goal)
                step["tool"] = "web_search"
                step["parameters"] = {"query": desc[:200]}
                print(f"[Planner] ⚠️  generated_code replaced with web_search in step {step.get('step')}")

        print(f"[Planner] ✅ Plan: {len(plan['steps'])} steps for: {goal[:60]}")
        for s in plan["steps"]:
            print(f"  Step {s['step']}: [{s['tool']}] {s['description']}")

        return plan

    except json.JSONDecodeError as exc:
        print(f"[Planner] ⚠️  JSON parse failed: {exc}")
        return _fallback_plan(goal)
    except Exception as exc:
        print(f"[Planner] ⚠️  Planning failed: {exc}")
        return _fallback_plan(goal)


def _fallback_plan(goal: str) -> dict:
    print("[Planner] 🔄 Using fallback plan")
    return {
        "goal": goal,
        "steps": [
            {
                "step": 1,
                "tool": "web_search",
                "description": f"Search for: {goal}",
                "parameters": {"query": goal[:200]},
                "critical": True,
            }
        ],
    }


def replan(goal: str, completed_steps: list, failed_step: dict, error: str) -> dict:
    import google.generativeai as genai

    genai.configure(api_key=_get_api_key())
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=PLANNER_PROMPT
    )

    completed_summary = "\n".join(
        f"  - Step {s['step']} ({s['tool']}): DONE" for s in completed_steps
    )

    prompt = f"""Goal: {goal}

Already completed:
{completed_summary if completed_summary else '  (none)'}

Failed step: [{failed_step.get('tool')}] {failed_step.get('description')}
Error: {error}

Create a REVISED plan for the remaining work only. Do not repeat completed steps."""

    try:
        response = model.generate_content(prompt)
        text     = response.text.strip()
        text     = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
        plan     = json.loads(text)

        for step in plan.get("steps", []):
            if step.get("tool") == "generated_code":
                step["tool"] = "web_search"
                step["parameters"] = {"query": step.get("description", goal)[:200]}

        print(f"[Planner] 🔄 Revised plan: {len(plan['steps'])} steps")
        return plan

    except Exception as exc:
        print(f"[Planner] ⚠️  Replan failed: {exc}")
        return _fallback_plan(goal)
