#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嵌入式Python安装脚本（跨平台）
功能：下载并解压Python嵌入式版本，然后配置pip
"""

import os
import sys
import platform
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional

# 修复Windows中文输出编码问题
if sys.platform == "win32":
    import io
    # 设置标准输出和错误输出使用UTF-8编码
    if sys.stdout.encoding != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if sys.stderr.encoding != "utf-8":
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# 配置常量
PYTHON_VERSION = "3.12.12"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"


def log(message: str, color: str = ""):
    """打印日志消息"""
    if color:
        print(f"{color}{message}\033[0m")
    else:
        print(message)


def get_python_url() -> tuple[str, str, str]:
    """
    根据平台获取Python下载URL
    返回: (url, archive_name, python_exe_name)
    """
    system = platform.system()
    machine = platform.machine().lower()

    log(f"检测平台: {system} ({machine})")

    if machine in ("x86_64", "amd64"):
        arch = "x86_64"
    elif machine in ("aarch64", "arm64"):
        arch = "aarch64"
    else:
        log(f"错误: 不支持的架构 {machine}", "\033[31m")
        sys.exit(1)

    base_url = (
        "https://github.com/indygreg/python-build-standalone/releases/download/20251209"
    )

    if system == "Darwin":
        url = f"{base_url}/cpython-{PYTHON_VERSION}+20251209-{arch}-apple-darwin-install_only_stripped.tar.gz"
    elif system == "Windows":
        url = f"{base_url}/cpython-{PYTHON_VERSION}+20251209-{arch}-pc-windows-msvc-install_only_stripped.tar.gz"
    elif system == "Linux":
        url = f"{base_url}/cpython-{PYTHON_VERSION}+20251209-{arch}-unknown-linux-gnu-install_only_stripped.tar.gz"
    else:
        log(f"错误: 不支持的操作系统 {system}", "\033[31m")
        sys.exit(1)

    return (
        url,
        f"python-{PYTHON_VERSION}+20251209-{arch}-{system}-install_only_stripped.tar.gz",
        "python3",
    )


def download_file(url: str, dest: Path):
    """下载文件"""
    log(f"下载: {url}", "\033[36m")
    try:
        with urllib.request.urlopen(url) as response, open(dest, "wb") as f:
            shutil.copyfileobj(response, f)
        log(f"下载完成: {dest.name}", "\033[32m")
    except Exception as e:
        log(f"下载失败: {e}", "\033[31m")
        sys.exit(1)


def extract_python(archive: Path, dest: Path, is_zip: bool, keep_archive: bool = False):
    """解压Python - Windows直接解压到目标目录，Unix去除第一层目录"""
    log(f"解压到: {dest}", "\033[36m")
    dest.mkdir(parents=True, exist_ok=True)

    try:
        if is_zip:
            # Windows: ZIP文件直接解压到目标目录（确保文件在python文件夹根目录）
            with zipfile.ZipFile(archive, "r") as z:
                # 先解压到临时位置，检查结构
                temp_extract = dest.parent / f"temp_extract_{archive.stem}"
                if temp_extract.exists():
                    shutil.rmtree(temp_extract)
                temp_extract.mkdir(parents=True, exist_ok=True)

                try:
                    z.extractall(temp_extract)

                    # 检查是否只有一个子目录且该子目录包含python.exe
                    subdirs = [d for d in temp_extract.iterdir() if d.is_dir()]
                    files_in_root = [f for f in temp_extract.iterdir() if f.is_file()]

                    if subdirs and len(subdirs) == 1 and not files_in_root:
                        # 如果只有一个子目录，将子目录内容移动到目标目录
                        subdir = subdirs[0]
                        for item in subdir.rglob("*"):
                            if item.is_file():
                                relative_path = item.relative_to(subdir)
                                target_file = dest / relative_path
                                target_file.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(item, target_file)
                        shutil.rmtree(temp_extract)
                    else:
                        # 文件直接在根目录，移动到目标目录
                        for item in temp_extract.iterdir():
                            target = dest / item.name
                            if target.exists():
                                if target.is_file():
                                    target.unlink()
                                else:
                                    shutil.rmtree(target)
                            shutil.move(str(item), str(target))
                        temp_extract.rmdir()
                finally:
                    # 确保临时目录被清理
                    if temp_extract.exists():
                        shutil.rmtree(temp_extract, ignore_errors=True)
        else:
            # Unix: 使用tar解压并去除第一层目录
            if not shutil.which("tar"):
                log("错误: 未找到 tar 命令", "\033[31m")
                sys.exit(1)
            subprocess.run(
                ["tar", "-xzf", str(archive), "-C", str(dest), "--strip-components=1"],
                check=True,
            )
        log("解压完成", "\033[32m")
    except Exception as e:
        log(f"解压失败: {e}", "\033[31m")
        sys.exit(1)
    finally:
        # 只在不需要保留归档文件时删除
        if archive.exists() and not keep_archive:
            archive.unlink()


def find_python_exe(dest_dir: Path, exe_name: str) -> Optional[Path]:
    """查找Python可执行文件，如果不存在则返回None"""
    system = platform.system()

    if system == "Windows":
        # Windows: python-build-standalone 提供 python.exe
        possible_paths = [
            dest_dir / "python.exe",
            dest_dir / exe_name,
            dest_dir / "bin" / "python.exe",
            dest_dir / "bin" / exe_name,
        ]
    else:
        # Unix: 通常在 bin 目录
        possible_paths = [
            dest_dir / "bin" / exe_name,
            dest_dir / "bin" / "python",
            dest_dir / exe_name,
            dest_dir / "python",
        ]

    for exe_path in possible_paths:
        if exe_path.exists() and exe_path.is_file():
            # 设置执行权限（Unix）
            if system != "Windows":
                os.chmod(exe_path, 0o755)
            return exe_path.resolve()

    return None


def configure_windows_python(dest_dir: Path):
    """配置Windows Python的_pth文件"""
    pth_files = list(dest_dir.glob("python*._pth"))
    if not pth_files:
        log("警告: 未找到 _pth 文件，跳过配置", "\033[33m")
        return

    pth_file = pth_files[0]
    log(f"配置 _pth 文件: {pth_file.name}", "\033[36m")

    content = pth_file.read_text(encoding="utf-8")

    # 启用 import site
    content = content.replace("# import site", "import site")
    content = content.replace("#import site", "import site")

    # 添加搜索路径
    paths = [".", ".\\Lib", ".\\Lib\\site-packages", ".\\DLLs"]
    for path in paths:
        if path not in content:
            content += f"\n{path}"

    pth_file.write_text(content, encoding="utf-8", newline="\r\n")


def setup_pip(python_exe: Path, dest_dir: Path):
    """配置pip - 总是执行一次get-pip以确保pip正确安装"""
    # 下载get-pip.py到目标目录
    get_pip_path = dest_dir / "get-pip.py"

    log("下载get-pip.py...", "\033[36m")
    try:
        with urllib.request.urlopen(GET_PIP_URL) as response, open(
            get_pip_path, "wb"
        ) as f:
            shutil.copyfileobj(response, f)
    except Exception as e:
        log(f"下载get-pip.py失败: {e}", "\033[31m")
        sys.exit(1)

    # 执行get-pip.py安装/更新pip
    log("执行get-pip.py安装pip...", "\033[36m")
    try:
        subprocess.run([str(python_exe), str(get_pip_path.resolve())], check=True)

        # 验证pip是否安装成功
        result = subprocess.run(
            [str(python_exe), "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            log(f"pip安装成功: {result.stdout.strip()}", "\033[32m")
        else:
            log("警告: pip安装完成但无法验证版本", "\033[33m")
    except Exception as e:
        log(f"安装pip失败: {e}", "\033[31m")
        sys.exit(1)
    finally:
        # 清理get-pip.py
        if get_pip_path.exists():
            get_pip_path.unlink()


def main():
    """主函数"""
    log("=" * 50)
    log("Python嵌入式版本安装工具", "\033[36m")
    log("=" * 50)

    # 解析命令行参数
    if len(sys.argv) < 2:
        log("使用方法: python install_python.py <目标目录>", "\033[31m")
        log("示例: python install_python.py install/python", "\033[33m")
        sys.exit(1)

    dest_dir = Path(sys.argv[1]).resolve()
    log(f"目标目录: {dest_dir}", "\033[36m")

    # 获取下载信息
    python_url, archive_name, exe_name = get_python_url()

    # 检查是否已安装
    python_exe = find_python_exe(dest_dir, exe_name) if dest_dir.exists() else None
    if python_exe:
        log(f"Python已存在于: {dest_dir}", "\033[33m")
        setup_pip(python_exe, dest_dir)
        log("完成", "\033[32m")
        return

    # 下载Python
    archive_path = Path(archive_name)
    download_file(python_url, archive_path)

    # 解压Python
    is_zip = archive_name.endswith(".zip")
    extract_python(archive_path, dest_dir, is_zip)

    # 配置Python（Windows需要修改_pth文件）
    if platform.system() == "Windows":
        configure_windows_python(dest_dir)

    # 查找Python可执行文件
    python_exe = find_python_exe(dest_dir, exe_name)
    if not python_exe:
        log("错误: 未找到Python可执行文件", "\033[31m")
        sys.exit(1)

    # 配置pip
    setup_pip(python_exe, dest_dir)

    log("=" * 50)
    log("安装完成！", "\033[32m")
    log("=" * 50)


if __name__ == "__main__":
    main()
