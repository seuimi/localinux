# 모듈
import os
import questionary
import re
import subprocess
from ruamel.yaml import YAML
from rich.console import Console
from rich.text import Text



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
    language_set = questionary.select(
        "언어를 선택하세요.", choices=["한국어", "English"]
    ).ask()

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



# 초기세팅
if config["first_setup"] is False:
        user_name_set = questionary.text(
              language["setup"]["user_set"], validate=lambda text: bool(re.fullmatch(r"[A-Za-z0-9_]+", text))
        ).ask()

        config["first_setup"] = True
        config["user_name"] = user_name_set

        save_config(config)

        print(language["setup"]["user_set_complete"])
else:
      print("세팅이 이미 완료된 상태입니다.")