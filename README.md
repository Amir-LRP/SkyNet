# SKYNET — Autonomous AI Operating System

> Next-generation voice + text AI assistant powered by Gemini Live  
> Built for real computer control, autonomous execution, and bilingual (Persian/English) intelligence

---

## ⚡ Features

| Category | Capabilities |
|---|---|
| 🎙 Voice | Real-time streaming via Gemini 2.5 Flash Live |
| 👁 Vision | Screen capture & webcam analysis |
| 🖥 Control | Mouse, keyboard, system & window automation |
| 🌐 Browser | Playwright-based automation (Chrome, Firefox, Edge) |
| 📁 Files | Create, move, delete, search & organize |
| 🤖 Agents | Multi-step planning, execution & replanning |
| 🧠 Memory | Persistent long-term memory across sessions |
| 🛠 Dev Agent | Auto project scaffolding |
| 🇮🇷 Persian | Full native Farsi + RTL support |
| 💬 Messaging | Telegram & WhatsApp automation |
| ▶️ YouTube | Play, summarize, trends |
| ✈️ Travel | Google Flights search |
| 🎮 Gaming | Steam & Epic Games management |
| 📦 Processing | Images, PDFs, audio, video, code, spreadsheets |

---

## 📦 Requirements

- Python 3.11+
- Gemini API key (free tier supported)
- Windows / macOS / Linux

---

## 🚀 Installation

```bash
git clone [<repo>](https://github.com/Amir-LRP/SkyNet.git)
cd SKYNET

python setup.py
python main.py
```

On first run, SKYNET will prompt for your API key and OS configuration.

---

## 🎯 Usage

| Method | Action |
|---|---|
| 🎙 Voice | Speak naturally |
| ⌨️ Text | Type command + Enter |
| 📂 Files | Drag & drop |
| 🔇 Mute | F4 |
| 🖥 Fullscreen | F11 |

---

## 🇮🇷 Persian Support

- Auto language detection (FA/EN)
- RTL rendering
- Persian memory storage
- Native response generation
- Persian file handling

---

## 🧠 Architecture

```
User (voice/text)
      ↓
Skynet Runtime (main.py)
      ↓
Gemini Live Session
      ↓
Tool Dispatcher
      ↓
┌───────────────┐
│ Tools / Agents│
│ Planner       │
│ Executor      │
│ Memory        │
└───────────────┘
      ↓
Memory Store (persistent)
```

---

## ⚙️ Configuration

```json
{
  "gemini_api_key": "YOUR_KEY",
  "os_system": "windows"
}
```

Delete file to reset setup.

---

## ⌨️ Shortcuts

| Key | Action |
|---|---|
| F4 | Mute / Unmute |
| F11 | Fullscreen |
| Enter | Send input |

---

## 🧩 Troubleshooting

**🎙 Microphone not working**
→ Check OS permissions

**🌐 Playwright issues**
```bash
python -m playwright install
```

**🔑 API errors**
→ Reset `config/api_keys.json`

**🖥 GPU N/A**
→ Normal if no GPU is available

---

## 🛰 SKYNET

Autonomous AI system for real-world computer control, automation, and intelligent task execution.
```
