"""
MAA_Punish
MAA_Punish pipeline 兑换码程序
作者:overflow65537
"""

import re
from maa.context import Context
from maa.custom_action import CustomAction
import json
import time
from pathlib import Path


class RedeemCode(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        pipeline_obj = context.get_node_data("可以输入兑换码")
        if pipeline_obj is None:
            self.send_msg(context, "兑换码节点不存在")
            return CustomAction.RunResult(success=False)
        param = (
            pipeline_obj.get("action", {})
            .get("param", {})
            .get("custom_action_param", {})
        )

        # 读取工作目录下的兑换码文件
        inv_code_path = Path("inv_code.json")
        if not inv_code_path.exists():
            inv_code = []
        else:
            with open("inv_code.json", "r") as f:
                data = json.load(f)
                if data is None:
                    inv_code = []
                else:
                    inv_code = data.get("inv_code", [])

        for code in param["code"]:
            if code in inv_code:
                continue
            else:
                context.run_task("点击兑换码")
                time.sleep(0.1)
                print(code)

                self.send_msg(context, f"开始兑换 {code}")
                print(f"输入兑换码 {code}")
                context.tasker.controller.post_input_text(str(code))
                time.sleep(0.1)
                context.run_task("确定")

                inv_code.append(code)
                with open("inv_code.json", "w") as f:
                    json.dump({"inv_code": inv_code}, f, indent=4)

                return CustomAction.RunResult(success=True)

        self.send_msg(context, "所有兑换码已兑换")
        context.override_next("兑换码", ["返回主菜单" ])
        return CustomAction.RunResult(success=True)

    def send_msg(self, context: Context, msg: str):
        msg_node = {
            "发送消息_这是程序自动生成的node所以故意写的很长来防止某一天想不开用了这个名字导致报错": {
                "focus": {"Node.Recognition.Succeeded": msg}
            }
        }
        context.run_task(
            "发送消息_这是程序自动生成的node所以故意写的很长来防止某一天想不开用了这个名字导致报错",
            pipeline_override=msg_node,
        )


class CheckRedeemCode(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        pipeline_obj = context.get_node_data("可以输入兑换码")
        if pipeline_obj is None:
            context.override_next("兑换码", [])
            return CustomAction.RunResult(success=False)
        param = (
            pipeline_obj.get("action", {})
            .get("param", {})
            .get("custom_action_param", {})
        )

        # 读取工作目录下的兑换码文件
        inv_code_path = Path("inv_code.json")
        if not inv_code_path.exists():
            inv_code = []
        else:
            with open("inv_code.json", "r") as f:
                data = json.load(f)
                if data is None:
                    inv_code = []
                else:
                    inv_code = data.get("inv_code", [])

        for code in param["code"]:
            if code in inv_code:
                continue
            else:
                context.override_next(
                    "兑换码",
                    [
                        "[JumpBack]可以输入兑换码",
                        "[JumpBack]前往兑换",
                        "[JumpBack]打开其他设置",
                        "[JumpBack]设置_滑动",
                        "[JumpBack]打开设置",
                        "[JumpBack]关闭奖励通知",
                        "[JumpBack]返回主菜单",
                    ],
                )
                print(f"兑换码 {code} 未兑换")
                return CustomAction.RunResult(success=True)

        print("所有兑换码均已兑换")

        context.override_next("兑换码", [])
        return CustomAction.RunResult(success=True)
