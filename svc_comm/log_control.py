import logging


def get_log(name, log_set, level=logging.INFO, propagate=False):
    """
    获取日志句柄
    :param name:
    :param log_set:
    :param level:
    :return:
    """
    # 强制utf-8
    log_set['encoding'] = 'utf-8'
    log_set['mode'] = 'a'
    log_set['delay'] = True
    formatter = logging.Formatter(
        '%(asctime)s [pid=%(process)d request_id=%(request_id)s %(filename)s:%(lineno)s %(funcName)s %(levelname)s] %(message)s')

    # get a named channel
    log = logging.getLogger(name)
    log.propagate = propagate
    # 清理之前的handler避免写多份
    log.handlers.clear()
    log.setLevel(level)
    return log