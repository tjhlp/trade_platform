import re
import pymysql
from flask import make_response

# from svc_comm.mysql_control import MysqlUtil, MyDb, SimpleDb
from svc_comm.host import *
from svc_comm.svc_util import *
from svc_comm.sys_code import *


class Model(SimpleDb):
    T_USER = "user"

    def __init__(self):
        super().__init__(DB_ACCOUNT_RELEASE)

    def simple_where_parse(self, where, table_name=None):
        """where条件解析，仅支持=和in操作, 各条件用and连接"""
        where_tpl = []
        where_value = []
        for k, v in where.items():
            if table_name:
                k = "%s.%s" % (table_name, k)
            if isinstance(v, list):
                if v:
                    tpl = "%s in (%s)" % (k, ",".join(["%s"] * len(v)))
                    where_tpl.append(tpl)
                    where_value += v
            else:
                # 默认操作符
                tpl = "%s = %%s" % (k)
                where_tpl.append(tpl)
                where_value.append(v)
        return " and ".join(where_tpl), where_value

    def my_insert(self, table_name, params, re_conn=True):
        if not isinstance(table_name, str) or not isinstance(params, dict):
            raise ValueError("param error")

        key = []
        value_holder = []
        value = []
        for k, v in params.items():
            key.append('`%s`' % k)
            value_holder.append('%s')
            value.append(v)

        sql = 'INSERT INTO `%s`(%s) values(%s)' % (
            table_name, ','.join(key), ','.join(value_holder))

        # 事务中不能打开重连
        if re_conn:
            re_conn = False

        last_insert_id = super().db_insert(sql, value, re_conn)
        print('last_wind:%s', last_insert_id)
        return last_insert_id

    def my_query(self, table_name, params, limit):

        where_value = []
        where_key = []

        if 'name' in params:
            where_key.append('name=%s')
            where_value.append(params['name'])


        sql = '''SELECT * FROM %s WHERE %s ORDER BY id DESC %s''' % \
              (table_name, ' AND '.join(where_key), limit)

        result = super().db_query(sql, where_value)

        for x in result:
            x['name'] = json_decode(x['name'])
            x['mobile'] = json_decode(x['product'])

        rsp = {}
        rsp['list'] = result
        return rsp


class UserInfo(object):
    def __init__(self):
        self.model = Model()

    @url_module_report
    def add_user(self):
        params = {'name': (1, str), 'mobile': (1, str), 'password': (1, str),
                  'password2': (1, str)}
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(CODE_INPUT_PARAM_INVALID)

        # 验证请求参数
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', js['name']):
            return code2rsp(CODE_USERNAME_ERROR)
        if not re.match(r'^[a-zA-Z0-9]{6,20}$', js['password']):
            return code2rsp(CODE_PASSWORD_TYPE)
        if js['password'] != js['password2']:
            print('两次输入不同')
            return code2rsp(CODE_PASSWORD_CONSISTENT)
        del js['password2']
        if not re.match(r'^1[3-9]\d{9}$', js['mobile']):
            return code2rsp(CODE_MOBILE_TYPE)

        # # 业务逻辑
        user = self.model.my_insert('user', js)
        # 返回响应信息
        if not user:
            print('数据库插入失败')
            return code2rsp(CODE_ADD_ERROR)

        return code2rsp(CODE_SUCCESS)

    @url_module_report
    def user_list(self):
        params = {'name': (0, str), 'mobile': (0, str), 'page_index': (1, int), 'page_size': (1, int), }
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(CODE_INPUT_PARAM_INVALID)

        limit = self.model.append_limit(js['page_index'], js['page_size'])
        if not limit:
            return code2rsp(CODE_INVALID_PAGE_INDEX_SIZE)

        # # 业务逻辑
        user = self.model.my_query('user', js, limit)
        # 返回响应信息
        if not user:
            return code2rsp(CODE_QUERY_ERROR)

        return code2rsp(CODE_SUCCESS)
