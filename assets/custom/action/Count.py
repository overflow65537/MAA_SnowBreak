from maa.context import Context
from maa.custom_action import CustomAction
import json


class Count(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        argv: dict = json.loads(argv.custom_action_param)
        print(argv)
        if not argv:
            return CustomAction.RunResult(success=True)
        if argv.get("count") < argv.get("target_count"):
            argv["count"] += 1
            context.override_pipeline(
                {
                    argv.get("self"): {
                        "custom_action_param": argv,
                    },
                }
            )
        else:
            context.override_pipeline(
                {
                    argv.get("self"): {
                        "custom_action_param": {
                            "self": argv.get("self"),
                            "count": 0,
                            "target_count": argv.get("target_count"),
                            "next": argv.get("next"),
                        },
                    },
                }
            )
            context.run_task(argv.get("next"))

        return CustomAction.RunResult(success=True)
