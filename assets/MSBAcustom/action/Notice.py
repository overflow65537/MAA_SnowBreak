"""
MAA_SnowBreak
MAA_SnowBreak 通知
作者:overflow65537
"""

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import OCRResult
import json
import datetime


class Notice(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        param: dict = json.loads(argv.custom_action_param)
        action = param.get("action")
        if action == "set_Currency":
            image = context.tasker.controller.post_screencap().wait().get()
            Currency_reco = context.run_recognition("识别数据金", image)
            if (
                Currency_reco
                and Currency_reco.hit
                and isinstance(Currency_reco.best_result, OCRResult)
            ):
                Currency = Currency_reco.best_result.text

            else:
                Currency = "0"

            context.tasker.resource.override_pipeline(
                {"资源变量": {"focus": {"start_Currency": Currency}}}
            )
        elif action == "show_Currency":
            image = context.tasker.controller.post_screencap().wait().get()
            end_Currency_reco = context.run_recognition("识别数据金", image)

            if (
                end_Currency_reco
                and end_Currency_reco.hit
                and isinstance(end_Currency_reco.best_result, OCRResult)
            ):
                end_Currency = end_Currency_reco.best_result.text
            else:
                end_Currency = "0"

            energy_reco = context.run_recognition("识别体力", image)

            if (
                energy_reco
                and energy_reco.hit
                and isinstance(energy_reco.best_result, OCRResult)
            ):
                energy = energy_reco.best_result.text
            else:
                energy = "0"

            resource = context.get_node_object("资源变量")
            if resource is None:
                return CustomAction.RunResult(success=False)
            start_Currency = resource.focus.get("start_Currency")

            # 收益
            if start_Currency.isdigit() and end_Currency.isdigit() and energy.isdigit():
                profit = int(end_Currency) - int(start_Currency)
                next_energy = 240 - int(energy) * 6 * 60

                now_time = datetime.datetime.now()
                next_time = now_time + datetime.timedelta(seconds=next_energy)
                self.custom_notify(context, "初始数据金:")
                self.custom_notify(context, start_Currency)
                self.custom_notify(context, "当前数据金:")
                self.custom_notify(context, end_Currency)
                self.custom_notify(context, "收益:")
                self.custom_notify(context, str(profit))
                self.custom_notify(context, "下次体力恢复时间:")
                self.custom_notify(context, next_time.strftime("%Y-%m-%d %H:%M:%S"))

        return CustomAction.RunResult(success=True)

    def custom_notify(self, context: Context, msg: str):
        """自定义通知"""
        context.override_pipeline(
            {"custom通知": {"focus": {"Node.Recognition.Succeeded": msg}}}
        )
        context.run_task("custom通知")
