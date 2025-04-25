from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import RecognitionDetail
import time

blocks = [
    # 1号
    [
        [
            [1, 1],
            [1, 1],
        ]
    ],
    # 2号
    [
        [
            [2],
            [2],
            [2],
            [2],
        ],
        [
            [2, 2, 2, 2],
        ],
    ],
    # 3号
    [
        [
            [3, 3, 0],
            [0, 3, 3],
        ],
        [
            [0, 3],
            [3, 3],
            [3, 0],
        ],
    ],
    # 4号
    [
        [
            [0, 4, 4],
            [4, 4, 0],
        ],
        [
            [4, 0],
            [4, 4],
            [0, 4],
        ],
    ],
    # 5号
    [
        [
            [0, 5],
            [0, 5],
            [5, 5],
        ],
        [
            [5, 0, 0],
            [5, 5, 5],
        ],
        [
            [5, 5],
            [5, 0],
            [5, 0],
        ],
        [
            [5, 5, 5],
            [0, 0, 5],
        ],
    ],
    # 6号
    [
        [
            [6, 0],
            [6, 0],
            [6, 6],
        ],
        [
            [6, 6, 6],
            [6, 0, 0],
        ],
        [
            [6, 6],
            [0, 6],
            [0, 6],
        ],
        [
            [0, 0, 6],
            [6, 6, 6],
        ],
    ],
    # 7号
    [
        [
            [7, 7, 7],
            [0, 7, 0],
        ],
        [
            [0, 7],
            [7, 7],
            [0, 7],
        ],
        [
            [0, 7, 0],
            [7, 7, 7],
        ],
        [
            [7, 0],
            [7, 7],
            [7, 0],
        ],
    ],
    # 8号
    [
        [
            [0, 8, 0],
            [8, 8, 8],
            [0, 8, 0],
        ]
    ],
    # 9号
    [[[9]]],
    # 10号
    [
        [
            [10],
            [10],
        ],
        [
            [10, 10],
        ],
    ],
    # 11号
    [
        [
            [11, 0],
            [11, 11],
        ],
        [
            [11, 11],
            [11, 0],
        ],
        [
            [11, 11],
            [0, 11],
        ],
        [
            [0, 11],
            [11, 11],
        ],
    ],
]


class PuzzleSolver:
    def __init__(self):
        self.m = 0  # 棋盘行数
        self.n = 0  # 棋盘列数
        self.a = []  # 当前棋盘状态
        self.l = []  # 剩余拼图块数量
        self.res = []  # 解方案集合
        self.temp_solution = []  # 临时存储当前解块信息

    def solve(self, arr, num):
        """主求解入口"""
        self.res = []
        self.m = len(arr)
        self.n = len(arr[0]) if self.m > 0 else 0
        self.a = [row.copy() for row in arr]  # 深拷贝棋盘
        self.l = num.copy()  # 深拷贝剩余数量

        self.dfs(0)  # 从第一个格子开始搜索
        return self.res

    def can_place_block(self, x, y, b, d):
        """判断能否放置指定形状"""
        pat = blocks[b][d]
        # 计算形状的水平偏移量
        offset = 0
        while pat[0][offset] == 0:
            offset += 1
        y -= offset  # 调整起始列位置

        if y < 0:
            return False

        # 检查每个拼图块单元是否可放置
        for i in range(len(pat)):
            for j in range(len(pat[0])):
                if pat[i][j] != 0:
                    xi, yj = x + i, y + j
                    if xi >= self.m or yj >= self.n or self.a[xi][yj] != -1:
                        return False
        return True

    def place_block(self, x, y, b, d, v):
        """实际放置拼图块"""
        pat = blocks[b][d]
        offset = 0
        while pat[0][offset] == 0:
            offset += 1
        y -= offset

        # 标记棋盘位置
        for i in range(len(pat)):
            for j in range(len(pat[0])):
                if pat[i][j] != 0:
                    self.a[x + i][y + j] = v

    def dfs(self, p):
        """深度优先搜索核心"""
        # 终止条件：处理完所有格子
        if p == self.m * self.n:
            # 记录完整解（棋盘状态+块信息）
            self.res.append(
                {
                    "board": [row.copy() for row in self.a],
                    "blocks": self.temp_solution.copy(),
                }
            )
            return len(self.res) >= 10000

        x, y = divmod(p, self.n)  # 转换为二维坐标

        # 跳过已填充格子
        if self.a[x][y] != -1:
            return self.dfs(p + 1)

        # 尝试所有拼图块类型
        for b in range(len(blocks)):
            if self.l[b] <= 0:
                continue

            # 尝试所有旋转形态
            for d in range(len(blocks[b])):
                if not self.can_place_block(x, y, b, d):
                    continue

                # 计算实际放置坐标（考虑偏移）
                pat = blocks[b][d]
                offset = 0
                while pat[0][offset] == 0:
                    offset += 1
                actual_y = y - offset

                # 计算包围盒坐标
                rows = len(pat)
                cols = len(pat[0])
                begin_pos = (x, actual_y)  # 左上角坐标
                end_pos = (x + rows - 1, actual_y + cols - 1)  # 右下角坐标

                # 更新块信息记录方式
                block_info = {
                    "type": b,
                    "direction": d,
                    "begin_position": begin_pos,
                    "end_position": end_pos,
                }

                # 放置块并记录
                self.place_block(x, y, b, d, b + 1)
                self.l[b] -= 1
                self.temp_solution.append(block_info)

                if self.dfs(p + 1):
                    return True

                # 回溯时移除记录
                self.l[b] += 1
                self.place_block(x, y, b, d, -1)
                self.temp_solution.pop()

        return False


