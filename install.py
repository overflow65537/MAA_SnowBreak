from pathlib import Path
import shutil
import sys
import jsonc
from configure import configure_ocr_model


working_dir = Path(__file__).parent
install_path = working_dir / Path("install")
version = len(sys.argv) > 1 and sys.argv[1] or "v0.0.1"


def install_resource():

    configure_ocr_model()

    shutil.copytree(
        working_dir / "assets",
        install_path,
        dirs_exist_ok=True,
    )
    shutil.rmtree(install_path / "MaaCommonAssets")

    (install_path / "logo.png").unlink(missing_ok=True)

    shutil.copy2(
        working_dir / "logo.png",
        install_path / "logo.png",
    )
    shutil.copy2(
        working_dir / "update_flag.txt",
        install_path / "update_flag.txt",
    )

    with open(install_path / "interface.json", "r", encoding="utf-8") as f:
        interface = jsonc.load(f)

    interface["version"] = version
    with open(install_path / "interface.json", "w", encoding="utf-8") as f:
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
    shutil.copy2(
        working_dir / "DISCLAIMER.md",
        install_path,
    )
    shutil.copy2(
        working_dir / "CONTACT.md",
        install_path,
    )
    shutil.copy2(
        install_path / "logo.png",
        install_path / "dashboard.png",
    )


if __name__ == "__main__":
    install_resource()
    install_chores()
