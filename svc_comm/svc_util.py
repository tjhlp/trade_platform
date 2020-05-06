import logging
import json
import time

from flask import make_response


def json_encode(js_obj, sort=True, ensure_ascii=False):
    """
    将一个python对象编码为字符串，支持中文
    为了简化代码，用[]表示数组空，用{}表示其他空
    :param js_obj: python对象
    :param sort: 是否按key排序，默认按key排序，方便数据对比
    :return:
    """
    # noinspection PyBroadException
    try:
        if js_obj:
            return json.dumps(js_obj, sort_keys=sort, ensure_ascii=ensure_ascii)
        else:
            return '[]' if isinstance(js_obj, list) else '{}'
    except Exception as e:
        logging.debug('json_encode got exception: %s, js_obj:%s' % (str(e), js_obj))
        return '{}'


def url_module_report(url_handler):
    """
    这个修饰器提供cgi接口模调上报
    :param url_handler:
    :return:
    """

    def wrapper(obj):
        rsp = {'code': 500, 'value': -1, 'returnCode': 500, 'returnValue': -1}
        # noinspection PyBroadException
        try:
            # real do
            rsp = url_handler(obj)
        except:
            logging.error('url_handler exception: %s' % '错误')
        finally:
            if isinstance(rsp, tuple):
                code, value, rsp_str = rsp
            else:
                code = rsp['code'] if obj.pure_js else rsp['returnCode']
                value = rsp['value'] if obj.pure_js else rsp['returnValue']
                rsp_str = json_encode(rsp, False)

            logging.info("code:%s value:%s ,business timecost: %sms", code, value, time.time())

            return make_response(rsp_str, {"Content-Type": "application/json"})

    return wrapper
