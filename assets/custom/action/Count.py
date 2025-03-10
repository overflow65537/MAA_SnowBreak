from maa.context import Context
from maa.custom_action import CustomAction
import json


class Count(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        argv: dict = json.loads(argv.custom_action_param)
        print(argv)
        if argv.get("Count") < 100:
            argv["Count"] += 1
            context.override_pipeline(
                {
                    "黑屏计数": {"custom_action_param": argv},
                }
            )
        else:
            context.run_task("重启游戏")

        return CustomAction.RunResult(
            success=True
        )
