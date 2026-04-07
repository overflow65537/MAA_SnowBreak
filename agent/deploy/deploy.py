"""
部署前检查和依赖安装模块
在运行main之前检查并安装必要的Python库
"""

import io
import json
import logging
import subprocess
import sys
from pathlib import Path

# 强制 stdout/stderr 使用 UTF-8，避免 Windows cp1252 下中文日志/print 报 UnicodeEncodeError
if hasattr(sys.stdout, "buffer") and getattr(
    sys.stdout, "encoding", ""
).lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "buffer") and getattr(
    sys.stderr, "encoding", ""
).lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 尝试导入 jsonc，优先使用 jsonc
try:
    import jsonc

    USE_JSONC = True
except ImportError:
    USE_JSONC = False
    # 如果 jsonc 不存在，说明依赖还没安装，需要直接安装


def setup_logger():
    """配置日志系统，同时输出到控制台和文件"""
    # 获取日志文件路径：__file__ 的上3层目录中的 debug/deploy.log
    # __file__ = ./agent/deploy/deploy.py
    # parent = ./agent/deploy/
    # parent.parent = ./agent/
    # parent.parent.parent = ./
    # 所以日志文件路径 = ./debug/deploy.log
    log_dir = Path(__file__).parent.parent.parent / "debug"
    log_file = log_dir / "deploy.log"

    # 创建 logger
    logger = logging.getLogger("deploy")
    logger.setLevel(logging.INFO)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 创建格式器
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 文件处理器（追加模式）
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# 初始化日志
logger = setup_logger()


def get_main_py_path():
    """获取main.py的路径（作为基准路径）"""
    # 获取当前文件的目录
    current_file = Path(__file__).resolve()
    # 当前文件在 agent/deploy/deploy.py
    # main.py 在 agent/main.py，即 ../main.py
    main_py_path = current_file.parent.parent / "main.py"
    return main_py_path


def get_interface_version():
    """从interface.json中读取版本号（需要 jsonc 支持）"""
    if not USE_JSONC:
        raise ImportError("jsonc 未安装，无法读取 interface.json")

    # 以 main.py 为基准路径
    main_py_path = get_main_py_path()
    # interface.json 在 assets/interface.json，从 main.py 看是 ../assets/interface.json
    interface_path = main_py_path.parent.parent / "interface.json"

    if not interface_path.exists():
        raise FileNotFoundError(f"无法找到 interface.json 文件: {interface_path}")

    try:
        with open(interface_path, "r", encoding="utf-8") as f:
            # 使用 jsonc 库处理带注释的 JSON
            import jsonc

            interface_data = jsonc.load(f)

            version = interface_data.get("version")

            if version is None:
                raise ValueError("interface.json 中未找到 version 字段")

            return str(version)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"解析 interface.json 失败: {e}")


