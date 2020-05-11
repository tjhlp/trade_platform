import logging
import threading
import pymysql
import decimal
import datetime

from svc_comm.host import DB_ACCOUNT_RELEASE


class SimpleDb(object):
    """简单的封装下db操作"""

    def __init__(self, mdb=DB_ACCOUNT_RELEASE):
        self.mdb = mdb
        self.conn = self.get_mysql_conn(mdb)

    def _parse_where(self, where):
        """解析sql的where子句，目前仅支持以and连接条件"""
        where_tpl = []
        where_value = []
        for k, v in where.items():
            if isinstance(v, list):
                where_tpl.append(
                    '%s in (%s)' % (k, ', '.join(['%s'] * len(v))))
                where_value += v
                continue
            if '=' not in k and '>' not in k and '<' not in k and 'like' not in k:
                where_tpl.append('%s=%s' % (k, '%s'))
            else:
                where_tpl.append('%s %s' % (k, '%s'))
            where_value.append(v)
        return " and ".join(where_tpl), where_value

    @classmethod
    def get_mysql_conn(cls, mdb):
        """
        简单的数据库实例连接池
        :param mdb:
        :return:
        """
        return pymysql.connect(**mdb)

    def ping(self, re_conn):
        """
        检测连接状态并且重连
        不要太早连接数据库，如果在主进程里就连接，会被子进程继承引起错误
        不建议外部主动调用，执行sql会默认调用
        :param re_conn: 是否重新连接
        :return:
        """
        # get mysql connection
        self.conn = self.get_mysql_conn(DB_ACCOUNT_RELEASE)
        if re_conn:
            self.conn.ping(reconnect=True)

    def _get_where(self, table_name, where, order_by=None, limit=None,
                   fields=None):
        '''
        只支持最基础的单表 select 查询
        :param table_name: 表名
        :param where: dict类型，where条件，样例-{'uin': '123456', 'visit_time>=': '2018-06-26'}
        :param order_by: dict，样例-{'order_item': 'visit_time', 'order_method': 'desc'}
        :param limit: dict，样例-{'offset': 0, 'length': 10}
        :return:
        '''
        if order_by and (
                'order_item' not in order_by or 'order_method' not in order_by or
                order_by['order_method'] not in [
                    'asc', 'desc']):
            order_by = None  # 格式有问题，直接不适用

        if limit and ('offset' not in limit or 'length' not in limit):
            limit = None  # 格式有问题，直接不适用

        if not isinstance(where, dict):
            raise ValueError("where is not dict type")
        where_tpl, where_value = self._parse_where(where)

        fields_str = '*'
        if fields:
            if isinstance(fields, list):
                fields_str = ','.join(fields)
            else:
                fields_str = fields

        if where_tpl:
            sql = 'select %s from %s where %s' % (
                fields_str, table_name, where_tpl)
        else:
            sql = 'select %s from %s ' % (fields_str, table_name)

        if order_by:
            sql += ' order by %s %s' % (
                order_by['order_item'], order_by['order_method'])
        if limit:
            sql += ' limit %s, %s'
            where_value.append(limit['offset'])
            where_value.append(limit['length'])

        # 不在事务中才能打开重连
        result = self.mdb.db_query(sql, where_value)
        return result

    def db_insert(self, operation, params=None, re_conn=True):
        """
        插入操作
        :param operation:
        :param params:
        :param re_conn:
        :return:
        使用样例
        sql = '''insert into t_v2_product(categoryid,name,product,last_modify)values(%s,%s,%s,%s)'''
        result = self.db_insert(sql, [js['categoryid'], js['name'], json_encode(js['product']), http_user_id()])
        """
        self.ping(re_conn)
        try:
            csr = self.conn.cursor()
            print('operation:%s', operation)
            print('params :%s', params)
            csr.execute(operation, tuple(params) if isinstance(params, list) else params)
            affect = csr.lastrowid
            csr.close()
            return affect
        except Exception as e:
            log_str = 'db_insert db got exception:%s, operation:%s, params:%s' % (str(e), operation, params)
            logging.error(log_str)
            raise



