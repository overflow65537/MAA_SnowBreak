from maa.context import Context
from maa.custom_action import CustomAction
import json


class PPOverride(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        argv = json.loads(argv.custom_action_param)
        if not argv:
            return CustomAction.RunResult(success=True)
        context.override_pipeline(argv)
        return CustomAction.RunResult(success=True)