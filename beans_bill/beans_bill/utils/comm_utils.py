import logging
import json
import datetime

from beans_bill.utils import response_code
from django.http import JsonResponse
import decimal
logger = logging.getLogger('django')


def map_length():
    len_map = {
        "ownNodeID": 8, "sourceName": 60, "openName": 60,
        "status": 1,
    }
    return len_map


def valid_body_js(request, params):
    """
    先检查request的请求参数，然后转化为python对象
    :param params: {'page_index': 1, 'page_size': 1, 'id': 0, 'name': 0} 1表示必选参数，0表示可选参数
    {'page_index': (1, int), 'page_size': (1, int), 'id': (0, int), 'name': (0, str)} 判断可选的同时判断类型
    :return: python对象，处理结果CODE_SUCCESS表示成功
    使用样例
    params = {'page_index': 1, 'page_size': 1, 'id': 0, 'name': 0}
    js, code = self.valid_body_js(params)
    if code != CODE_SUCCESS:
        logging.error('invalid param')
    """

    try:
        raw_body = request.body
        all_js = json.loads(raw_body)

        # 空json是允许的{}
        if not isinstance(all_js, dict):
            return None, response_code.CODE_INVALID_JSON
        if params:
            must = set()
            option = set()
            for k, v in params.items():
                if isinstance(v, tuple):
                    # 第一个是可选项，第二个是类型
                    param_option = v[0]
                    if k in all_js and not isinstance(all_js[k], v[1]):
                        logger.debug('invalid param type:%s' % k)
                        return None, response_code.CODE_INPUT_PARAM_INVALID_TYPE
                    # 验证字符串长度
                    if k in all_js and v[1] == str:
                        str_len = map_length()
                        if k in str_len and len(all_js[k]) > str_len[k]:
                            return None, response_code.CODE_STRING_LENGTH_ERROR
                else:
                    param_option = v
                if param_option:
                    must.add(k)
                else:
                    option.add(k)

            if must and not must.issubset(set(all_js.keys())):
                logger.debug('must params:%s, now params:%s, difference:%s' % (
                    must, set(all_js.keys()), must.difference(set(all_js.keys()))))
                return None, response_code.CODE_INPUT_PARAM_MISS

        return all_js, response_code.CODE_SUCCESS

    except Exception as e:
        logger.debug('parser json got exception:%s' % str(e))
        return None, response_code.CODE_INPUT_PARAM_INVALID


def json_response(code, return_value=None):
    """json数据返回"""

    all_js = {
        'errCod': code[0],
        'errMsg': code[1]
    }
    if return_value:
        all_js['data'] = return_value
    return JsonResponse(all_js)


def append_limit(page_index, page_size, max_length=500):
    """
    根据分页参数生成limit字段'limit 1,2'
    :param page_index: 第几页，从1开始
    :param page_size: 每一页大小
    :return:
    """
    if not isinstance(page_index, int) or not isinstance(page_size, int) or page_index <= 0 or page_size <= 0:
        logging.info('invalid page_index or page_size')
        return ''

    # 一次最多查询500，保证安全
    if page_size > max_length:
        page_size = max_length

    start = (page_index - 1) * page_size
    return ' limit %s,%s' % (start, page_size)


def parse_json_sql(table_name, js):
    """
    解析json 转化为sql语句
    :param table_name: 数据库名
    :param js: json数据
    :return:
    """
    insert_element = []
    insert_values = []
    sql_create_table = "CREATE TABLE " + table_name + " (id int NOT NULL auto_increment,"
    for filed in js['selectedFiled']:
        tmp_field = filed["field_name"] + ' ' + filed["field_type"] + ' NOT NULL,'
        sql_create_table += tmp_field

        insert_element.append("%s" % filed["field_name"])
        insert_values.append("%s")
    else:
        sql_create_table += '  PRIMARY KEY (`id`))CHARSET=utf8mb4'

    sql_insert = 'INSERT INTO `%s`(%s) values(%s)' % (
        table_name, ','.join(insert_element), ','.join(insert_values))

    insert_data = []
    # executemany 需要元组
    for value in js['selectedValue']:
        insert_data.append(tuple(value))

    return sql_insert, sql_create_table, insert_data


def generate_insert_sql(source_ID, js):
    """
    生成插入sql语句
    :param source_ID: 数据源表的ID
    :param js: json数据
    :return:
    """
    # 数据源字段表的字段
    insert_field_element = ["Table_ID", "Field_ID", "Field_Type", "Field_Name",
                            "Open_Status", "Crt_Time", "Upd_Time"]
    insert_field_values = "%s, %s, %s, %s, %s, %s, %s"

    sql_insert_field = 'INSERT INTO `TAB_SOURCE_FIELD`(%s) values(%s)' % (
        ','.join(insert_field_element), insert_field_values)

    insert_field_data = []
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for filed in js['selectedFiled']:
        tmp_tuple = (
            source_ID, filed["field_name"], filed["field_type"], filed["field_name"], 'Y',
            time_now, time_now,
        )
        insert_field_data.append(tmp_tuple)

    return sql_insert_field, insert_field_data


def json_type(v):
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
