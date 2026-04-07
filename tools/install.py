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
    interface["title"] = f"MAA_snowbreak {version}"

    with open(install_path / "interface.json", "w", encoding="utf-8") as f:
        jsonc.dump(interface, f, ensure_ascii=False, indent=4)


def install_chores():
    for file in ["README.md", "LICENSE", "DISCLAIMER.md", "CONTACT.md", "logo.png", "update_flag.txt"]:
        shutil.copy2(
            working_dir / file,
            install_path / file,
        )


def install_agent():
    with open(install_path / "interface.json", "r", encoding="utf-8") as f:
        interface = jsonc.load(f)

    # 根据 CI 传入的 OS 环境变量来设置 child_exec
    target_os = os.getenv("TARGET_OS", "").lower()

    # OS 到 child_exec 的映射
    os_exec_map = {
        "win": r"./python/python.exe",
        "macos": r"./python/bin/python3",
        "linux": r"python3",
        "android": r"python3",
    }

    interface["agent"]["child_exec"] = os_exec_map.get(target_os, "python3")
    interface["agent"]["child_args"] = ["-u", r"{PROJECT_DIR}/MSBAcustom/main.py"]

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
