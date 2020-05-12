from svc_comm.host import *


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
        print(params)
        for k, v in params.items():
            key.append('`%s`' % k)
            value_holder.append('%s')
            value.append(v)

        sql = 'INSERT INTO `%s`(%s) values(%s)' % (
            table_name, ','.join(key), ','.join(value_holder))

        # 事务中不能打开重连
        if re_conn:
            re_conn = False
        print(sql)
        last_insert_id = self.m_db.db_insert(sql, value, re_conn)

        return last_insert_id


# js = {'name': '123sdgfd', 'mobile': '15077131300', 'password': '123456789'}
# c = Model()
#
# c.my_insert('user', js)

import pymysql

mdb = {
    'host': '18.163.103.171',
    'port': 3306,
    'user': 'root',
    'password': 'mysql',
    'database': 'active',
    'charset': 'utf8',
    'autocommit': True,
    'connect_timeout': 3,
    'read_timeout': 10,
    'write_timeout': 5
}


from svc_comm.mysql_control import SimpleDb


class Test(SimpleDb):
    def __init__(self):
        super().__init__(DB_ACCOUNT_RELEASE)


    def get(self):
        sql = "INSERT INTO `user`(`name`,`mobile`,`password`) values(%s,%s,%s)"
        value = ['123sdgfd', '15077131300', '123456789']
        last_insert_id = super().db_insert(sql, value, True)
        return last_insert_id


# t = Test()
# t.get()


js = {'page_index':123, 'page_size':2}
js1 = {}
if 'page_index' and 'page_size' in js1:
    print(123)
if [1]:
    print(2222)
