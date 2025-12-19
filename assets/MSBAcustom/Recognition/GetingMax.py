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
MAA_SnowBreak 寻找最大值
作者:overflow65537
"""

from maa.context import Context
from maa.custom_recognition import CustomRecognition


class GetingMax(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult | None:
        image = argv.image

        roi_list = [
            [34, 187, 30, 20],
            [196, 187, 30, 20],
            [34, 308, 30, 20],
            [196, 308, 30, 20],
            [34, 429, 30, 20],
            [196, 429, 30, 20],
            [34, 550, 30, 20],
            [196, 550, 30, 20],
        ]
        max_val = 0
        max_reco = None
        for roi in roi_list:
            result = context.run_recognition(
                "识别碎片数量", image, {"识别碎片数量": {"roi": roi}}
            )

            if result is None or not result.hit or not result.best_result:
                continue
            if result.best_result.text.isdigit():  # type: ignore
                digit_val = int(result.best_result.text)  # type: ignore
                if digit_val > max_val:
                    max_val = digit_val
                    max_reco = result.best_result
        if max_reco is None:
            return None
        return CustomRecognition.AnalyzeResult(
            box=max_reco.box, detail={"max":f"最大值为{max_reco.text}"}   # type: ignore
        )
