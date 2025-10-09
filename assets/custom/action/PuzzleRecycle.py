from maa.context import Context
from maa.custom_action import CustomAction
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import os
from datetime import datetime, timedelta
import json
import time

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class PuzzleRecycle(CustomAction):
    def __init__(self):
        super().__init__()
        self.logger = self._setup_logger()
        self._clear_old_logs()

    def _setup_logger(self):
        debug_dir = "debug"
        os.makedirs(debug_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d")
        log_file_name = f"custom_{timestamp}.log"
        log_file_path = os.path.join(debug_dir, log_file_name)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        logger.propagate = False

        file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def __del__(self):
        """清理日志记录器资源"""
        try:
            if hasattr(self, "logger") and self.logger:
                # 安全地关闭所有处理器
                for handler in self.logger.handlers[:]:
                    try:
                        handler.close()
                    except:
                        pass
                    self.logger.removeHandler(handler)
        except:
            # 避免在析构函数中抛出异常
            pass

    def _clear_old_logs(self):
        debug_dir = "debug"
        if not os.path.isdir(debug_dir):
            return

        three_days_ago = datetime.now() - timedelta(days=3)
        for root, dirs, files in os.walk(debug_dir):
            for file in files:
                if file.startswith("custom_") and file.endswith(".log"):
                    try:
                        timestamp_str = file.split("_")[1].split(".")[0]
                        file_time = datetime.strptime(timestamp_str, "%Y%m%d")
                        if file_time < three_days_ago:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            self.logger.info(f"已删除过期日志文件: {file_path}")
                    except Exception as e:
                        self.logger.error(f"处理文件 {file} 时出错: {e}")

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        min_retain = int(json.loads(argv.custom_action_param).get("min_retain", 15))
        image = context.tasker.controller.post_screencap().wait().get()

        roi_list = [
            [302, 290, 31, 22],
            [446, 290, 26, 22],
            [587, 290, 24, 21],
            [728, 289, 27, 25],
            [869, 289, 23, 25],
            [305, 411, 23, 21],
            [445, 411, 26, 23],
            [586, 410, 26, 24],
        ]
        PUZZLE_COUNT = [0] * 8
        for roi in roi_list:
            result = context.run_recognition(
                "识别碎片数量_回收", image, {"识别碎片数量_回收": {"roi": roi}}
            )
            if result:
                PUZZLE_COUNT[roi_list.index(roi)] = int(result.best_result.text)  # type: ignore
        self.logger.info(f"信源回收碎片数量总计{PUZZLE_COUNT}")

        recycle_count = self.recycle_fragments(PUZZLE_COUNT, min_retain)
        self.logger.info(f"信源回收待回收碎片数量总计{recycle_count}")

        for i in range(len(recycle_count)):
            if context.tasker.stopping:
                self.logger.info("任务已停止，不进行回收")
                break
            elif recycle_count[i] == 0:
                self.logger.info(f"信源回收碎片类型{i}数量不足，不进行回收")
                continue
            else:
                self.logger.info(
                    f"信源回收碎片类型{i}数量足够，进行回收,回收次数{recycle_count[i]}"
                )
                context.tasker.controller.post_click(roi_list[i][0], roi_list[i][1])
                time.sleep(0.5)
                for _ in range(recycle_count[i] - 1):
                    if context.tasker.stopping:
                        self.logger.info("任务已停止，不进行回收")
                        break
                    context.tasker.controller.post_click(835, 486)  # 添加按钮
                    time.sleep(0.5)
        self.logger.info("信源回收完成,等待确认")

        return CustomAction.RunResult(success=True)

    def recycle_fragments(self, fragment_counts: list, min_retain: int) -> list:
        """
        回收碎片方法：每种碎片保留最少数量后，其余凑5个一组回收
        """
        # 计算每种碎片可保留和可回收的数量
        retain = []
        recyclable = []
        for count in fragment_counts:
            if count >= min_retain:
                retain.append(min_retain)
                recyclable.append(count - min_retain)
            else:
                retain.append(count)
                recyclable.append(0)

        # 计算实际可回收的总数量
        total_recyclable = sum(recyclable)
        actual_recycle = (total_recyclable // 5) * 5

        new_recyclable = [0] * 8

        if actual_recycle == 0:
            return new_recyclable

        remaining = actual_recycle
        for i in range(8):
            if remaining <= 0:
                break
            take = min(recyclable[i], remaining)
            new_recyclable[i] = take
            remaining -= take

        return new_recyclable
