from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import RecognitionDetail

class PuzzleClculate(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        image = context.tasker.controller.post_screencap().wait().get()
        
       # 识别拼图板
        board = context.run_recognition(
             "识别可放置区域",image
        )
        if board is None:
            return CustomAction.RunResult(success=True)
        
        puzzle_layout = self.parse_puzzle_layout(board)       
        print("拼图板布局:") 
        for row in puzzle_layout:
            print(row)
        return CustomAction.RunResult(success=True)
            
    def parse_puzzle_layout(self,recognition_data:RecognitionDetail):
        """
        解析识别到的棋子布局
        :param recognition_data: 识别结果数据
        :return: 二维数组表示的拼图板布局
        """
        # 初始化一个5行6列的矩阵,向内部填充0
        matrix = [[0 for _ in range(6)] for _ in range(5)]
        
        # 定义行和列的边界阈值
        row_y = [109, 219, 328, 437, 547]  # 5个行的y坐标
        col_x = [389, 497, 605, 714, 823, 932]  # 6个列的x坐标
        
        for item in recognition_data.filterd_results:
            x, y, w, h = item.box
            
            # 确定行索引 (y坐标匹配)
            try:
                row_idx = next(i for i, ry in enumerate(row_y) if ry - 50 <= y <= ry + 50)
            except StopIteration:
                continue
                
            # 确定列索引 (x坐标匹配)
            try:
                col_idx = next(i for i, cx in enumerate(col_x) if cx - 50 <= x <= cx + 50)
            except StopIteration:
                continue
                
            matrix[row_idx][col_idx] = 1
            
        return matrix