import logging
import os

os.makedirs("debug", exist_ok=True)

logging.basicConfig(
    filename="debug/custom.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
    encoding="utf-8",
)


class PuzzleClculate(CustomAction):
    def __init__(self):
        super().__init__()
        self.PUZZLE_COUNT = [0] * 11
        logging.info("=" * 80)
        logging.info("初始化拼图计算器，碎片数量数组重置")
        logging.info("=" * 80)

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        logging.info("开始执行拼图计算任务")
        image = context.tasker.controller.post_screencap().wait().get()

        # 识别拼图板
        logging.debug("尝试识别拼图板")
        board = context.run_recognition("识别可放置区域", image)
        if board is None:
            logging.warning("未识别到拼图板")
            return CustomAction.RunResult(success=True)

        puzzle_layout = self.parse_puzzle_layout(board)
        logging.info(
            "拼图板布局解析完成:\n%s", "\n".join(str(row) for row in puzzle_layout)
        )

        # 识别碎片
        logging.debug("开始识别碎片数量")
        self.get_puzzle_count(context)
        logging.debug("二次识别获取更多碎片")
        context.tasker.controller.post_swipe(200, 600, 200, 100, 500).wait()
        time.sleep(1)
        self.get_puzzle_count(context)
        context.tasker.controller.post_swipe(200, 150, 200, 600, 500).wait()
        logging.info("最终碎片数量: %s", self.PUZZLE_COUNT)

        # 初始化求解器
        logging.debug("初始化拼图求解器")
        solver = PuzzleSolver()
        solutions = solver.solve(puzzle_layout, self.PUZZLE_COUNT)

        if solutions:
            selected_solution = next(
                (s for s in solutions if any(8 in row for row in s["board"])),
                solutions[0],
            )
            logging.debug("选择方案：\n%s", "\n".join(str(row) for row in selected_solution["board"]))

            last_block = None
            need_reinit = False
            for block in selected_solution["blocks"]:
                
                if need_reinit:
                    logging.debug("需要重新初始化")
                    context.run_task("重新进入拼图")
                    time.sleep(1)
                    last_block = None
                    need_reinit = False
                logging.info(
                    "处理碎片 %d 方向 %d", block["type"] + 1, block["direction"]
                )
                image = context.tasker.controller.post_screencap().wait().get()
                piece = context.run_recognition(f"识别碎片{block['type']+1}", image)
                if piece is None and block["type"] + 1 >= 8:
                    print(f"未搜索到{block['type']+1}, 尝试向上滑动")
                    context.tasker.controller.post_swipe(200, 600, 200, 100, 500).wait()
                    time.sleep(1)  # 滑动后等待动画结束
                    image = context.tasker.controller.post_screencap().wait().get()
                    piece = context.run_recognition(f"识别碎片{block['type']+1}", image)
                    if piece is None:
                        print(f"无法识别碎片{block['type']+1}")
                        return CustomAction.RunResult(success=True)
                elif piece is None and block["type"] + 1 < 8:
                    print(f"未搜索到{block['type']+1}, 尝试向下滑动")
                    context.tasker.controller.post_swipe(200, 150, 200, 600, 500).wait()
                    time.sleep(1)  # 滑动后等待动画结束
                    image = context.tasker.controller.post_screencap().wait().get()
                    piece = context.run_recognition(f"识别碎片{block['type']+1}", image)
                    if piece is None:
                        print(f"无法识别碎片{block['type']+1}")
                        return CustomAction.RunResult(success=True)
                # 旋转
                if block["direction"] == 1:
                    need_reinit = True
                    print("旋转90度")
                    if last_block != block["type"]:
                        context.tasker.controller.post_click(
                            piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                        ).wait()
                        time.sleep(0.5)
                    context.tasker.controller.post_click(
                        piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                    ).wait()

                elif block["direction"] == 2:
                    need_reinit = True
                    print("旋转180度")
                    if last_block != block["type"]:
                        context.tasker.controller.post_click(
                            piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                        ).wait()
                        time.sleep(0.5)
                    context.tasker.controller.post_click(
                        piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                    ).wait()
                    time.sleep(0.5)
                    context.tasker.controller.post_click(
                        piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                    ).wait()
                elif block["direction"] == 3:
                    need_reinit = True
                    print("旋转270度")
                    if last_block != block["type"]:
                        context.tasker.controller.post_click(
                            piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                        ).wait()
                        time.sleep(0.5)
                    context.tasker.controller.post_click(
                        piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                    )
                    time.sleep(0.5)
                    context.tasker.controller.post_click(
                        piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                    ).wait()
                    time.sleep(0.5)
                    context.tasker.controller.post_click(
                        piece.best_result.box[0] + 10, piece.best_result.box[1] + 10
                    )
                time.sleep(1)

                # 计算中心点坐标
                end_x, end_y = self.convert_grid_to_coords(
                    block["begin_position"], block["end_position"]
                )
                begin_x, begin_y = piece.best_result.box[0], piece.best_result.box[1]

                # 7号碎片特殊处理
                if block["type"] + 1 == 7 and block["direction"] == 1:
                    end_y = end_y + 100
                elif block["type"] + 1 == 7 and block["direction"] == 3:
                    end_y = end_y - 100
                print(f"碎片{block['type']+1}中心点坐标: ({end_x}, {end_y})")
                # 最终滑动
                context.tasker.controller.post_swipe(
                    begin_x, begin_y, end_x, end_y, 1000
                ).wait()
                last_block = block["type"]
                time.sleep(1)
                """context.run_task("重新进入拼图")
                time.sleep(1)"""
        else:
            print("未找到解决方案")
            context.run_task("退出拼图")
            context.run_task("一会儿再见")
            context.run_task("返回主菜单_基地_custom")
            context.run_task("停止任务")
            return CustomAction.RunResult(success=True)
        context.run_task("重新进入拼图")

        return CustomAction.RunResult(success=True)

    def parse_puzzle_layout(self, recognition_data: RecognitionDetail):
        """解析拼图板布局"""
        # 使用常量定义棋盘尺寸
        ROWS, COLS = 5, 6
        matrix = [[0] * COLS for _ in range(ROWS)]

        # 坐标配置，确保行列索引正确
        ROW_Y = [109, 219, 328, 437, 547]
        COL_X = [389, 497, 605, 714, 823, 932]

        for item in recognition_data.filterd_results:
            x, y, w, h = item.box

            # 行列索引查找逻辑
            row_idx = next(
                (i for i, ry in enumerate(ROW_Y) if ry - 50 <= y <= ry + 50), None
            )
            col_idx = next(
                (i for i, cx in enumerate(COL_X) if cx - 50 <= x <= cx + 50), None
            )

            if row_idx is not None and col_idx is not None:
                matrix[row_idx][col_idx] = -1

        return matrix

    def get_puzzle_count(self, context: Context):
        """获取碎片数量"""
        logging.debug("更新碎片数量")
        image = context.tasker.controller.post_screencap().wait().get()
        for i in range(11):
            result = context.run_recognition(f"识别碎片{i+1}", image)
            if result is None:
                logging.debug("未识别到碎片 %d", i + 1)
            else:
                count = context.run_recognition(f"识别碎片{i+1}数量", image)
                if count is not None:
                    old_count = self.PUZZLE_COUNT[i]
                    self.PUZZLE_COUNT[i] = int(count.best_result.text)
                    logging.debug(
                        "更新碎片 %d 数量：%d → %d",
                        i + 1,
                        old_count,
                        self.PUZZLE_COUNT[i],
                    )

    def convert_grid_to_coords(self, begin_pos, end_pos):
        """将网格坐标转换为屏幕坐标。"""
        AREA = (382, 101, 656, 551)

        total_rows = 5
        total_cols = 6

        # 计算单个格子尺寸
        cell_width = AREA[2] / total_cols
        cell_height = AREA[3] / total_rows

        # 计算实际坐标范围
        min_x = AREA[0] + begin_pos[1] * cell_width
        max_x = AREA[0] + (end_pos[1] + 1) * cell_width
        min_y = AREA[1] + begin_pos[0] * cell_height
        max_y = AREA[1] + (end_pos[0] + 1) * cell_height

        # 返回中心点坐标（取整）
        return (int((min_x + max_x) / 2), int((min_y + max_y) / 2))
