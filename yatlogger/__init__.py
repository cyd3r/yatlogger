import sys
import logging
from logging import LogRecord
from pathlib import Path
from typing import Union
import telegram
from telegram.utils.helpers import escape_markdown
from .config import get_config


__version__ = '0.1.0'


class TelegramHandler(logging.Handler):
    "A logging handler that sends messages to Telegram"
    def __init__(self, session_name: str = None, level=logging.INFO,
                 config: Union[str, Path, dict] = None):
        """Create a new logging handler that sends messages to Telegram.

        `session_name` is a text that will be prepended to messages to be able
        to better identify the source of the message.
        
        `level` is the minimum logging level that the handler will react to.

        `config` can either by a directory or a `dict`.
        If `config` is a directory, the handler will try to find a file named
        `.yatlogger.json` in that directory or starting from there in any of
        the parent directories. If `config` is a `dict`, the handler will use
        it directly. If `config` is `None`, the handler will look for a config
        file starting from the current working directory.
        """
        super().__init__(level=level)

        self.session_name = session_name

        if config is None:
            config = get_config()
        elif not isinstance(config, dict):
            config = get_config(config)

        self.bot = telegram.Bot(token=config["token"])
        self.chat_ids = config["users"]

    def emit(self, record: LogRecord):
        message = escape_markdown(self.format(record), version=2)
        session_name = None
        if self.session_name is not None:
            session_name = escape_markdown(self.session_name, version=2)

        prepend = ""
        if record.levelno == logging.ERROR:
            if session_name is None:
                prepend = "*Error*\n"
            else:
                prepend = f"*Error in {session_name}*\n"
        elif session_name is not None:
            prepend = f"_{session_name}_\n"

        for chat_id in self.chat_ids:
            self.bot.send_message(chat_id=chat_id, text=prepend + message,
                                  parse_mode="MarkdownV2")


def register(session_name: str = None, logger_name: str = None,
             level=logging.INFO, config: Union[str, Path, dict] = None):
    """Helper function that calls both `register_logger` and
    `hook_exception_log`.
    
    The used logger will be returned."""
    logger = register_logger(session_name, logger_name, level, config)
    hook_exception_log(logger_name)
    return logger


def register_logger(session_name: str = None, logger_name: str = None,
                    level=logging.INFO, config: Union[str, Path, dict] = None):
    """Helper function to create a new `TelegramHandler` and adding it the
    logger with name `name`.

    The `level` and `config` arguments are passed to `TelegramHandler`.

    The used logger will be returned.
    """
    logger = logging.getLogger(name=logger_name)
    logger.addHandler(TelegramHandler(session_name=session_name, level=level,
                                      config=config))
    return logger


def hook_exception_log(logger_name: str = None):
    """Sets an except hook to `sys.excepthook` that forwards the exception
    value to `logger.error()`.
    `KeboardInterrupt` won't be logged."""
    logger = logging.getLogger(name=logger_name)

    def custom_hook(type, value, traceback):
        if not isinstance(type, KeyboardInterrupt):
            logger.error(value)
        sys.__excepthook__(type, value, traceback)
        
    sys.excepthook = custom_hook


class log_exceptions:
    """A context manager that logs unhandled exceptions to the given logger.

    ``` python
    with yatlogger.log_exceptions():
        try:
            # this error will not be logged
            raise ValueError("handled eror")
        except:
            pass

        # this error will be logged using logging.error()
        raise ValueError("unhandled error")
    ```
    """
    def __init__(self, logger_name: str = None):
        """Create a new `log_exception` context manager."""
        self.logger = logging.getLogger(logger_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None or isinstance(exc_type, KeyboardInterrupt):
            return

        self.logger.error(exc_value)
