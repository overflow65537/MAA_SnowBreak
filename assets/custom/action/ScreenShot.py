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
MAA_SnowBreak 截图程序
作者:overflow65537
"""

from maa.context import Context
from maa.custom_action import CustomAction
import os
import time
import struct
import zlib
import numpy
import json


class ScreenShot(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        argv: dict = json.loads(argv.custom_action_param)
        image: numpy.ndarray = context.tasker.controller.post_screencap().wait().get()

        debug_dir = os.path.abspath("debug")
        three_days_ago = time.time() - 3 * 24 * 3600
        if os.path.exists(debug_dir):
            for entry in os.scandir(debug_dir):
                if (
                    entry.is_file()
                    and entry.name.lower().endswith(".png")
                    and entry.stat(follow_symlinks=False).st_mtime < three_days_ago
                ):
                    try:
                        os.remove(entry.path)
                    except:
                        pass

        height, width, _ = image.shape
        current_time = (
            argv.get("type", "") + "_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        )
        debug_path = os.path.join("debug", current_time)

        def png_chunk(chunk_type, data):
            chunk = chunk_type + data
            return (
                struct.pack("!I", len(data))
                + chunk
                + struct.pack("!I", zlib.crc32(chunk))
            )

        # Convert BGR to RGB
        image = image[:, :, [2, 1, 0]]

        raw_data = b"".join(b"\x00" + image[i, :, :].tobytes() for i in range(height))
        ihdr = struct.pack("!2I5B", width, height, 8, 2, 0, 0, 0)
        idat = zlib.compress(raw_data, level=9)

        with open(debug_path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            f.write(png_chunk(b"IHDR", ihdr))
            f.write(png_chunk(b"IDAT", idat))
            f.write(png_chunk(b"IEND", b""))

        return CustomAction.RunResult(success=True)
