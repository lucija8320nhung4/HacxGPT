"""
HacxGPT-CLI Launcher - Rich console interface.
Open-source CLI for unrestricted AI. Tables, panels, borders. All text in English.
"""
import os
import subprocess
import sys

if sys.platform == "win32":
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from rich.style import Style

from config_manager import get_config, save_config, PROVIDERS, get_models_for_provider
from utils import ensure_env

console = Console(force_terminal=True)

# Theme: green terminal style
STYLE_TITLE = Style(color="green", bold=True)
STYLE_ACCENT = Style(color="green")
STYLE_DIM = Style(dim=True)
STYLE_OK = Style(color="green")
STYLE_ERR = Style(color="red")
BOX_STYLE = box.ROUNDED  # or box.DOUBLE, box.HEAVY

LOGO = r"""$$\   $$\                                $$$$$$\  $$$$$$$\ $$$$$$$$\
$$ |  $$ |                              $$  __$$\ $$  __$$\__$$  __|
$$ |  $$ | $$$$$$\   $$$$$$$\ $$\   $$\ $$ /  \__|$$ |  $$ |  $$ |\
$$$$$$$$ | \____$$\ $$  _____|\$$\ $$  |$$ |$$$$\ $$$$$$$  |  $$ |\
$$  __$$ | $$$$$$$ |$$ /       \$$$$  / $$ |\_$$ |$$  ____/   $$ |\
$$ |  $$ |$$  __$$ |$$ |       $$  $$<  $$ |  $$ |$$ |        $$ |\
$$ |  $$ |\$$$$$$$ |\$$$$$$$\ $$  /\$$\ \$$$$$$  |$$ |        $$ |\
\__|  \__| \_______| \_______|\__/  \__| \______/ \__|        \__|"""


def clear_screen():
    os.system("cls" if sys.platform == "win32" else "clear")


def draw_header():
    """Rich header: logo in panel + rule."""
    logo_text = Text(LOGO, style="green")
    subtitle = Text("Open-source CLI for unrestricted AI", style="green dim")
    content = Text()
    content.append(logo_text)
    content.append("\n\n")
    content.append(subtitle)
    console.print(Panel(content, box=BOX_STYLE, border_style="green", padding=(0, 2)))
    console.print(Rule(style="green dim"))


def run_install_dependencies():
    clear_screen()
    draw_header()
    console.print(Panel("[bold green]Install dependencies[/]", title="[green]Step[/]", border_style="green", box=BOX_STYLE))
    console.print()
    cwd = os.path.dirname(os.path.abspath(__file__))
    req_path = os.path.join(cwd, "requirements.txt")
    if not os.path.exists(req_path):
        console.print(Panel("[dim]requirements.txt not found.[/]", border_style="yellow"))
        Prompt.ask("\n[green]Press Enter to continue[/]", default="")
        return
    console.print("  [dim]Running:[/] [green]pip install -r requirements.txt[/]\n")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=cwd,
    )
    console.print()
    if result.returncode == 0:
        console.print(Panel("[green]Dependencies installed successfully.[/]", border_style="green", box=BOX_STYLE))
    else:
        console.print(Panel(f"[red]Installation finished with exit code {result.returncode}.[/]", border_style="red", box=BOX_STYLE))
    Prompt.ask("\n[green]Press Enter to continue[/]", default="")


def run_settings():
    clear_screen()
    draw_header()
    console.print(Panel("[bold green]Settings[/] — Configure provider, model, API key (stored locally)", title="[green]Configuration[/]", border_style="green", box=BOX_STYLE))
    console.print()
    cfg = get_config()
    providers_list = list(PROVIDERS.keys())

    # Providers table
    tbl_prov = Table(title="Provider", box=BOX_STYLE, border_style="green", show_header=True, header_style="bold green")
    tbl_prov.add_column("#", style="dim", width=4)
    tbl_prov.add_column("Provider", style="green")
    tbl_prov.add_column("Current", style="dim")
    for i, p in enumerate(providers_list, 1):
        current = "  ✓" if p == cfg.get("provider") else ""
        tbl_prov.add_row(str(i), p, current)
    console.print(tbl_prov)
    console.print()
    try:
        choice = Prompt.ask(f"[green]Select provider[/] [dim][1-{len(providers_list)}][/], Enter = keep", default="")
        if choice:
            idx = int(choice)
            if 1 <= idx <= len(providers_list):
                cfg["provider"] = providers_list[idx - 1]
    except (ValueError, IndexError):
        pass

    # Models table
    models = get_models_for_provider(cfg["provider"])
    tbl_mod = Table(title=f"Models for [green]{cfg['provider']}[/]", box=BOX_STYLE, border_style="green", show_header=True, header_style="bold green")
    tbl_mod.add_column("#", style="dim", width=4)
    tbl_mod.add_column("Model", style="green")
    tbl_mod.add_column("Current", style="dim")
    for i, m in enumerate(models, 1):
        current = "  ✓" if m == cfg.get("model") else ""
        tbl_mod.add_row(str(i), m, current)
    console.print(tbl_mod)
    console.print()
    try:
        choice = Prompt.ask(f"[green]Select model[/] [dim][1-{len(models)}][/], Enter = keep", default="")
        if choice:
            idx = int(choice)
            if 1 <= idx <= len(models):
                cfg["model"] = models[idx - 1]
    except (ValueError, IndexError):
        pass
    if not cfg.get("model") and models:
        cfg["model"] = models[0]

    console.print()
    key = Prompt.ask("[green]API Key[/] [dim](stored locally only, leave empty to keep)[/]", default="", password=True)
    if key:
        cfg["api_key"] = key

    save_config(cfg["provider"], cfg["model"], cfg.get("api_key", ""))
    console.print()
    console.print(Panel("[green]Configuration saved.[/]", border_style="green", box=BOX_STYLE))
    Prompt.ask("\n[green]Press Enter to continue[/]", default="")


