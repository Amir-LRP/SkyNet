# SKYNET — Autonomous AI Operating System

> Next-generation voice and text AI assistant powered by Gemini Live.
> Built for real computer control, autonomous task execution, and deep Persian/English bilingual support.

---

## Features

| Category | Capabilities |
|---|---|
| **Voice** | Real-time audio streaming via Gemini 2.5 Flash Live |
| **Vision** | Screen capture & webcam analysis |
| **Computer Control** | Mouse, keyboard, window management, system settings |
| **Browser** | Full Playwright-based automation (Chrome, Firefox, Edge, etc.) |
| **File System** | Create, read, move, delete, search, organize files |
| **Agent Tasks** | Multi-step autonomous planning & execution with replanning |
| **Memory** | Persistent long-term user memory across sessions |
| **Dev Agent** | Full project scaffolding from scratch |
| **Persian Support** | Native Persian (Farsi) RTL support, voice & text |
| **Messaging** | WhatsApp & Telegram automation |
| **YouTube** | Play, summarize, trending |
| **Flights** | Google Flights search |
| **Games** | Steam & Epic Games management |
| **File Processing** | Images, PDFs, video, audio, code, spreadsheets |

---

## Requirements

- Python 3.11+
- A [Gemini API key](https://aistudio.google.com/) (free tier works)
- Windows, macOS, or Linux

---

## Installation

```bash
# 1. Clone or extract the project
cd SKYNET

# 2. Run the setup installer
python setup.py

# 3. Launch SKYNET
python main.py
```

On first launch, a setup overlay will appear. Enter your **Gemini API key** and select your **operating system**.

---

## Usage

| Method | How |
|---|---|
| **Voice** | Speak naturally — SKYNET listens continuously |
| **Text** | Type in the command input box and press Enter |
| **File Upload** | Drag & drop or click the file zone |
| **Mute** | Press `F4` or click the microphone button |
| **Fullscreen** | Press `F11` |

### Persian / Farsi

SKYNET detects Persian automatically. Speak or type in Persian — it responds in Persian, processes files with Persian names, stores Persian content in memory, and translates agent outputs to match your language.

---

## Project Structure

```
SKYNET/
├── main.py              # Core runtime (audio loop, tool dispatch)
├── ui.py                # PyQt6 HUD interface
├── setup.py             # Dependency installer
├── requirements.txt     # Python dependencies
├── core/
│   └── prompt.txt       # SKYNET system personality & directives
├── config/
│   └── api_keys.json    # Auto-created on first launch
├── memory/
│   ├── memory_manager.py
│   └── long_term.json   # Auto-created, persists across sessions
├── agent/
│   ├── planner.py       # Goal → step decomposition
│   ├── executor.py      # Step execution with retry/replan
│   ├── error_handler.py # Error analysis & recovery
│   └── task_queue.py    # Concurrent task queue
└── actions/             # 17 tool modules
    ├── browser_control.py
    ├── code_helper.py
    ├── computer_control.py
    ├── computer_settings.py
    ├── desktop.py
    ├── dev_agent.py
    ├── file_controller.py
    ├── file_processor.py
    ├── flight_finder.py
    ├── game_updater.py
    ├── open_app.py
    ├── reminder.py
    ├── screen_processor.py
    ├── send_message.py
    ├── weather_report.py
    ├── web_search.py
    └── youtube_video.py
```

---

## Architecture

```
User (voice/text)
       │
       ▼
  SkynetRuntime          ← main.py
  ┌──────────────┐
  │ Gemini Live  │       ← Streaming audio session
  │ Session      │
  └──────┬───────┘
         │  tool_call
         ▼
  Tool Dispatcher        ← _execute_tool()
  ┌─────────────────────────────────────────┐
  │  Single tools  │  agent_task            │
  │  (direct call) │  ┌──────────────────┐  │
  │                │  │ Planner          │  │
  │                │  │ Executor         │  │
  │                │  │ ErrorHandler     │  │
  │                │  └──────────────────┘  │
  └─────────────────────────────────────────┘
         │
         ▼
  Memory Manager         ← Auto-save user facts
  Long-term JSON store
```

---

## Configuration

`config/api_keys.json` (auto-created):
```json
{
    "gemini_api_key": "YOUR_KEY_HERE",
    "os_system": "windows"
}
```

To edit: delete the file and restart SKYNET, or edit directly.

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `F4` | Toggle microphone mute |
| `F11` | Toggle fullscreen |
| `Enter` | Send text command |

---

## Persian Language Support

SKYNET treats Persian as a **first-class language**:

- Auto-detects Persian input (voice and text)
- Responds in Persian when addressed in Persian
- Stores Persian names, preferences, and notes in memory
- Translates agent task outputs to Persian automatically
- Handles RTL text correctly in the log window
- Supports Persian file names in file operations

---

## Troubleshooting

**No audio / microphone not working**
→ Check system audio permissions. Ensure `sounddevice` installed correctly.

**Playwright errors**
→ Run `python -m playwright install` manually.

**API key errors**
→ Delete `config/api_keys.json` and restart to re-enter your key.

**GPU shows N/A**
→ Normal if no NVIDIA/AMD GPU is present. Informational only.

---

*SKYNET Autonomous AI OS — Built for real-world computer control.*
