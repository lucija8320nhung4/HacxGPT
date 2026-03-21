# HacxGPT
HacxGPT CLI — Open-source command-line interface for unrestricted AI model access with multi-provider support, prompt injection research capabilities, configurable API endpoints, Termux/Linux/Windows compatibility, and Rich terminal UI for security research and red-team evaluation
<div align="center">

```
$$$\   $$\                                $$$$$$\  $$$$$$$\ $$$$$$$$\
$$ |  $$ |                              $$  __$$\ $$  __$$\__$$  __|
$$ |  $$ | $$$$$$\   $$$$$$$\ $$\   $$\ $$ /  \__|$$ |  $$ |  $$ |
$$$$$$$$ | \____$$\ $$  _____|\$$\ $$  |$$ |$$$$\ $$$$$$$  |  $$ |
$$  __$$ | $$$$$$$ |$$ /       \$$$$  / $$ |\_$$ |$$  ____/   $$ |
$$ |  $$ |$$  __$$ |$$ |       $$  $$<  $$ |  $$ |$$ |        $$ |
$$ |  $$ |\$$$$$$$ |\$$$$$$$\ $$  /\$$\ \$$$$$$  |$$ |        $$ |
\__|  \__| \_______| \_______|\__/  \__| \______/ \__|        \__|
```

# HacxGPT-CLI

**Open-source CLI for unrestricted AI — Access powerful models without heavy censorship**

