from pathlib import Path

import os
import shutil
import sys
import json
import jsonc

from configure import configure_ocr_model


repo_root = Path(__file__).parent.parent.resolve()
working_dir = repo_root / "deps" / "MAA_SnowBreak"
install_path = repo_root / "install"
version = len(sys.argv) > 1 and sys.argv[1] or "v0.0.1"


def install_resource():

    configure_ocr_model()

    shutil.copytree(
        working_dir / "assets",
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
    for file in ["README.md", "LICENSE", "DISCLAIMER.md", "CONTACT.md", "logo.png"]:
        shutil.copy2(
            working_dir / file,
            install_path / file,
        )


def install_agent():
    agent_src = repo_root / "agent"
    agent_dst = install_path / "agent"
    if agent_src.exists():
        shutil.copytree(
            agent_src,
            agent_dst,
            dirs_exist_ok=True,
        )
    else:
        agent_dst.mkdir(parents=True, exist_ok=True)

    msba_custom_dir = working_dir / "assets" / "MSBAcustom"
    excluded_files = {"main.py", "custom.json"}

    for item in msba_custom_dir.iterdir():
        if item.name in excluded_files:
            continue

        target = agent_dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)

    with open(install_path / "interface.json", "r", encoding="utf-8") as f:
        interface = jsonc.load(f)

    # 根据 CI 传入的 OS 环境变量来设置 child_exec
    target_os = os.getenv("TARGET_OS", "").lower()

    # OS 到 child_exec 的映射
    os_exec_map = {
        "win": r"./python/python.exe",
        "macos": r"./python/bin/python3",
        "linux": r"python3",
    }

    interface["agent"]["child_exec"] = os_exec_map.get(target_os, "python3")
    interface["agent"]["child_args"] = ["-u", r"./Agent/main.py"]

    with open(install_path / "interface.json", "w", encoding="utf-8") as f:
        json.dump(interface, f, ensure_ascii=False, indent=4)

    shutil.copy2(
        working_dir / "requirements.txt",
        install_path / "requirements.txt",
    )


if __name__ == "__main__":
    install_resource()
    install_chores()
    install_agent()

    print(f"Install to {install_path} successfully.")
