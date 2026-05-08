from pathlib import Path
import json
import os
import shutil
import sys

import jsonc

repo_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(repo_root))

from configure import configure_ocr_model

install_path = repo_root / "install"
version = len(sys.argv) > 1 and sys.argv[1] or "v0.0.1"


def install_resource():
    configure_ocr_model()

    shutil.copytree(
        repo_root / "assets",
        install_path,
        dirs_exist_ok=True,
    )
    shutil.rmtree(install_path / "MaaCommonAssets", ignore_errors=True)

    with open(install_path / "interface.json", "r", encoding="utf-8") as f:
        interface = jsonc.load(f)

    interface["version"] = version
    interface["github"] = "https://github.com/steven42121/MAA_SnowBreak"
    interface.pop("mirrorchyan_rid", None)

    with open(install_path / "interface.json", "w", encoding="utf-8") as f:
        jsonc.dump(interface, f, ensure_ascii=False, indent=4)


def install_chores():
    for file in ["README.md", "LICENSE", "DISCLAIMER.md", "CONTACT.md", "logo.png", "requirements.txt"]:
        shutil.copy2(repo_root / file, install_path / file)


def install_agent():
    custom_src = repo_root / "assets" / "MSBAcustom"
    agent_dst = install_path / "agent"
    shutil.copytree(custom_src, agent_dst, dirs_exist_ok=True)

    with open(install_path / "interface.json", "r", encoding="utf-8") as f:
        interface = jsonc.load(f)

    target_os = os.getenv("TARGET_OS", "").lower()
    os_exec_map = {
        "win": r"./python/python.exe",
        "macos": r"./python/bin/python3",
        "linux": r"python3",
    }

    interface.setdefault("agent", {})
    interface["agent"]["child_exec"] = os_exec_map.get(target_os, "python3")
    interface["agent"]["child_args"] = ["-u", r"./agent/main.py"]
    interface["agent"]["embedded"] = True

    with open(install_path / "interface.json", "w", encoding="utf-8") as f:
        json.dump(interface, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    install_resource()
    install_chores()
    install_agent()
    print(f"Install to {install_path} successfully.")
