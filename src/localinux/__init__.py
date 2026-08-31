import os
import subprocess
from pathlib import Path

from rich.console import Console
from rich.text import Text
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = ROOT / "config.yaml"
LOCALES_DIR = ROOT / "locales"

yaml = YAML()
yaml.preserve_quotes = True


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {"first_setup": False, "language": "", "user_name": ""}

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = yaml.load(f)
        return data or {"first_setup": False, "language": "", "user_name": ""}


def load_language(language: str) -> dict:
    path = LOCALES_DIR / f"{language}.yaml"

    if not path.exists():
        path = LOCALES_DIR / "en.yaml"

    with open(path, "r", encoding="utf-8") as f:
        return yaml.load(f)


def print_logo(console: Console) -> None:
    localinux_logo = """\
    
    
    ██╗      ██████╗  ██████╗ █████╗ ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗
    ██║     ██╔═══██╗██╔════╝██╔══██╗██║     ██║████╗  ██║██║   ██║╚██╗██╔╝
    ██║     ██║   ██║██║     ███████║██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝
    ██║     ██║   ██║██║     ██╔══██║██║     ██║██║╚██╗██║██║   ██║ ██╔██╗
    ███████╗╚██████╔╝╚██████╗██║  ██║███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗
    ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
        L O C A L I N U X
"""

    logo = Text()
    for line in localinux_logo.splitlines():
        for i, char in enumerate(line):
            if char != " ":
                ratio = i / max(len(line) - 1, 1)
                r = 255
                g = int(255 - (155 * ratio))
                b = int(255 - (75 * ratio))
                logo.append(char, style=f"rgb({r},{g},{b})")
            else:
                logo.append(" ")
        logo.append("\n")

    console.print(logo)


def main() -> None:
    console = Console()

    config = load_config()
    lang_code = config.get("language") or "ko"
    t = load_language(lang_code)
    splash = t.get("splash", {})

    subprocess.run(["cls" if os.name == "nt" else "clear"], shell=True)

    print_logo(console)
    console.print()
    console.print(f"[bold cyan]Localinux[/bold cyan]  [dim]{splash.get('tagline', '')}[/dim]")
    console.print()
    console.print(f"[bold]{splash.get('made_by', 'Made by')}[/bold]  [green]{splash.get('author', '')}[/green]")
    console.print(f"[dim]{splash.get('repo', '')}[/dim]")
    console.print()
    console.print(f"[yellow]{splash.get('how_to_run', '')}[/yellow]")
    console.print(f"  [bold white]{splash.get('run_command', 'uv run main.py')}[/bold white]")
    console.print()
    console.print(f"[dim]{splash.get('hint', '')}[/dim]")
    console.print()


if __name__ == "__main__":
    main()