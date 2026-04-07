from pathlib import Path

import shutil

repo_root = Path(__file__).parent
assets_dir = repo_root / "deps" / "MAA_SnowBreak" / "assets"


def configure_ocr_model():
    if not (assets_dir / "MaaCommonAssets" / "OCR").exists():
        print("Please clone this repository completely, including submodules, and don’t download the zip package!")
        print("请完整克隆本仓库并初始化全部子模块，不要下载 zip 包！")
        exit(1)

    shutil.copytree(
        assets_dir / "MaaCommonAssets" / "OCR" / "ppocr_v4" / "zh_cn",
        assets_dir / "resource" / "base" / "model" / "ocr",
        dirs_exist_ok=True,
    )


if __name__ == "__main__":
    configure_ocr_model()

    print("OCR model configured.")