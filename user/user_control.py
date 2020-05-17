import re

from svc_comm.host import *
from svc_comm.svc_util import *
from svc_comm.sys_code import *


class Model(object):
    T_USER = "user"

    def __init__(self):
        self.mdb = SimpleDb()

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

        last_insert_id = self.mdb.db_insert(sql, value, re_conn)
        return last_insert_id

    def my_query(self, table_name, params, limit):

        where_key = ['state=%s']
        where_value = ['正常']

        if 'name' in params:
            where_key.append('name=%s')
            where_value.append(params['name'])

        if 'mobile' in params:
            where_key.append('mobile=%s')
            where_value.append(params['mobile'])

        sql = '''SELECT * FROM %s WHERE %s ORDER BY id DESC ''' % \
              (table_name, ' AND '.join(where_key))
        if limit:
            sql += ('%s' % limit)
        result = self.mdb.db_query(sql, where_value)
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
        account = self.model.my_insert('account', {'name': js['name']})

        # 返回响应信息
        if not (user and account):
            print('数据库插入失败')
            return code2rsp(CODE_ADD_ERROR)

        return code2rsp(CODE_SUCCESS)

    @url_module_report
    def user_list(self):
        params = {'id': (1, int), 'name': (0, str), 'mobile': (0, str), 'page_index': (1, int), 'page_size': (1, int)}
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(CODE_INPUT_PARAM_INVALID)

        limit = None
        if 'page_index' and 'page_size' in js:
            limit = self.model.mdb.append_limit(js['page_index'], js['page_size'])
            if not limit:
                return code2rsp(CODE_INVALID_PAGE_INDEX_SIZE)

        # # 业务逻辑
        rsp = self.model.my_query('user', js, limit)
        # 返回响应信息
        if not rsp:
            return code2rsp(CODE_QUERY_ERROR)

        return dict2rsp(CODE_SUCCESS, rsp)

    @url_module_report
    def login(self):
        params = {'name': (0, str), 'mobile': (0, str), 'password': (1, str)}
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(CODE_INPUT_PARAM_INVALID)

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', js['name']):
            if not re.match(r'^[a-zA-Z0-9]{6,20}$', js['mobile']):
                return code2rsp(CODE_PASSWORD_TYPE)
        rsp = self.model.my_query('user', js, None)
        get_password = rsp['list'][0]['password']

        if get_password != js['password']:
            return code2rsp(CODE_PASSWORD_ERROR)

        return code2rsp(CODE_SUCCESS)

    @url_module_report
    def remove(self):
        params = {'id': (1, int)}
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(code)

        try:
            # 软删除，将状态置为删除
            sql = '''update user set state='删除' where id=%s'''
            result = self.model.mdb.db_update(sql, [js['id']])
            self.model.mdb.db_commit()
            rsp = {'affect': result}
            return dict2rsp(CODE_SUCCESS, rsp)
        except Exception as e:
            self.model.mdb.db_rollback()
            logging.error("exception: %s", str(e))
            logging.info("delete %s failed" % js['id'])
            return code2rsp(CODE_ACTION_FAILED)

    @url_module_report
    def update(self):
        params = {'id': (0, int), 'name': (0, str), 'mobile': (0, str)}
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(code)

        update = self.model.mdb.append_set_update(js, ['id', 'name', 'mobile'], [])
        if not update:
            logging.error('invalid param')
            return code2rsp(CODE_INPUT_PARAM_INVALID, '')

        sql = '''update user ''' + update + ''' where id=%s'''
        result = self.model.mdb.db_update(sql, [js['id']])
        rsp = {'affect': result}

        return dict2rsp(CODE_SUCCESS, rsp)