def get_saved_version():
    """读取已保存的版本号"""
    version_file = Path(__file__).parent / ".version"

    if not version_file.exists():
        return None

    try:
        with open(version_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        logger.warning(f"读取版本文件失败: {e}")
        return None


def save_version(version):
    """保存版本号到文件"""
    version_file = Path(__file__).parent / ".version"

    try:
        with open(version_file, "w", encoding="utf-8") as f:
            f.write(version)
    except Exception as e:
        logger.warning(f"保存版本文件失败: {e}")


def load_requirements_from_file():
    """从requirements.txt读取依赖列表（必须存在）"""
    # 以 main.py 为基准路径
    main_py_path = get_main_py_path()
    # requirements.txt 在 main.py 上层目录，即 ../requirements.txt
    requirements_path = main_py_path.parent.parent / "requirements.txt"

    if not requirements_path.exists():
        print(f"error: 无法找到 requirements.txt 文件: {requirements_path}")
        raise FileNotFoundError(f"无法找到 requirements.txt 文件: {requirements_path}")

    packages = []
    try:
        with open(requirements_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith("#"):
                    continue
                # 保留完整的包名和版本号
                packages.append(line)

        if not packages:
            print(f"error: requirements.txt 文件中没有找到任何依赖包")
            raise ValueError("requirements.txt 文件中没有找到任何依赖包")

        return packages
    except Exception as e:
        print(f"error: 读取 requirements.txt 失败: {e}")
        raise ValueError(f"读取 requirements.txt 失败: {e}")


def install_package_with_fallback(package_spec):
    """
    尝试使用多个源安装包，按顺序回退
    1. 清华源
    2. 阿里源
    3. PyPI 官方源
    """
    sources = [
        ("阿里源", "https://mirrors.aliyun.com/pypi/simple/"),
        ("清华源", "https://pypi.tuna.tsinghua.edu.cn/simple"),
        ("PyPI官方源", "https://pypi.org/simple"),
    ]

    last_error = None
    for source_name, source_url in sources:
        try:
            logger.info(f"尝试使用 {source_name} 安装 {package_spec}...")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "-i",
                    source_url,
                    package_spec,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info(f"✓ {package_spec} 安装成功 (使用 {source_name})")
            # 记录 pip 输出（如果有）
            if result.stdout:
                logger.debug(f"pip 输出: {result.stdout}")
                print(f"info: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            last_error = e
            logger.warning(
                f"使用 {source_name} 安装 {package_spec} 失败，尝试下一个源..."
            )
            print(
                f"error: 使用 {source_name} 安装 {package_spec} 失败，尝试下一个源..."
            )
            if e.stderr:
                logger.debug(f"  错误输出: {e.stderr}")
            if e.stdout:
                logger.debug(f"  标准输出: {e.stdout}")
            # 继续尝试下一个源

    # 所有源都失败了
    logger.error(f"✗ {package_spec} 安装失败（所有源都尝试失败）:")
    if last_error:
        logger.error(f"  最后错误输出: {last_error.stderr}")
        if last_error.stdout:
            logger.debug(f"  最后标准输出: {last_error.stdout}")
    return False


def check_and_install_dependencies():
    """检查并安装必要的依赖库"""
    # 从 requirements.txt 读取所有依赖
    print("info: 开始安装依赖")
    required_packages = load_requirements_from_file()
    if not required_packages:
        raise ValueError("requirements.txt 中没有找到任何依赖包")

    all_installed = True

    for package_spec in required_packages:
        logger.info(f"正在安装 {package_spec}...")
        print(f"info: 正在安装 {package_spec}...")
        success = install_package_with_fallback(package_spec)
        if not success:
            all_installed = False

    return all_installed


def deploy():
    """主部署检查函数"""
    logger.info("=" * 50)
    logger.info("开始部署前检查...")
    logger.info("=" * 50)
    print("info:开始部署检查")

    try:
        # 如果 jsonc 不存在，说明依赖还没安装，直接安装
        if not USE_JSONC:
            logger.info("检测到 jsonc 未安装，跳过版本检查，直接安装依赖...")
            logger.info("开始安装依赖库...")
            success = check_and_install_dependencies()

            if success:
                logger.info("✓ 依赖安装完成")
            else:
                logger.error("✗ 依赖安装失败，请手动安装后重试")
                return False

            logger.info("=" * 50)
            return True

        # jsonc 存在，进行版本检查
        # 读取当前版本
        current_version = get_interface_version()
        logger.info(f"当前 interface_version: {current_version}")

        # 读取已保存的版本
        saved_version = get_saved_version()

        if saved_version == current_version:
            logger.info(f"版本一致 (v{saved_version})，跳过依赖检查")
            logger.info("=" * 50)
            print("info: 版本一致，跳过依赖检查")
            return True

        if saved_version:
            logger.info(f"版本已更新: {saved_version} -> {current_version}")
        else:
            logger.info("首次运行，开始依赖检查...")

        # 检查并安装依赖
        logger.info("开始检查依赖库...")
        success = check_and_install_dependencies()

        if success:
            # 保存新版本
            save_version(current_version)
            logger.info(f"✓ 依赖检查完成，版本已更新为: {current_version}")
        else:
            logger.error("✗ 依赖安装失败，请手动安装后重试")
            return False

        logger.info("=" * 50)
        return True

    except Exception as e:
        logger.error(f"✗ 部署检查过程中发生错误: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
