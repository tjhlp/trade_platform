# -*- coding:utf-8 -*-
import logging
from flask import Blueprint
from svc_comm import log_control, host
from user.user_control import *


user_console = Blueprint('user', __name__)


def init_each_process():
    """
    子进程自己初始化句柄，避免从主进程继承
    :return:
    """
    log_control.get_log(None, host.LOG_SET, logging.INFO)


class User(object):
    """
    主进程的所有东西都会被子进程继承，尽量不要初始化太多东西
    """

    @classmethod
    def setup(cls, app):
        # log_control.get_log(None, host.LOG_SET, logging.INFO)
        logging.info('wsgi application[%s] setup' % host.APP_NAME)

        app.before_first_request(init_each_process)

        # 改变requests的特性
        # requests.adapters.DEFAULT_RETRIES = 1
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        User.add_urls(user_console)
        app.register_blueprint(user_console, url_prefix='/user')

    @classmethod
    def add_urls(cls, blue):

        user_info = UserInfo()

        post_urls = {
            # 用户模块
            '/register': user_info.add_user,
            '/list': user_info.user_list,
            '/remove': user_info.remove,
            '/update': user_info.update,
        }

        for url in post_urls:
            blue.add_url_rule(url, url.replace('/', '_'), post_urls[url], methods=('OPTIONS', 'POST'))






