#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path


PYTHON_VERSION = "3.12.12"
BUILD_DATE = "20251209"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"


def log(message):
    print(message, flush=True)


def get_python_url():
    system = platform.system()
    machine = platform.machine().lower()

    if machine in ("x86_64", "amd64"):
        arch = "x86_64"
    elif machine in ("aarch64", "arm64"):
        arch = "aarch64"
    else:
        raise RuntimeError(f"unsupported architecture: {machine}")

    base_url = f"https://github.com/indygreg/python-build-standalone/releases/download/{BUILD_DATE}"
    if system == "Darwin":
        platform_name = "apple-darwin"
    elif system == "Windows":
        platform_name = "pc-windows-msvc"
    elif system == "Linux":
        platform_name = "unknown-linux-gnu"
    else:
        raise RuntimeError(f"unsupported system: {system}")

    archive_name = f"cpython-{PYTHON_VERSION}+{BUILD_DATE}-{arch}-{platform_name}-install_only_stripped.tar.gz"
    return f"{base_url}/{archive_name}", archive_name


def find_python(dest_dir):
    candidates = [
        dest_dir / "python.exe",
        dest_dir / "python3",
        dest_dir / "bin" / "python3",
        dest_dir / "bin" / "python",
    ]
    for candidate in candidates:
        if candidate.is_file():
            if platform.system() != "Windows":
                os.chmod(candidate, 0o755)
            return candidate.resolve()
    return None


def download_file(url, path):
    log(f"Downloading {url}")
    with urllib.request.urlopen(url) as response, open(path, "wb") as f:
        shutil.copyfileobj(response, f)


def extract_archive(archive, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as tar:
        members = tar.getmembers()
        for member in members:
            parts = Path(member.name).parts
            member.name = str(Path(*parts[1:])) if len(parts) > 1 else ""
            if member.name:
                tar.extract(member, dest_dir)


def configure_windows_python(dest_dir):
    for pth_file in dest_dir.glob("python*._pth"):
        content = pth_file.read_text(encoding="utf-8")
        content = content.replace("# import site", "import site").replace("#import site", "import site")
        for path in [".", ".\\Lib", ".\\Lib\\site-packages", ".\\DLLs"]:
            if path not in content:
                content += f"\n{path}"
        pth_file.write_text(content, encoding="utf-8", newline="\r\n")
        break


def setup_pip(python_exe, dest_dir):
    get_pip = dest_dir / "get-pip.py"
    download_file(GET_PIP_URL, get_pip)
    try:
        subprocess.run([str(python_exe), str(get_pip)], check=True)
        subprocess.run([str(python_exe), "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    finally:
        get_pip.unlink(missing_ok=True)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: install_python.py <target-dir>")

    dest_dir = Path(sys.argv[1]).resolve()
    python_exe = find_python(dest_dir)
    if python_exe is None:
        url, archive_name = get_python_url()
        archive = Path(archive_name)
        download_file(url, archive)
        try:
            extract_archive(archive, dest_dir)
        finally:
            archive.unlink(missing_ok=True)

        if platform.system() == "Windows":
            configure_windows_python(dest_dir)

        python_exe = find_python(dest_dir)
        if python_exe is None:
            raise RuntimeError("python executable not found after extraction")

    setup_pip(python_exe, dest_dir)


if __name__ == "__main__":
    main()
