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

from maa.context import Context
from maa.custom_action import CustomAction
import time


# @AgentServer.custom_action("ShotTarget")
class ShotTarget(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        shot_chance = argv.custom_action_param
        print(bool(shot_chance))
        image = context.tasker.controller.post_screencap().wait().get()
        item = context.run_recognition("展开道具", image)
        if item:
            x, y = (
                item.best_result.box[0] + item.best_result.box[2] // 2,
                item.best_result.box[1] + item.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            image = context.tasker.controller.post_screencap().wait().get()

        # reset = context.run_recognition("检查重置之锤", image)
        eject = context.run_recognition("检查退弹布偶", image)
        empty = context.run_recognition(
            "检查子弹_custom", image, {"检查子弹_custom": {"roi": [1067, 651, 25, 33]}}
        )
        water = context.run_recognition(
            "检查子弹_custom", image, {"检查子弹_custom": {"roi": [988, 652, 25, 34]}}
        )

        has_eject = bool(eject)
        is_not_shot_chance_true = argv.custom_action_param != '{"shot_chance":true}'
        if water and empty:
            has_bullets = (
                int(water.best_result.text) != 0 and int(empty.best_result.text) != 0
            )
        else:
            has_bullets = False

        if has_eject and is_not_shot_chance_true and has_bullets:
            eject_count = len(eject.filterd_results)

            bullet_count = int(water.best_result.text) + int(empty.best_result.text)
            print(f"子弹数量:{bullet_count}")
            print(f"退弹数量:{eject_count}")
            if eject_count >= bullet_count - 1:
                print("开始退弹")
                while (not int(water.best_result.text) == 0) and (
                    not int(empty.best_result.text) == 0
                ):
                    x, y = (
                        eject.best_result.box[0] + eject.best_result.box[2] // 2,
                        eject.best_result.box[1] + eject.best_result.box[3] // 2,
                    )
                    context.tasker.controller.post_click(x, y).wait()
                    print(f"点击{x},{y}")
                    time.sleep(1)
                    print("开始重新装填")
                    context.run_task("使用道具")
                    time.sleep(1)
                    image = context.tasker.controller.post_screencap().wait().get()
                    empty = context.run_recognition(
                        "检查子弹_custom",
                        image,
                        {"检查子弹_custom": {"roi": [1067, 651, 25, 33]}},
                    )  # 空弹数量
                    water = context.run_recognition(
                        "检查子弹_custom",
                        image,
                        {"检查子弹_custom": {"roi": [988, 652, 25, 34]}},
                    )  # 水弹数量
                    eject = context.run_recognition("检查退弹布偶", image)
                if int(water.best_result.text) == 0:
                    context.run_task("向自己开枪_custom"),
                    return CustomAction.RunResult(success=True)
                elif int(empty.best_result.text) == 0:
                    context.run_task("向对方开枪_custom_100")
                    return CustomAction.RunResult(success=True)
                else:
                    return CustomAction.RunResult(success=True)

        """if reset and eject: #有重置之锤和退弹布偶就直接用
            x, y = (
                reset.best_result.box[0] + reset.best_result.box[2] // 2,
                reset.best_result.box[1] + reset.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            context.run_task("使用道具")
            time.sleep(1)
            image = context.tasker.controller.post_screencap().wait().get()
            eject_steal = context.run_recognition("检查退弹布偶_偷", image)
            if eject_steal :
                sorted_results = sorted(eject_steal.filterd_results, key=lambda x: x.score, reverse=True)
                target_list = [result.box for result in sorted_results[:4]] # 按照得分从高到低排序，取前4个
                for box in target_list:
                    x = (box[0] + box[2]) // 2
                    y = (box[1] + box[3]) // 2
                    context.tasker.controller.post_click(x, y).wait()
                    time.sleep(0.5)
                context.run_task("确定偷窃道具") #其实就是点击确定
            else:
                context.tasker.controller.post_click(10, 10).wait()"""

        health = context.run_recognition("生命值缺失", image)
        health_gem = context.run_recognition("检查活力宝石", image)
        if health and health_gem:

            x, y = (
                health_gem.best_result.box[0] + health_gem.best_result.box[2] // 2,
                health_gem.best_result.box[1] + health_gem.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(0.5)
            image = context.tasker.controller.post_screencap().wait().get()
        lock = context.run_recognition("检查手铐", image)
        lock_status = context.run_recognition("检查手铐状态", image)
        if lock and not (lock_status):
            x, y = (
                lock.best_result.box[0] + lock.best_result.box[2] // 2,
                lock.best_result.box[1] + lock.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(0.5)
            image = context.tasker.controller.post_screencap().wait().get()
        barrel = context.run_recognition("检查枪管", image)
        if barrel and argv.custom_action_param == '{"shot_chance":true}':
            x, y = (
                barrel.best_result.box[0] + barrel.best_result.box[2] // 2,
                barrel.best_result.box[1] + barrel.best_result.box[3] // 2,
            )
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(1)
            context.run_task("使用道具")
            time.sleep(0.5)
        context.run_task("向对方开枪")
        return CustomAction.RunResult(success=True)
