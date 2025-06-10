import os
if not os.path.exists("run_cli.py"):
    os.environ["MAAFW_BINARY_PATH"] = os.getcwd()
from maa.toolkit import Toolkit

from maa.context import Context
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition

import sys
print("如无必要，请使用MFW.exe运行")
print("if not necessary, please use MFW.exe to run")
#创建一个logger
import logging
import os
import importlib.util
from typing import Dict
import logging
import os
from logging.handlers import TimedRotatingFileHandler



def Read_Config(file_path):
    """
    读取配置文件
    """
    import json

    with open(file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

def path_to_list(path):
    """将路径转换为列表形式"""
    parts = []
    while True:
        path, part = os.path.split(path)
        if part:
            parts.insert(0, part)
        else:
            if path:
                parts.insert(0, path)
            break
    return parts


os.makedirs("debug", exist_ok=True)
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(filename)s][L%(lineno)d][%(funcName)s] | %(message)s",
    level=logging.DEBUG,
    handlers=[
        TimedRotatingFileHandler(
            os.path.join(os.getcwd(), "debug", "picli.log"),
            when="midnight",
            backupCount=3,
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)



def load_custom_objects(custom_dir):

    if not os.path.exists(custom_dir):
        logger.warning(f"自定义文件夹 {custom_dir} 不存在")
        return
    if not os.listdir(custom_dir):
        logger.warning(f"自定义文件夹 {custom_dir} 为空")
        return
    if os.path.exists(os.path.join(custom_dir, "custom.json")):
        logger.info("配置文件方案")
        custom_config: Dict[str, Dict] = Read_Config(
            os.path.join(custom_dir, "custom.json")
        )
        for custom_name, custom in custom_config.items():
            custom_type: str = custom.get("type", "")
            custom_class_name: str = custom.get("class", "")
            custom_file_path: str = custom.get("file_path", "")
            if "{custom_path}" in custom_file_path:
                custom_file_path = custom_file_path.replace(
                    "{custom_path}", custom_dir
                )
                custom_file_path = os.path.join(*path_to_list(custom_file_path))

            if not all(
                [custom_type, custom_name, custom_class_name, custom_file_path]
            ):
                logger.warning(f"配置项 {custom} 缺少必要信息，跳过")
                continue
            print(
                f"custom_type: {custom_type}, custom_name: {custom_name}, custom_class_name: {custom_class_name}, custom_file_path: {custom_file_path}"
            )
            module_name = os.path.splitext(os.path.basename(custom_file_path))[0]
            # 动态导入模块
            spec = importlib.util.spec_from_file_location(
                module_name, custom_file_path
            )
            if spec is None:
                logger.error(f"无法获取模块 {module_name} 的 spec，跳过加载")
                continue
            module = importlib.util.module_from_spec(spec)

            if spec.loader is None:
                logger.error(f"模块 {module_name} 的 loader 为 None，跳过加载")
                continue
            spec.loader.exec_module(module)
            print(f"模块 {module} 导入成功")

            # 获取类对象
            class_obj = getattr(module, custom_class_name)

            # 实例化类
            instance = class_obj()

            if custom_type == "action":
                if Toolkit.pi_register_custom_action(custom_name, instance):
                    logger.info(f"加载自定义动作{custom_name}")
            elif custom_type == "recognition":
                if Toolkit.pi_register_custom_recognition(custom_name, instance):
                    logger.info(f"加载自定义识别器{custom_name}")

def main():
    # 注册自定义动作
    load_custom_objects(os.path.join(os.getcwd(), "custom"))

    # 注册自定义识别

    directly = "-d" in sys.argv
    Toolkit.pi_run_cli("./", "./", directly)


if __name__ == "__main__":
    main()
