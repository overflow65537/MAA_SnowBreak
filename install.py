from pathlib import Path
import PyInstaller.__main__
import site
import os

import shutil
import sys
import json

from configure import configure_ocr_model


working_dir = Path(__file__).parent
install_path = working_dir / Path("install")
version = len(sys.argv) > 1 and sys.argv[1] or "v0.0.1"


def bulid():
    # 获取 site-packages 目录列表
    site_packages_paths = site.getsitepackages()

    # 查找包含 maa/bin 的路径
    maa_bin_path = None
    for path in site_packages_paths:
        potential_path = os.path.join(path, "maa", "bin")
        if os.path.exists(potential_path):
            maa_bin_path = potential_path
            break

    if maa_bin_path is None:
        raise FileNotFoundError("not found maa/bin")

    # 构建 --add-data 参数
    add_data_param = f"{maa_bin_path}{os.pathsep}maa/bin"

    # 查找包含 MaaAgentBinary 的路径
    maa_bin_path2 = None
    for path in site_packages_paths:
        potential_path = os.path.join(path, "MaaAgentBinary")
        if os.path.exists(potential_path):
            maa_bin_path2 = potential_path
            break

    if maa_bin_path2 is None:
        raise FileNotFoundError("not found MaaAgentBinary")

    # 构建 --add-data 参数
    add_data_param2 = f"{maa_bin_path2}{os.pathsep}MaaAgentBinary"

    command = [
        "run_cli.py",
        "--name=maapicli",
        f"--add-data={add_data_param}",
        f"--add-data={add_data_param2}",
        f"--distpath={install_path}",
        "--onefile",
        "--clean",
    ]
    PyInstaller.__main__.run(command)


def install_resource():

    configure_ocr_model()

    shutil.copytree(
        working_dir / "assets" / "resource",
        install_path / "resource",
        dirs_exist_ok=True,
    )
    shutil.copy2(
        working_dir / "assets" / "interface.json",
        install_path,
    )

    with open(install_path / "interface.json", "r", encoding="utf-8") as f:
        interface = json.load(f)

    interface["version"] = version

    with open(install_path / "interface.json", "w", encoding="utf-8") as f:
        json.dump(interface, f, ensure_ascii=False, indent=4)


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
    bulid()
    install_resource()
    install_chores()
