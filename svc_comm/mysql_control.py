import logging
import threading
import pymysql
import decimal
import datetime

from svc_comm import host


class MysqlUtil(object):
    """
    访问mysql的一些常用功能，通过参数绑定来防止sql注入
    使用方法
    db = MysqlUtil(连接配置)
    result = db.db_query('select * from x where id=%s', [1])
    affect = db.db_update('update x set id=%s where id=%s', [1, 2])
    """

    """
    注意直接与db相关的操作不能吞没异常，否则调用方可能无法区分出错误，比如之前db_update
    这个函数之前抛异常时返回0， 但考虑到执行成功也有可能返回0，例如affect = 0的情况
    """

    def __init__(self, mdb):
        self.mdb = mdb
        self.conn = None

    @classmethod
    def db_instance_name(cls, mdb):
        return '%s_%s_%s' % (mdb['host'], mdb['port'], mdb['database'])

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
        self.conn = self.get_mysql_conn(self.mdb)
        if re_conn:
            self.conn.ping(reconnect=True)

    @classmethod
    def __json_type(cls, v):
        """
        mysql的浮点数Decimal，各种日期时间类型，json转换默认都不支持，需要特别处理
        :param v:
        :return:
        """
        if isinstance(v, decimal.Decimal):
            return str(v)
        elif isinstance(v, datetime.datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(v, datetime.date):
            return v.strftime('%Y-%m-%d')
        elif isinstance(v, datetime.timedelta):
            h, remain = divmod(int(v.total_seconds()), 3600)
            m, s = divmod(remain, 60)
            return '%02d:%02d:%02d' % (h, m, s)
        return v

    def db_query(self, operation, params=None, dict_format=True, re_conn=True):
        """
        查询结果集合默认返回字典的列表
        :param operation:
        :param params:
        :param dict_format: False 返回tuple列表
        :param re_conn:
        :return:
        使用样例
        sql = '''select id,name from t_v2_activity'''
        result = self.db_query(sql)
        rsp = {x['id']: x['name'] for x in result}
        """
        self.ping(re_conn)

        try:
            csr = self.conn.cursor(cursor=pymysql.cursors.DictCursor if dict_format else None)
            csr.execute(operation, tuple(params) if isinstance(params, list) else params)
            r = csr.fetchall()
            # 系统自带的json序列化不支持很多mysql类型,自行先转
            for i in range(0, len(r)):
                if dict_format:
                    for k, v in r[i].items():
                        r[i][k] = self.__json_type(v)
                else:
                    # tuple只能全部替换
                    r[i] = tuple(map(lambda x: self.__json_type(x), r[i]))
            csr.close()
            return r
        except Exception as e:
            log_str = 'db_query db got exception:%s, operation:%s, params:%s' % (str(e), operation, params)
            logging.error(log_str)
            raise


class SimpleDb(object):
    """简单的封装下db操作"""

    def __init__(self, db_config):
        self.m_db = MysqlUtil(db_config)
        self._init_state()

    def _init_state(self):
        """初始化state thread local"""
        self._state = threading.local()
        # in_tx属性记录是否在事务中
        self._state.in_tx = False

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
        result = self.m_db.db_query(sql, where_value)
        return result


class MyDb(SimpleDb):

    def __init__(self, db_config_name=host.DB_ACCOUNT_RELEASE):
        SimpleDb.__init__(self, db_config_name)