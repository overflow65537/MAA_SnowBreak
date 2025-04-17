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
        argv = json.loads(argv.custom_action_param)
        image: numpy.ndarray = context.tasker.controller.post_screencap().wait().get()

        height, width, _ = image.shape
        current_time = argv.get("type","")+"_"+ time.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
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
