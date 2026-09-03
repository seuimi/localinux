# 모듈
import os
import questionary
import re
import subprocess
from ruamel.yaml import YAML
from rich.console import Console
from rich.text import Text
import zipfile
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn
)



# 설정 파일
config_file = "config.yaml"
yaml = YAML()
yaml.preserve_quotes = True

def load_config():
        if not os.path.exists(config_file):
                yaml_set = """# ==============================
# ! ! [ 경고 / Warning ] ! !
#
# 현재 이 파일은 프로그램의 설정값이 저장된 파일입니다.
# 임의로 내용이나 구조를 변경하면 프로그램의 실행에 큰 문제가 발생될 수 있습니다.
#
# This file contains the program's configuration settings.
# Modifying its contents or structure arbitrarily may cause serious problem with the program.
# ==============================

first_setup: false

language: ""

user_name: ""
"""

                with open(config_file, "w", encoding="utf-8") as file:
                        file.write(yaml_set)
        with open(config_file, "r", encoding="utf-8") as file:
                return yaml.load(file)

def save_config(config):
        with open(config_file, "w", encoding="utf-8") as file:
                yaml.dump(config, file)

# 언어
def load_language(language):
    language_file = f"locales/{language}.yaml"

    with open(language_file, "r", encoding="utf-8") as file:
        return yaml.load(file)

config = load_config()



# 언어 설정
if config["language"] == "":
    language_set = questionary.select("언어를 선택하세요.", choices=["한국어", "English"]).ask()

    language_list = {
        "한국어": "ko",
        "English": "en"
    }

    config["language"] = language_list[language_set]

    save_config(config)

language = load_language(config["language"])



# Localinux 텍스트
console = Console()

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

            logo.append(
                char,
                style=f"rgb({r},{g},{b})"
            )
        else:
            logo.append(" ")

    logo.append("\n")

subprocess.run(['cls' if os.name == 'nt' else 'clear'],shell=True)
console.print(logo)



# 서버 다운로드
server_download_url = "http://127.0.0.1:1234/server-latest.zip"

server_DIR = Path("server")
server_PATH = server_DIR / "server-latest.zip"

def download_server():
    server_DIR.mkdir(parents=True, exist_ok=True)
    console.print('\n' + language["server"]["download_start"], style="#FF9F43")

    try:
        with urlopen(server_download_url) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            with open(server_PATH, "wb") as file:
                with Progress(
                    TextColumn("[progress.description]{task.description}"), BarColumn(), DownloadColumn(), TransferSpeedColumn(), TimeRemainingColumn()
                ) as progress:
                    task = progress.add_task(
                        "server download...", total=total_size
                    )
                    while True:
                        chunk = response.read(1024 * 64)
                        if not chunk:
                            break
                        file.write(chunk)
                        progress.update(
                            task, advance=len(chunk)
                        )

        console.print(language["server"]["download_done"] + '\n', style="green")

    except (URLError, TimeoutError, ConnectionError):
        console.print('\n' + language["server"]["download_error"] + '\n', style="red")
        input("[ Enter ] Program exit...")
         
        raise SystemExit



# 서버 압축 해제
def extract_server():
    console.print(language["server"]["zip_out_your_pc"], style="#FF9F43")
    with zipfile.ZipFile(server_PATH, "r") as archive:
        members = archive.infolist()
        with Progress(
        TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.completed}/{task.total}"), TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(
                "Extracting downloaded server...", total=len(members)
            )
            for member in members:
                archive.extract(
                    member, path=server_DIR
                )
                progress.update(
                    task, advance=1
                )
    server_PATH.unlink()

    console.print(language["server"]["zip_out_your_pc_done"] + '\n', style="green")



# 초기세팅
if config["first_setup"] is False:
    config["first_setup"] = True

    console.print(language["setup"]["user_set_done"], style="green")

    download_server()
    extract_server()

    save_config(config)
else:
      print("done.")