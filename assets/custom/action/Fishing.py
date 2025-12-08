# Copyright (c) 2024-2025 MAA_SnowBreak
# Copyright (c) 2024 LaoZhuJackson (Original Project: https://github.com/LaoZhuJackson/SnowbreakAutoAssistant)
#
# This module is derived from the original project's fishing module: https://github.com/LaoZhuJackson/SnowbreakAutoAssistant/tree/main/app/modules/fishing
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
MAA_SnowBreak
MAA_SnowBreak 钓鱼识别器
作者:overflow65537
"""

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import ColorMatchResult, BoxAndCountResult
import time


# @AgentServer.custom_action("Fishing")
class Fishing(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        image = context.tasker.controller.post_screencap().wait().get()
        result = context.run_recognition("检查黄色块数量", image)

        initial_yellow_count = 0
        yellow_count = 0

        if (
            result
            and result.hit
            and result.best_result
            and isinstance(result.best_result, BoxAndCountResult)
        ):
            initial_yellow_count = result.best_result.count
            yellow_count = result.best_result.count

        start_time = time.time()
        while time.time() - start_time < 2:
            if yellow_count < initial_yellow_count - 50:
                break

            image = context.tasker.controller.post_screencap().wait().get()
            result = context.run_recognition("检查黄色块数量", image)
            if result is None or not result.hit:
                return CustomAction.RunResult(success=True)
            if result.best_result and isinstance(result.best_result, BoxAndCountResult):
                yellow_count = result.best_result.count

        context.tasker.controller.post_click(1171, 618).wait()

        return CustomAction.RunResult(success=True)
