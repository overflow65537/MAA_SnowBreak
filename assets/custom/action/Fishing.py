#from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction
import time

#@AgentServer.custom_action("Fishing")
class Fishing(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        image = context.tasker.controller.post_screencap().wait().get()
        result = context.run_recognition("检查黄色块数量", image)

        if result.best_result.count:
            initial_yellow_count = result.best_result.count
            yellow_count = result.best_result.count

        start_time = time.time()
        while time.time() - start_time < 2:
            if yellow_count < initial_yellow_count - 50:
                break

            image = context.tasker.controller.post_screencap().wait().get()
            result = context.run_recognition("检查黄色块数量", image)
            if not result:
                return CustomAction.RunResult(success=True)
            yellow_count = result.best_result.count

        context.tasker.controller.post_click(1171, 618).wait()

        return CustomAction.RunResult(success=True)
