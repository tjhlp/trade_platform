import re

from svc_comm.host import *
from svc_comm.svc_util import *
from svc_comm.sys_code import *


class Model(object):

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

        for k, v in params.items():
            where_key.append("%s" % k + "=%s")
            where_value.append(v)

        sql = '''SELECT * FROM %s WHERE %s ORDER BY id DESC ''' % \
              (table_name, ' AND '.join(where_key))
        if limit:
            sql += ('%s' % limit)

        print(sql)
        result = self.mdb.db_query(sql, where_value)

        rsp = {}
        rsp['list'] = result
        return rsp


class Account(object):
    def __init__(self):
        self.model = Model()

    @url_module_report
    def account_add(self):
        params = {'name': (1, str), 'account_condition': (1, dict),
                  'account_attr': (1, int), 'user_id': (1, int)}
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(CODE_INPUT_PARAM_INVALID)

        # 业务逻辑
        js['account_condition'] = json_encode(js['account_condition'])
        user = self.model.my_insert('account', js)
        # 返回响应信息
        if not user:
            print('数据库插入失败')
            return code2rsp(CODE_ADD_ERROR)

        return code2rsp(CODE_SUCCESS)

    @url_module_report
    def account_list(self):
        params = {'name': (0, str), 'account_attr': (0, int), 'user_id': (1, int)}
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
        rsp = self.model.my_query('account', js, limit)
        # 返回响应信息
        if not rsp:
            return code2rsp(CODE_QUERY_ERROR)

        return dict2rsp(CODE_SUCCESS, rsp)

    @url_module_report
    def account_remove(self):
        params = {'id': (1, int)}
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(code)

        try:
            # 软删除，将状态置为删除
            sql = '''update account set state='删除' where id=%s'''
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
    def account_update(self):
        params = {'name': (0, str), 'account_condition': (0, dict),
                  'account_attr': (0, int), 'id': (1, int)}
        js, code = valid_body_js(params)
        if not js:
            logging.error('invalid param')
            return code2rsp(code)

        update = self.model.mdb.append_set_update(js, ['name', 'account_attr'], ['account_condition'])
        if not update:
            logging.error('invalid param')
            return code2rsp(CODE_INPUT_PARAM_INVALID, '')

        sql = '''update account ''' + update + ''' where id=%s'''
        print(sql)
        result = self.model.mdb.db_update(sql, [js['id']])
        rsp = {'affect': result}

        return dict2rsp(CODE_SUCCESS, rsp)


