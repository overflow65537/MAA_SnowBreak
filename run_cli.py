import os
if not os.path.exists("run_cli.py"):
    os.environ["MAAFW_BINARY_PATH"] = os.getcwd()

from assets.custom.action.Fishing.main import Fishing
from assets.custom.action.ShotTarget.main import ShotTarget
from assets.custom.action.ScreenShot.main import ScreenShot
from assets.custom.action.ShotSelf.main import ShotSelf

from maa.toolkit import Toolkit

import sys

def main():
    # 注册自定义动作
    Toolkit.pi_register_custom_action("Fishing", Fishing())
    Toolkit.pi_register_custom_action("ShotTarget", ShotTarget())
    Toolkit.pi_register_custom_action("ScreenShot", ScreenShot())
    Toolkit.pi_register_custom_action("ShotSelf", ShotSelf())

    # 注册自定义识别

    directly = "-d" in sys.argv
    Toolkit.pi_run_cli("./", "./", directly)


if __name__ == "__main__":
    main()
