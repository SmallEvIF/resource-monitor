import logging
import os
import uuid
from datetime import datetime

from colorama import Fore, Style

LOG_COLOR_PRE = {
    'DEBUG': Fore.WHITE,
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.MAGENTA + Style.BRIGHT
}
LOG_COLOR_END = Style.RESET_ALL


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # 获取当前日志级别的颜色
        color = LOG_COLOR_PRE.get(record.levelname, '')
        # 格式化日志消息并添加颜色
        formatted_message = super().format(record)
        return f"{color}{formatted_message}{LOG_COLOR_END}"


class MyLogger(logging.Logger, metaclass=type):

    def __init__(
            self,
            name,
            level=logging.DEBUG,
            log_path=None
    ):
        super().__init__(name, level)
        self.head = ""
        self.log_path = log_path or os.path.join(os.path.dirname(__file__), "logs")
        self._init()

    def _init(self):
        os.makedirs(self.log_path, exist_ok=True)
        self._init_handlers()

    def _init_handlers(self):
        format_style = f'%(asctime)s <{self.head}> [%(name)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
        color_formatter = ColoredFormatter(format_style, datefmt='%Y-%m-%d %H:%M:%S')
        file_formatter = logging.Formatter(format_style, datefmt='%Y-%m-%d %H:%M:%S')
        file_name = os.path.join(self.log_path, f'{self.name}_{datetime.now().strftime("%Y%m%d")}.log')
        self.handlers = []
        # 创建文件处理器并设置日志格式
        file_handler = logging.FileHandler(file_name, encoding='utf-8')
        file_handler.setLevel(self.level)  # 文件日志级别为INFO
        file_handler.setFormatter(file_formatter)

        # 创建控制台处理器并设置日志格式
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)  # 控制台日志级别为DEBUG
        console_handler.setFormatter(color_formatter)

        # 将处理器添加到logger
        self.addHandler(file_handler)
        self.addHandler(console_handler)

    def set_head(self, head):
        self.head = head
        self._init_handlers()

    def setLevel(self, level):
        super().setLevel(level)
        self._init_handlers()


if __name__ == "__main__":
    logger = MyLogger("cookie")
    logger.info("This is an info message.")
    logger.debug("This is an info message.")
    logger.warning("This is an info message.")
    logger.error("This is an info message.")
    logger.error("\n")
    logger.set_head(str(uuid.uuid4()))
    logger.info("This is an info message.")
    logger.debug("This is an info message.")
    logger.warning("This is an info message.")
    logger.error("This is an info message.")
    logger.error("\n")
    logger.setLevel(logging.WARNING)
    logger.info("This is an info message.")
    logger.debug("This is an info message.")
    logger.warning("This is an info message.")
    logger.error("This is an info message.")
