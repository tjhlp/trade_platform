from svc_comm.mysql_control import MysqlUtil, MyDb
from svc_comm.host import *
from svc_comm.svc_util import *


class UserInfo(MysqlUtil):
    def __init__(self):
        MysqlUtil.__init__(self, DB_ACCOUNT_RELEASE)

        self.my_db = MyDb()

    @url_module_report
    def user_add(self):

        return '11111'

