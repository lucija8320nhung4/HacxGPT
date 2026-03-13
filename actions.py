# -*- coding: utf-8 -*-
"""Actions for DataHaven CLI — run commands according to README."""
import os
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from config import PATHS, PROJECT_ROOT, INJECT_CONTRACTS

console = Console()


def _run(cmd: list[str], cwd: Path, env: dict | None = None) -> bool:
    """Run command; return True on success."""
    env = env or {}
    full_env = {**os.environ, **env}
    try:
        r = subprocess.run(
            cmd,
            cwd=cwd,
            env=full_env,
            shell=(sys.platform == "win32"),
        )
        return r.returncode == 0
    except FileNotFoundError:
        console.print(f"[red]Command not found: {cmd}[/red]")
        return False


def install_dependencies() -> bool:
    """Install dependencies (test): cd test && bun i."""
    path = PATHS["test"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        console.print("Create the repository structure or set DATAHAVEN_PROJECT_ROOT.")
        return False
    console.print(Panel("Installing dependencies in [bold]test[/bold] (bun i)", border_style="blue"))
    return _run(["bun", "i"], cwd=path)


def launch_network() -> bool:
    """Launch local network: cd test && bun cli launch."""
    path = PATHS["test"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Launching local network (bun cli launch)", border_style="blue"))
    return _run(["bun", "run", "cli", "launch"], cwd=path)


def run_tests_e2e() -> bool:
    """Run E2E tests: cd test && bun teste2e."""
    path = PATHS["test"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    env = {"INJECT_CONTRACTS": "true"} if INJECT_CONTRACTS else None
    console.print(Panel("Running E2E tests (bun teste2e)", border_style="blue"))
    return _run(["bun", "run", "teste2e"], cwd=path, env=env)


def run_tests_e2e_parallel() -> bool:
    """Run E2E tests with limited concurrency: bun teste2eparallel."""
    path = PATHS["test"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Running E2E tests parallel (bun teste2eparallel)", border_style="blue"))
    return _run(["bun", "run", "teste2eparallel"], cwd=path)


def contracts_build() -> bool:
    """Build contracts: cd contracts && forge build."""
    path = PATHS["contracts"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Building contracts (forge build)", border_style="blue"))
    return _run(["forge", "build"], cwd=path)


def contracts_test() -> bool:
    """Test contracts: cd contracts && forge test."""
    path = PATHS["contracts"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Running contract tests (forge test)", border_style="blue"))
    return _run(["forge", "test"], cwd=path)


def operator_build() -> bool:
    """Build operator: cd operator && cargo build --release --features fast-runtime."""
    path = PATHS["operator"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Building operator (cargo build --release --features fast-runtime)", border_style="blue"))
    return _run(["cargo", "build", "--release", "--features", "fast-runtime"], cwd=path)


def operator_test() -> bool:
    """Test operator: cd operator && cargo test."""
    path = PATHS["operator"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Running operator tests (cargo test)", border_style="blue"))
    return _run(["cargo", "test"], cwd=path)


def regenerate_wagmi() -> bool:
    """Regenerate contract bindings: cd test && bun generatewagmi."""
    path = PATHS["test"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Regenerating WAGMI bindings (bun generatewagmi)", border_style="blue"))
    return _run(["bun", "run", "generatewagmi"], cwd=path)


def regenerate_types() -> bool:
    """Regenerate runtime types: cd test && bun generatetypes."""
    path = PATHS["test"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Regenerating runtime types (bun generatetypes)", border_style="blue"))
    return _run(["bun", "run", "generatetypes"], cwd=path)


def build_docker_operator() -> bool:
    """Build Docker image: cd test && bun builddockeroperator."""
    path = PATHS["test"]
    if not path.exists():
        console.print(f"[yellow]Folder not found: {path}[/yellow]")
        return False
    console.print(Panel("Building Docker image (bun builddockeroperator)", border_style="blue"))
    return _run(["bun", "run", "builddockeroperator"], cwd=path)
