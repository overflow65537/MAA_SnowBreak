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
            }
        count: 当前次数
        target_count: 目标次数
        next_node: 达到目标次数后执行的节点. 支持多个节点，按顺序执行.可以出现重复节点
        
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
            )
        else:
            context.override_pipeline(
                {
                    argv.node_name: {
                        "custom_action_param": {
                            "count": 0,
                            "target_count": argv_dict.get("target_count"),
                            "next_node": argv_dict.get("next_node"),
                        },
                    },
                }
            )
            for i in argv.get("next_node"):
                context.run_task(i)

        return CustomAction.RunResult(success=True)
