import logging
import builtins


PRINT_LEVEL_NUM = 60
logging.addLevelName(PRINT_LEVEL_NUM, "PRINT")


def _log_print(self, message, *args, **kws):
    if self.isEnabledFor(PRINT_LEVEL_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(PRINT_LEVEL_NUM, message, args, **kws)


logging.Logger.print = _log_print


from shortesttrack_tools.logger.utils import get_prototype_logger
_script_logger = get_prototype_logger('script')


def _print(*args, sep=' ', end='\n', file=None):
    _script_logger.print(*args)


builtins.print = _print