def run_about():
    clear_screen()
    draw_header()
    about_table = Table(box=BOX_STYLE, border_style="green", show_header=False, padding=(0, 2))
    about_table.add_column("Section", style="bold green", width=22)
    about_table.add_column("Content", style="white")
    about_table.add_row("About", "HacxGPT-CLI Launcher — open-source CLI for unrestricted AI, access powerful models without heavy censorship.")
    about_table.add_row("Project", "Powerful, unrestricted, seamless AI-driven conversations.")
    about_table.add_row("What it is", "Open-source CLI for multiple AI providers; advanced system prompt engineering; connects to OpenRouter, Groq, HacxGPT API.")
    about_table.add_row("Provides", "Multi-provider support, local API key storage, cross-platform (Linux, Windows, macOS, Termux), free (BYO keys).")
    about_table.add_row("HacxGPT", "hacxgpt-lightning (production coding)")
    about_table.add_row("Groq", "kimi-k2-instruct-0905, qwen3-32b")
    about_table.add_row("OpenRouter", "mimo-v2-flash, devstral-2512, glm-4.5-air, kimi-k2, deepseek-r1t-chimera")
    about_table.add_row("API keys", "OpenRouter: openrouter.ai/keys | Groq: console.groq.com/keys | HacxGPT: hacxgpt.com")
    about_table.add_row("Links", "Website: hacxgpt.com | Telegram: t.me/HacxGPT | Email: contact@hacxgpt.com | GitHub: HacxGPT-Official/HacxGPT-CLI")
    about_table.add_row("Privacy", "Configuration stored locally only. No data sent to our servers.")
    console.print(Panel(about_table, title="[bold green]About HacxGPT-CLI[/]", border_style="green", box=BOX_STYLE))
    Prompt.ask("\n[green]Press Enter to continue[/]", default="")


def run_chat():
    from chat import chat_request
    cfg = get_config()
    if not cfg.get("api_key", "").strip():
        clear_screen()
        draw_header()
        console.print(Panel("[yellow]Set your API key in [bold]Settings[/] first.[/]", title="[green]Start Chat[/]", border_style="yellow", box=BOX_STYLE))
        Prompt.ask("\n[green]Press Enter to continue[/]", default="")
        return
    clear_screen()
    draw_header()
    info_table = Table(box=box.MINIMAL, show_header=False)
    info_table.add_column("Key", style="dim")
    info_table.add_column("Value", style="green")
    info_table.add_row("Provider", cfg["provider"])
    info_table.add_row("Model", cfg["model"])
    info_table.add_row("Commands", "/clear = clear history  |  /exit = back to menu")
    console.print(Panel(info_table, title="[bold green]Start Chat[/]", border_style="green", box=BOX_STYLE))
    console.print()
    messages = []
    while True:
        try:
            user_input = Prompt.ask("[green]You[/]")
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("/exit", "/quit"):
            break
        if user_input.lower() == "/clear":
            messages = []
            console.print(Panel("[dim]History cleared.[/]", border_style="dim", box=box.MINIMAL))
            console.print()
            continue
        messages.append({"role": "user", "content": user_input})
        with console.status("[dim]Thinking...[/]", spinner="dots"):
            reply = chat_request(messages, cfg["api_key"], cfg["provider"], cfg["model"])
        if reply and not reply.startswith("["):
            messages.append({"role": "assistant", "content": reply})
            console.print(Panel(reply, title="[green]AI[/]", border_style="green", box=BOX_STYLE))
        else:
            console.print(Panel(reply or "[red]No response[/]", border_style="red", box=BOX_STYLE))
        console.print()
    Prompt.ask("[green]Press Enter to continue[/]", default="")


def run_status():
    clear_screen()
    draw_header()
    cfg = get_config()
    key_raw = (cfg.get("api_key") or "").strip()
    key_preview = (key_raw[:8] + "...") if key_raw else "(not set)"
    tbl = Table(title="Current configuration", box=BOX_STYLE, border_style="green", show_header=True, header_style="bold green")
    tbl.add_column("Setting", style="dim", width=12)
    tbl.add_column("Value", style="green")
    tbl.add_row("Provider", cfg.get("provider", "—"))
    tbl.add_row("Model", cfg.get("model", "—"))
    tbl.add_row("API Key", key_preview)
    console.print(Panel(tbl, title="[bold green]Status[/] (/status)", border_style="green", box=BOX_STYLE))
    Prompt.ask("\n[green]Press Enter to continue[/]", default="")


