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
MAA_SnowBreak 计数程序
作者:overflow65537
"""


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

        current_count = argv_dict.get("count", 0)
        target_count = argv_dict.get("target_count", 0)

        if current_count <= target_count:
            argv_dict["count"] = current_count + 1
            context.override_pipeline(
                {argv.node_name: {"custom_action_param": argv_dict}}
            )
            self._run_nodes(context, argv_dict.get("else_node"))
        else:
            context.override_pipeline(
                {
                    argv.node_name: {
                        "custom_action_param": {
                            "count": 0,
                            "target_count": target_count,
                            "else_node": argv_dict.get("else_node"),
                            "next_node": argv_dict.get("next_node"),
                        }
                    }
                }
            )
            self._run_nodes(context, argv_dict.get("next_node"))

        return CustomAction.RunResult(success=True)

    def _run_nodes(self, context: Context, nodes):
        """统一处理节点执行逻辑"""
        if not nodes:
            return
        if isinstance(nodes, str):
            nodes = [nodes]
        for node in nodes:
            context.run_task(node)
