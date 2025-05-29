# Copyright (c) 2024-2025 MAA_Punish
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
MAA_Punish
MAA_Punish 逻辑识别器
作者:overflow65537
"""

from maa.context import Context
from maa.custom_recognition import CustomRecognition
import json


class LOp(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        """
        逻辑识别器：
        custom_recognition_param:
            {
                "mode": and,
                "nodes": ["node1", ["node2"]],
            }
        mode: 模式 and 或者 or,默认为and
        nodes: 需要识别的节点,使用列表括起来为反转识别结果
        """
        image = argv.image
        param: dict = json.loads(argv.custom_recognition_param)
        mode: str = param.get("mode", "and")
        nodes: list = param.get("nodes", [])

        if mode == "and":
            for item in nodes:
                result = self._eval_node(item, context, image)
                if not result:
                    return
            return CustomRecognition.AnalyzeResult(
                box=(0, 0, 100, 100), detail=f"{nodes} used in {mode} success"
            )

        elif mode == "or":
            for item in nodes:
                result = self._eval_node(item, context, image)
                if result:
                    return CustomRecognition.AnalyzeResult(
                        box=(0, 0, 100, 100), detail=f"{nodes} used in {mode} success"
                    )
            return

        else:
            return

    def _eval_node(self, node, context: Context, image) -> bool:

        if isinstance(node, str):
            return bool(context.run_recognition(node, image))

        elif isinstance(node, list) and len(node) == 1:
            inner_node = node[0]
            return not bool(context.run_recognition(inner_node, image))