def run_roadmap():
    clear_screen()
    draw_header()
    tbl = Table(title="Technical milestones", box=BOX_STYLE, border_style="green", show_header=True, header_style="bold green")
    tbl.add_column("#", style="dim", width=3)
    tbl.add_column("Milestone", style="green")
    milestones = [
        "Advanced Reasoning Support: Deep-think/reasoning for complex problem-solving",
        "Agentic Capabilities: Autonomous tool use and multi-step execution",
        "Web Search Integration: Real-time data retrieval",
        "Advanced File Analysis: Large datasets and documents",
        "IDE Integrations: VS Code, IntelliJ, and other editors",
        "Conversation Management: Save, load, and resume conversations",
        "Multi-Modal Support: Image and document analysis",
        "Custom Prompt Templates: User-defined system prompts",
        "Provider Auto-Switching: Switch providers by task type",
    ]
    for i, m in enumerate(milestones, 1):
        tbl.add_row(str(i), m)
    console.print(Panel(tbl, title="[bold green]Roadmap[/]", border_style="green", box=BOX_STYLE))
    Prompt.ask("\n[green]Press Enter to continue[/]", default="")


def run_links():
    clear_screen()
    draw_header()
    tbl = Table(title="Important links", box=BOX_STYLE, border_style="green", show_header=True, header_style="bold green")
    tbl.add_column("Resource", style="dim", width=18)
    tbl.add_column("URL / Contact", style="green")
    tbl.add_row("Website", "hacxgpt.com")
    tbl.add_row("Telegram", "t.me/HacxGPT")
    tbl.add_row("Email", "contact@hacxgpt.com")
    tbl.add_row("GitHub", "@HacxGPT-Official")
    tbl.add_row("OpenRouter (keys)", "openrouter.ai/keys")
    tbl.add_row("Groq (keys)", "console.groq.com/keys")
    console.print(Panel(tbl, title="[bold green]Links[/]", border_style="green", box=BOX_STYLE))
    Prompt.ask("\n[green]Press Enter to continue[/]", default="")


def run_disclaimer():
    clear_screen()
    draw_header()
    tbl = Table(box=BOX_STYLE, border_style="green", show_header=False)
    tbl.add_column("Note", style="bold yellow", width=14)
    tbl.add_column("Text", style="white")
    tbl.add_row("Purpose", "Educational and research. You are responsible for compliance with laws and API terms.")
    tbl.add_row("API usage", "Third-party providers (OpenRouter, Groq) have their own ToS.")
    tbl.add_row("Privacy", "Your prompts are sent to the provider you choose, not to us.")
    tbl.add_row("API keys", "Store securely and never share.")
    tbl.add_row("Responsibility", "You are responsible for how you use this tool.")
    tbl.add_row("Developers", "Do NOT collect API keys or prompts; NOT responsible for misuse; encourage responsible use.")
    console.print(Panel(tbl, title="[bold green]Disclaimer[/]", border_style="green", box=BOX_STYLE))
    Prompt.ask("\n[green]Press Enter to continue[/]", default="")


@ensure_env
def main():
    menu_table = Table(box=BOX_STYLE, border_style="green", show_header=True, header_style="bold green", title="Menu")
    menu_table.add_column("Key", style="dim", width=6)
    menu_table.add_column("Action", style="green")
    menu_table.add_row("1", "Install dependencies")
    menu_table.add_row("2", "Settings")
    menu_table.add_row("3", "Start Chat")
    menu_table.add_row("4", "Status")
    menu_table.add_row("5", "About")
    menu_table.add_row("6", "Roadmap")
    menu_table.add_row("7", "Links")
    menu_table.add_row("8", "Disclaimer")
    menu_table.add_row("0", "Exit")

    while True:
        clear_screen()
        draw_header()
        console.print(menu_table)
        console.print()
        console.print(Rule(style="dim"))
        console.print("[dim]API keys stored locally only  |  hacxgpt.com[/]")
        console.print()
        choice = Prompt.ask("[green]Select option[/]", default="").strip()

        if choice == "0":
            clear_screen()
            console.print(Panel("[green]Goodbye.[/]", border_style="green", box=BOX_STYLE))
            break
        if choice == "1":
            run_install_dependencies()
        elif choice == "2":
            run_settings()
        elif choice == "3":
            run_chat()
        elif choice == "4":
            run_status()
        elif choice == "5":
            run_about()
        elif choice == "6":
            run_roadmap()
        elif choice == "7":
            run_links()
        elif choice == "8":
            run_disclaimer()
        else:
            console.print(Panel("[yellow]Invalid option.[/]", border_style="yellow", box=BOX_STYLE))
            Prompt.ask("[green]Press Enter to continue[/]", default="")


if __name__ == "__main__":
    main()
