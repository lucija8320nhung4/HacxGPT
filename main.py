# -*- coding: utf-8 -*-
"""
DataHaven CLI — AI-First Decentralized Storage.
Menu in CMD style with Rich.
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.markdown import Markdown
from rich import box
from utils import ensure_env

from config import PATHS, PROJECT_ROOT
import actions

console = Console()

LOGO = r"""
                  $$$$$$$\             $$\                     
                  $$  __$$\            $$ |                    
                  $$ |  $$ | $$$$$$\ $$$$$$\    $$$$$$\        
                  $$ |  $$ | \____$$\\_$$  _|   \____$$\       
                  $$ |  $$ | $$$$$$$ | $$ |     $$$$$$$ |      
                  $$ |  $$ |$$  __$$ | $$ |$$\ $$  __$$ |      
                  $$$$$$$  |\$$$$$$$ | \$$$$  |\$$$$$$$ |      
                  \_______/  \_______|  \____/  \_______|      
                                                               
                                                               
                                                               
            $$\                                                
            $$ |                                               
            $$$$$$$\   $$$$$$\ $$\    $$\  $$$$$$\  $$$$$$$\   
            $$  __$$\  \____$$\\$$\  $$  |$$  __$$\ $$  __$$\  
            $$ |  $$ | $$$$$$$ |\$$\$$  / $$$$$$$$ |$$ |  $$ | 
            $$ |  $$ |$$  __$$ | \$$$  /  $$   ____|$$ |  $$ | 
            $$ |  $$ |\$$$$$$$ |  \$  /   \$$$$$$$\ $$ |  $$ | 
            \__|  \__| \_______|   \_/     \_______|\__|  \__| 
"""


def show_logo() -> None:
    console.print(Panel(LOGO, border_style="cyan", box=box.DOUBLE, padding=(0, 1)))
    console.print(
        "[bold cyan]AI-First Decentralized Storage[/bold cyan] "
        "secured by EigenLayer — verifiable storage for AI & Web3"
    )
    console.print()


def show_about() -> None:
    about_text = """
# DataHaven

**AI-First Decentralized Storage** secured by EigenLayer — a verifiable storage network for AI training data, ML models, and Web3 applications.

## Core capabilities
- **Verifiable Storage** — Files chunked, Merkle trees, commitments on-chain
- **Provider Network** — MSPs (Main) and BSPs (Backup) with on-chain slashing
- **EigenLayer Security** — Validators secured by Ethereum restaking
- **EVM Compatibility** — Frontier pallets, Solidity, MetaMask
- **Cross-chain** — Snowbridge for Ethereum ↔ DataHaven

## Links
- [DataHaven Website](https://datahaven.network)
- [DataHaven Documentation](https://docs.datahaven.network)
- [StorageHub](https://github.com/polkadot-storage-hub/storage-hub)
- [EigenLayer](https://docs.eigenlayer.xyz)
- [Substrate](https://docs.substrate.io)
- [Snowbridge](https://docs.snowbridge.network)

## License
GPL-3.0
"""
    console.print(Panel(Markdown(about_text), title="About DataHaven", border_style="green", box=box.ROUNDED))


def show_settings() -> None:
    table = Table(title="Settings", box=box.ROUNDED, border_style="yellow")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Project root", str(PROJECT_ROOT))
    for name, path in PATHS.items():
        exists = "[green]exists[/green]" if path.exists() else "[red]missing[/red]"
        table.add_row(f"  {name}/", f"{path} {exists}")
    table.add_row("INJECT_CONTRACTS", "Set env INJECT_CONTRACTS=true to inject contracts in E2E")
    console.print(table)
    console.print("\n[dim]To use another repo root: set environment variable DATAHAVEN_PROJECT_ROOT[/dim]\n")


def show_prerequisites() -> None:
    text = """
- **Kurtosis** — Network orchestration
- **Bun v1.3.2+** — TypeScript runtime
- **Docker** — Container management
- **Foundry** — Solidity (forge)
- **Rust** — Operator build
- **Helm** — Kubernetes (optional)
- **Zig** — macOS cross-compilation (optional)
"""
    console.print(Panel(text.strip(), title="Prerequisites", border_style="magenta", box=box.ROUNDED))


def show_menu() -> str:
    table = Table(show_header=False, box=box.SIMPLE, border_style="blue")
    table.add_column("Key", style="bold cyan", width=4)
    table.add_column("Action", style="white")
    table.add_row("1", "Install Dependencies (test: bun i)")
    table.add_row("2", "Launch Local Network (bun cli launch)")
    table.add_row("3", "Run E2E Tests (bun teste2e)")
    table.add_row("4", "Run E2E Tests Parallel (bun teste2eparallel)")
    table.add_row("5", "Contracts: Build (forge build)")
    table.add_row("6", "Contracts: Test (forge test)")
    table.add_row("7", "Operator: Build (cargo build --release --features fast-runtime)")
    table.add_row("8", "Operator: Test (cargo test)")
    table.add_row("9", "Regenerate WAGMI bindings")
    table.add_row("10", "Regenerate runtime types")
    table.add_row("11", "Build Docker image (operator)")
    table.add_row("s", "Settings (paths & env)")
    table.add_row("p", "Prerequisites")
    table.add_row("a", "About")
    table.add_row("q", "Quit")
    console.print(Panel(table, title="Menu", border_style="blue", box=box.DOUBLE))
    return Prompt.ask("[bold]Choice[/bold]", default="q").strip().lower()


@ensure_env
def main() -> None:
    show_logo()

    while True:
        choice = show_menu()

        if choice == "q":
            console.print("[yellow]Bye.[/yellow]")
            break
        if choice == "s":
            show_settings()
            continue
        if choice == "p":
            show_prerequisites()
            continue
        if choice == "a":
            show_about()
            continue

        actions_map = {
            "1": actions.install_dependencies,
            "2": actions.launch_network,
            "3": actions.run_tests_e2e,
            "4": actions.run_tests_e2e_parallel,
            "5": actions.contracts_build,
            "6": actions.contracts_test,
            "7": actions.operator_build,
            "8": actions.operator_test,
            "9": actions.regenerate_wagmi,
            "10": actions.regenerate_types,
            "11": actions.build_docker_operator,
        }
        fn = actions_map.get(choice)
        if fn:
            ok = fn()
            console.print("[green]Done.[/green]" if ok else "[red]Failed.[/red]")
        else:
            console.print("[red]Unknown option.[/red]")

        console.print()


if __name__ == "__main__":
    main()
