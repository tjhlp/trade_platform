# -*- coding:utf-8 -*-
import logging
import requests
from flask import Blueprint
from svc_comm import log_control, host
# from account.api_account import AccountInfo


account_console = Blueprint('account_console', __name__)


def init_each_process():
    """
    子进程自己初始化句柄，避免从主进程继承
    :return:
    """
    log_control.get_log(None, host.LOG_SET, logging.INFO)


class Account(object):
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
        Account.add_urls(account_console)
        app.register_blueprint(account_console, url_prefix='/account_console')

    @classmethod
    def add_urls(cls, blue):

        # api_account = AccountInfo()


        post_urls = {

            # '/account/add': api_account.account_add,
        }

        for url in post_urls:
            blue.add_url_rule(url, url.replace('/', '_'), post_urls[url], methods=('OPTIONS', 'POST'))






