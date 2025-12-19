import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime, timedelta

class Logger:
    def __init__(self,  name: str = ""):
        """
        初始化日志记录器
        
        Args:
            component_name (str): 组件名称，默认为"CombatActions"
            role_name (str): 角色名称，用于日志标识
        """
        self.name = name
        self.logger = self._create_logger()
        self._clear_old_logs()
    
    def _create_logger(self):
        """
        创建并配置日志记录器
        
        Returns:
            logging.Logger: 配置好的日志记录器实例
        """
        # 创建特定名称的日志记录器
        logger_name = self.name
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        
        # 禁止日志传播到父记录器
        logger.propagate = False
        
        # 清除可能已存在的处理器
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        
        # 创建日志目录
        log_path = Path("debug") / "custom.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建文件和控制台处理器
        file_handler = TimedRotatingFileHandler(
            log_path,
            when="midnight",
            backupCount=3,
            encoding="utf-8",
        )
        stream_handler = logging.StreamHandler()
        
        # 设置日志格式
        name_tag = f"|{self.name}|" if self.name else ""
        LOG_FORMAT = f"[%(asctime)s][%(levelname)s][%(filename)s][L%(lineno)d][%(funcName)s] {name_tag} %(message)s"
        
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
        return logger
    
    def _clear_old_logs(self):
        """
        清理3天前的旧日志文件
        支持清理 custom_YYYYMMDD.log 格式的日志文件
        """
        debug_dir = Path("debug")
        if not debug_dir.is_dir():
            return
        
        three_days_ago = datetime.now() - timedelta(days=3)
        for file in debug_dir.iterdir():
            if file.is_file() and file.name.startswith("custom_") and file.name.endswith(".log"):
                try:
                    # 尝试从文件名中提取日期
                    timestamp_str = file.name.split("_")[1].split(".")[0]
                    file_time = datetime.strptime(timestamp_str, "%Y%m%d")
                    if file_time < three_days_ago:
                        file.unlink()
                        self.logger.info(f"已删除过期日志文件: {file}")
                except (ValueError, IndexError):
                    # 如果文件名格式不正确，跳过
                    pass
                except Exception as e:
                    self.logger.error(f"处理文件 {file.name} 时出错: {e}")
    
    def __del__(self):
        """
        对象被销毁时清理日志记录器资源
        """
        try:
            if hasattr(self, "logger") and self.logger:
                # 关闭并移除所有处理器
                for handler in self.logger.handlers[:]:
                    handler.close()
                    self.logger.removeHandler(handler)
                
                # 从logging模块中移除该日志记录器
                logger_name = self.name
                if logger_name in logging.Logger.manager.loggerDict:
                    del logging.Logger.manager.loggerDict[logger_name]
        except Exception as e:
            # 避免在析构函数中抛出异常
            pass
    
    def get_logger(self):
        """
        获取配置好的日志记录器实例
        
        Returns:
            logging.Logger: 日志记录器实例
        """
        return self.logger
    