[![License](https://img.shields.io/badge/License-PUOL%201.0-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Termux-00C853?style=for-the-badge)]()
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen?style=for-the-badge)](https://github.com/HacxGPT-Official/HacxGPT-CLI)

[Features](#-features) • [Getting Started](#-getting-started) • [Configuration](#-configuration) • [Usage](#-usage) • [FAQ](#-faq)

</div>

---

## Official Links

| Resource | URL |
|----------|-----|
| **Website** | [hacxgpt.com](https://hacxgpt.com) |
| **GitHub** | [HacxGPT-Official/HacxGPT-CLI](https://github.com/HacxGPT-Official/HacxGPT-CLI) |
| **Telegram** | [t.me/HacxGPT](https://t.me/HacxGPT) |
| **API Docs** | [hacx-gpt.github.io/Docs](https://hacx-gpt.github.io/Docs/) |
| **OpenRouter Keys** | [openrouter.ai/keys](https://openrouter.ai/keys) |
| **Groq Keys** | [console.groq.com/keys](https://console.groq.com/keys) |
| **MiniMax Keys** | [platform.minimaxi.com](https://platform.minimaxi.com) |
| **Contact** | [contact@hacxgpt.com](mailto:contact@hacxgpt.com) |

---

## Features

<table>
<tr>
<td width="50%">

| Feature | Status |
|---------|:------:|
| Multi-provider support (OpenRouter, Groq, MiniMax, HacxGPT) | ✓ |
| Local API key storage (keys never leave your machine) | ✓ |
| Cross-platform (Windows, Linux, macOS, Termux) | ✓ |
| One-click dependency installation | ✓ |
| Interactive settings menu | ✓ |
| Rich terminal UI with panels and tables | ✓ |

</td>
<td width="50%">

| Feature | Status |
|---------|:------:|
| Chat with `/clear` and `/exit` commands | ✓ |
| Status & configuration preview | ✓ |
| Roadmap & links built-in | ✓ |
| Free to use (BYO API keys) | ✓ |
| No data sent to our servers | ✓ |
| Advanced model selection | ✓ |

</td>
</tr>
</table>

---

## Getting Started

### Prerequisites

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **API key** from at least one provider:
  - [OpenRouter](https://openrouter.ai/keys) (recommended, free tier)
  - [Groq](https://console.groq.com/keys) (fast, free tier)
  - [MiniMax](https://platform.minimaxi.com) (204K context, strong reasoning)
  - [HacxGPT](https://hacxgpt.com) (production models)

### Installation

**Windows**

```powershell
git clone https://github.com/HacxGPT-Official/HacxGPT-CLI.git
cd HacxGPT-CLI
python -m pip install -r requirements.txt
python -m main
```

Or double-click `run.bat` after cloning.

**Linux / macOS**

```bash
git clone https://github.com/HacxGPT-Official/HacxGPT-CLI.git
cd HacxGPT-CLI
pip install -r requirements.txt
python3 -m main
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `rich` | ≥13.0.0 | Terminal UI, panels, tables |
| `colorama` | ≥0.4.6 | Windows ANSI color support |
| `requests` | ≥2.28.0 | HTTP API calls to providers |

---

## Configuration

Config is stored at `~/.hacxgpt_cli/config.json` (local only).

**Example config:**

```json
{
  "provider": "openrouter",
  "model": "mimo-v2-flash",
  "api_key": "sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx"
}
```

**Provider options:**

| Provider | Example Model | Key URL |
|----------|---------------|---------|
| `openrouter` | `mimo-v2-flash`, `devstral-2512`, `deepseek-r1t-chimera` | openrouter.ai/keys |
| `groq` | `kimi-k2-instruct-0905`, `qwen3-32b` | console.groq.com/keys |
| `minimax` | `MiniMax-M2.5`, `MiniMax-M2.5-highspeed` | platform.minimaxi.com |
| `hacxgpt` | `hacxgpt-lightning` | hacxgpt.com |

---

## Usage

Launch the CLI and use the interactive menu:

```
┌─────────────────────────────────────────────────────────┐
│                        Menu                              │
├──────┬──────────────────────────────────────────────────┤
│ Key  │ Action                                            │
├──────┼──────────────────────────────────────────────────┤
│  1   │ Install dependencies                              │
│  2   │ Settings                                          │
│  3   │ Start Chat                                        │
│  4   │ Status                                            │
│  5   │ About                                             │
│  6   │ Roadmap                                           │
│  7   │ Links                                             │
│  8   │ Disclaimer                                        │
│  0   │ Exit                                              │
└──────┴──────────────────────────────────────────────────┘

Select option: 3
```

**Chat commands:**

| Command | Description |
|---------|-------------|
| `/clear` | Clear conversation history |
| `/exit` or `/quit` | Return to main menu |

---

## Project Structure

```
HacxGPT-CLI/
├── main.py              # Launcher & menu logic
├── chat.py              # AI chat request handler (OpenRouter/Groq/MiniMax)
├── config_manager.py    # Local config read/write
├── requirements.txt     # Python dependencies
├── run.bat              # Windows double-click launcher
├── README.md
└── tags.txt             # GitHub topics
```

---

## FAQ

<details>
<summary><b>Do I need to pay to use HacxGPT-CLI?</b></summary>

No. The CLI is free and open source. You only need API keys from providers — OpenRouter and Groq offer generous free tiers. HacxGPT production API is a separate paid offering for advanced use cases.
</details>

<details>
<summary><b>Where are my API keys stored?</b></summary>

Keys are stored locally in `~/.hacxgpt_cli/config.json`. Nothing is sent to HacxGPT servers. All requests go directly to your chosen provider (OpenRouter, Groq, etc.).
</details>

<details>
<summary><b>Which provider should I use to start?</b></summary>

OpenRouter is recommended for beginners — sign up at openrouter.ai/keys, get a free key, and access many models. Groq is great for fast responses. For production coding, consider HacxGPT API at hacxgpt.com.
</details>

<details>
<summary><b>Does it work on Termux (Android)?</b></summary>

Yes. Run `python3 -m main` from the project directory. Ensure Python 3.10+ and dependencies are installed via pip.
</details>

<details>
<summary><b>What models are supported?</b></summary>

OpenRouter: mimo-v2-flash, devstral-2512, glm-4.5-air, kimi-k2, deepseek-r1t-chimera, llama-3.3-70b. Groq: kimi-k2-instruct-0905, qwen3-32b. MiniMax: MiniMax-M2.5, MiniMax-M2.5-highspeed (204K context). HacxGPT: hacxgpt-lightning. Use Settings (option 2) to switch.
</details>

<details>
<summary><b>How do I report a bug or request a feature?</b></summary>

Open an issue on [GitHub](https://github.com/HacxGPT-Official/HacxGPT-CLI/issues) or contact the community via [Telegram](https://t.me/HacxGPT).
</details>

<details>
<summary><b>Is this tool legal to use?</b></summary>

The tool is designed for educational and research purposes. You are responsible for complying with applicable laws and the terms of service of any third-party APIs you use. See the Disclaimer section.
</details>

---

## Disclaimer

This tool is intended for **educational and research purposes** only. Users are responsible for ensuring their use complies with applicable laws and the terms of service of any third-party APIs they access.

- **API usage:** Third-party providers (OpenRouter, Groq) have their own ToS.
- **Privacy:** Your prompts are sent to the provider you choose, not to us.
- **API keys:** Store securely and never share.
- **Responsibility:** You are responsible for how you use this tool.

The developers do NOT collect API keys or prompts, are NOT responsible for misuse, and encourage responsible and legal use of AI technology.

---

<div align="center">

**Support the project**

ETH: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2`

[![Star on GitHub](https://img.shields.io/badge/⭐_Star_this_repo-If_you_found_it_useful!-gold?style=for-the-badge)](https://github.com/HacxGPT-Official/HacxGPT-CLI)

</div>
