from maa.context import Context
from maa.custom_action import CustomAction
import json


class Count(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        """
        自定义动作：
        custom_action_param:
            {
                "count": 0,
                "target_count": 10,
                "next_node": ["node1", "node2"],
                "else_node": ["node3"],
            }
        count: 当前次数
        target_count: 目标次数
        next_node: 达到目标次数后执行的节点. 支持多个节点，按顺序执行，可以出现重复节点，可以为空
        else_node: 未达到目标次数时执行的节点. 支持多个节点，按顺序执行，可以出现重复节点，可以为空
        """

        argv_dict: dict = json.loads(argv.custom_action_param)
        print(argv_dict)
        if not argv_dict:
            return CustomAction.RunResult(success=True)
        if argv_dict.get("count") <= argv_dict.get("target_count"):
            argv_dict["count"] += 1
            context.override_pipeline(
                {
                    argv.node_name: {
                        "custom_action_param": argv_dict,
                    },
                }
            ),
            if argv_dict.get("else_node",):
                if isinstance(argv_dict.get("else_node"), list):
                    for i in argv_dict.get("else_node",):
                        context.run_task(i)
                elif isinstance(argv_dict.get("else_node"), str):
                    context.run_task(argv_dict.get("else_node"))
        else:
            context.override_pipeline(
                {
                    argv.node_name: {
                        "custom_action_param": {
                            "count": 0,
                            "target_count": argv_dict.get("target_count"),
                            "else_node": argv_dict.get("else_node"),
                            "next_node": argv_dict.get("next_node"),
                        },
                    },
                }
            )
            if argv_dict.get("next_node",):
                if isinstance(argv_dict.get("next_node"), list):
                    for i in argv_dict.get("next_node"):
                        context.run_task(i)
                elif isinstance(argv_dict.get("next_node"), str):
                    context.run_task(argv_dict.get("next_node"))

        return CustomAction.RunResult(success=True)
