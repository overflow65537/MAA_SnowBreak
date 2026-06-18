from pathlib import Path
import shutil
import subprocess
import sys

import jsonc

# 仓库根目录（本脚本位于 tools/ci/）
REPO_ROOT = Path(__file__).resolve().parents[2]
install_path = REPO_ROOT / "install"
version = len(sys.argv) > 1 and sys.argv[1] or "v0.0.1"
MODEL_OCR_DET = REPO_ROOT / "resource/base/model/ocr/det.onnx"

# 安装包资源（原 assets/ 下内容，现位于仓库根目录）
RESOURCE_ITEMS = (
    "agent",
    "resource",
    "tasks",
    "interface.json",
)


def ensure_model_submodule():
    if MODEL_OCR_DET.is_file():
        return

    print("OCR model not found, initializing submodule resource/base/model...")
    subprocess.run(
        [
            "git",
            "submodule",
            "update",
            "--init",
            "--depth",
            "1",
            "resource/base/model",
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    if not MODEL_OCR_DET.is_file():
        print(
            "OCR model is missing under resource/base/model/ocr.\n"
            "Please clone with --recursive or run:\n"
            "  git submodule update --init resource/base/model"
        )
        sys.exit(1)


def install_resource():
    ensure_model_submodule()

    for name in RESOURCE_ITEMS:
        src = REPO_ROOT / name
        dst = install_path / name
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    shutil.copy2(
        REPO_ROOT / "logo.png",
        install_path / "logo.png",
    )
    shutil.copy2(
        REPO_ROOT / "CFA_setting.json",
        install_path / "CFA_setting.json",
    )

    with open(install_path / "interface.json", "r", encoding="utf-8") as f:
        interface = jsonc.load(f)

    interface["version"] = version
    with open(install_path / "interface.json", "w", encoding="utf-8") as f:
        jsonc.dump(interface, f, ensure_ascii=False, indent=4)

    if not (install_path / "resource/base/model/ocr/det.onnx").is_file():
        print("Install failed: OCR model was not copied into install/resource/base/model/ocr")
        sys.exit(1)


def install_chores():
    shutil.copy2(
        REPO_ROOT / "README.md",
        install_path,
    )
    shutil.copy2(
        REPO_ROOT / "LICENSE",
        install_path,
    )
    shutil.copy2(
        REPO_ROOT / "DISCLAIMER.md",
        install_path / "DISCLAIMER.md",
    )
    shutil.copy2(
        REPO_ROOT / "CONTACT.md",
        install_path / "CONTACT.md",
    )
    shutil.copy2(
        install_path / "logo.png",
        install_path / "dashboard.png",
    )


if __name__ == "__main__":
    install_resource()
    install_chores()
