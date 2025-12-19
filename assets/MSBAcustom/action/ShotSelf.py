# Copyright (c) 2024-2025 MAA_SnowBreak
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
MAA_SnowBreak 水弹活动射击判断
作者:overflow65537
"""

# from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction
import time


class ShotSelf(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        image = context.tasker.controller.post_screencap().wait().get()
        item = context.run_recognition("展开道具", image)
        if item and item.hit and item.best_result:
            x, y = (
                item.best_result.box[0] + item.best_result.box[2] // 2,
                item.best_result.box[1] + item.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            image = context.tasker.controller.post_screencap().wait().get()
        health = context.run_recognition("生命值缺失", image)
        health_gem = context.run_recognition("检查活力宝石", image)
        if (
            health
            and health_gem
            and health.hit
            and health_gem.hit
            and health.best_result
            and health_gem.best_result
        ):
            x, y = (
                health_gem.best_result.box[0] + health_gem.best_result.box[2] // 2,
                health_gem.best_result.box[1] + health_gem.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(1)
            image = context.tasker.controller.post_screencap().wait().get()
        lock = context.run_recognition("检查手铐", image)
        lock_status = context.run_recognition("检查手铐状态", image)
        if (lock and lock.hit and lock.best_result) and not (
            lock_status and not lock_status.hit
        ):
            x, y = (
                lock.best_result.box[0] + lock.best_result.box[2] // 2,
                lock.best_result.box[1] + lock.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(1)
            image = context.tasker.controller.post_screencap().wait().get()
        reversal = context.run_recognition("检查逆转魔术", image)
        if reversal and reversal.hit and reversal.best_result:
            x, y = (
                reversal.best_result.box[0] + reversal.best_result.box[2] // 2,
                reversal.best_result.box[1] + reversal.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(1)
            barrel = context.run_recognition("检查枪管", image)
            if barrel and barrel.hit and barrel.best_result:
                x, y = (
                    barrel.best_result.box[0] + barrel.best_result.box[2] // 2,
                    barrel.best_result.box[1] + barrel.best_result.box[3] // 2,
                )
                context.tasker.controller.post_click(x, y).wait()
                time.sleep(1)
                context.run_task("使用道具")
                time.sleep(1)
            context.run_task("向对方开枪")
            return CustomAction.RunResult(success=True)
        context.run_task("向自己开枪")
        return CustomAction.RunResult(success=True)
