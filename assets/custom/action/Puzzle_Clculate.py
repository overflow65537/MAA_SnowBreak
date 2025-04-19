from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import RecognitionDetail
import time

blocks = [
    [[[1, 1], [1, 1]]],
    [[[2, 2, 2, 2]], [[2], [2], [2], [2]]],
    [[[3, 3, 0], [0, 3, 3]], [[0, 3], [3, 3], [3, 0]]],
    [[[0, 4, 4], [4, 4, 0]], [[4, 0], [4, 4], [0, 4]]],
    [
        [[5, 0, 0], [5, 5, 5]],
        [[5, 5], [5, 0], [5, 0]],
        [[5, 5, 5], [0, 0, 5]],
        [[0, 5], [0, 5], [5, 5]],
    ],
    [
        [[0, 0, 6], [6, 6, 6]],
        [[6, 6], [0, 6], [0, 6]],
        [[6, 6, 6], [6, 0, 0]],
        [[6, 0], [6, 0], [6, 6]],
    ],
    [
        [[0, 7, 0], [7, 7, 7]],
        [[7, 7, 7], [0, 7, 0]],
        [[7, 0], [7, 7], [7, 0]],
        [[0, 7], [7, 7], [0, 7]],
    ],
    [[[0, 8, 0], [8, 8, 8], [0, 8, 0]]],
    [[[9]]],
    [[[10, 10]], [[10], [10]]],
    [
        [[11, 11], [11, 0]],
        [[11, 11], [0, 11]],
        [[0, 11], [11, 11]],
        [[11, 0], [11, 11]],
    ],
]


class PuzzleSolver:
    def __init__(self):
        self.m = 0  # 棋盘行数
        self.n = 0  # 棋盘列数
        self.a = []  # 当前棋盘状态
        self.l = []  # 剩余拼图块数量
        self.res = []  # 解方案集合

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
            self.res.append([row.copy() for row in self.a])
            if len(self.res) >= 10000:
                print("方案数过多，仅保留前10000种")
                return True
            return False

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

                # 放置拼图块并递归搜索
                self.place_block(x, y, b, d, b + 1)
                self.l[b] -= 1
                if self.dfs(p + 1):
                    return True

                # 回溯恢复状态
                self.l[b] += 1
                self.place_block(x, y, b, d, -1)

        return False


class PuzzleClculate(CustomAction):
    def __init__(self):
        super().__init__()
        # 初始化拼图数量数组，每个元素代表对应类型的拼图数量
        self.PUZZLE_COUNT = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        image = context.tasker.controller.post_screencap().wait().get()

        # 识别拼图板
        board = context.run_recognition("识别可放置区域", image)
        if board is None:
            return CustomAction.RunResult(success=True)

        puzzle_layout = self.parse_puzzle_layout(board)
        print("拼图板布局:")
        for row in puzzle_layout:
            print(row)

        # 识别碎片
        self.get_puzzle_count(context)
        context.tasker.controller.post_swipe(200, 600, 200, 100, 500).wait()
        time.sleep(1)  # 滑动后等待动画结束
        self.get_puzzle_count(context)
        print("碎片数量:")
        for idx, count in enumerate(self.PUZZLE_COUNT):
            print(f"碎片{idx}: {count}")

        # 初始化求解器
        solver = PuzzleSolver()
        solutions = solver.solve(puzzle_layout, self.PUZZLE_COUNT)
        if solutions:
            # 打印前十个解决方案
            for i in range(min(10, len(solutions))):
                print(f"解决方案 {i+1}:")
                for row in solutions[i]:
                    print(row)
        else:
            print("未找到解决方案")
            return CustomAction.RunResult(success=True)

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
        image = context.tasker.controller.post_screencap().wait().get()
        PUZZLE_TYPES = 11  # 碎片类型总数

        pieces = {
            i: (
                context.run_recognition(f"识别碎片{i}", image),
                context.run_recognition(f"识别碎片{i}数量", image),
            )
            for i in range(1, PUZZLE_TYPES + 1)
        }

        for idx, (_, count_result) in pieces.items():
            if count_result and count_result.filterd_results:
                try:
                    self.PUZZLE_COUNT[idx - 1] = int(
                        count_result.filterd_results[0].text
                    )
                except (ValueError, IndexError) as e:
                    print(f"碎片{idx}数量识别错误: {str(e)}")
