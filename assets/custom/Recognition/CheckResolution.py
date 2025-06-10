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
MAA_SnowBreak 分辨率检查
作者:overflow65537
"""

from maa.context import Context
from maa.custom_recognition import CustomRecognition
import os
import chardet


class CheckResolution(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult | None:
        try:
            log_path = os.path.join(os.getcwd(), "debug", "maa.log")
            # 读取文件的前部分内容以检测编码
            with open(log_path, "rb") as raw_file:
                raw_data = raw_file.read(1024)
                result = chardet.detect(raw_data)
                encoding = result["encoding"]

            # 使用检测到的编码读取文件
            with open(log_path, "r", encoding=encoding, errors="replace") as file:
                lines = file.readlines()
                # 倒序
                lines.reverse()
                for line in lines:
                    if (
                        "[MtouchHelper.cpp][L29][MaaNS::CtrlUnitNs::MtouchHelper::read_info]"
                        in line
                    ):
                        # 提取 分辨率
                        parts = line.split()
                        width = int(parts[-3])
                        height = int(parts[-2])

                        # 计算比例是否为 16:9
                        ratio = width / height
                        target_ratio = 16 / 9
                        is_16_9 = abs(ratio - target_ratio) < 0.001
                        if is_16_9:
                            return CustomRecognition.AnalyzeResult(
                                box=[10, 10, 0, 0],
                                detail=f"分辨率为 {width}x{height}, 比例为 16:9",
                            )
                    elif "[MtouchHelper.cpp][L53][MaaNS::CtrlUnitNs::MtouchHelper::read_info]" in line:
                        width_start = line.find("display_width_=") + len("display_width_=")
                        width_end = line.find("]", width_start)
                        width = int(line[width_start:width_end])

                        height_start = line.find("display_height_=") + len("display_height_=")
                        height_end = line.find("]", height_start)
                        height = int(line[height_start:height_end])
                        # 计算比例是否为 16:9
                        ratio = width / height
                        target_ratio = 16 / 9
                        is_16_9 = abs(ratio - target_ratio) < 0.001
                        if is_16_9:
                            return CustomRecognition.AnalyzeResult(
                                box=[10, 10, 0, 0],
                                detail=f"分辨率为 {width}x{height}, 比例为 16:9",
                            )
                    else:
                        continue
            

            return None

        except Exception as e:
            return None
