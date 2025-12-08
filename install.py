from pathlib import Path
import PyInstaller.__main__
import site
import os

import shutil
import sys
import jsonc

from configure import configure_ocr_model


working_dir = Path(__file__).parent
install_path = working_dir / Path("maapicli")
version = len(sys.argv) > 1 and sys.argv[1] or "v0.0.1"


def install_resource():

    configure_ocr_model()

    shutil.copytree(
        working_dir / "assets",
        install_path,
        dirs_exist_ok=True,
    )
    shutil.rmtree(install_path / "MaaCommonAssets")

    shutil.copy2(
        working_dir / "logo.png",
        install_path / "logo.png",
    )

    # 删除指定文件,而非文件夹
    try:
        os.remove(install_path / "custom" / "main.py")
    except FileNotFoundError:
        pass
    try:
        os.remove(install_path / "custom" / "Agent_file.py")
    except FileNotFoundError:
        pass


    with open(install_path / "interface.jsonc", "r", encoding="utf-8") as f:
        interface = jsonc.load(f)

    interface["version"] = version
    interface["name"] = f"MAA_snowbreak {version}"

    with open(install_path / "interface.jsonc", "w", encoding="utf-8") as f:
        jsonc.dump(interface, f, ensure_ascii=False, indent=4)


def install_chores():
    shutil.copy2(
        working_dir / "README.md",
        install_path,
    )
    shutil.copy2(
        working_dir / "LICENSE",
        install_path,
    )


if __name__ == "__main__":
    install_resource()
    install_chores()
