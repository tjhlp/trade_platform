import logging
import json
import time
import functools

from flask import make_response
from flask import request

from svc_comm.sys_code import *


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

    @functools.wraps(url_handler)
    def wrapper(obj):
        rsp = {'code': 500, 'value': -1, 'returnCode': 500, 'returnValue': -1}
        # noinspection PyBroadException
        try:
            rsp = url_handler(obj)
        except:
            logging.error('url_handler exception: %s' % '错误')
        finally:
            if isinstance(rsp, tuple):
                code, value, rsp_str = rsp
            else:
                code = rsp['code']
                value = rsp['value']
                rsp_str = json_encode(rsp, False)

            return make_response(rsp_str, {"Content-Type": "application/json"})

    return wrapper


def json_decode(js_str):
    """
    将json字符串解码为成python对象
    解码失败默认生成一个AutoVivification的空字典
    :param js_str: json字符串
    :return: python对象
    """

    try:
        return json.loads(js_str)
    except Exception as e:
        logging.debug('json_decode got exception: %s, js_str:%s' % (str(e), js_str))
        return 'error'


def valid_body_js(params):
    """
    先检查request的请求参数，然后转化为python对象
    :param params: {'page_index': 1, 'page_size': 1, 'activity_id': 0, 'name': 0} 1表示必选参数，0表示可选参数
    {'page_index': (1, int), 'page_size': (1, int), 'activity_id': (0, int), 'name': (0, str)} 判断可选的同时判断类型
    :return: python对象，处理结果CODE_SUCCESS表示成功
    使用样例
    params = {'page_index': 1, 'page_size': 1, 'activity_id': 0, 'name': 0}
    js, code = self.valid_body_js(params)
    if code != CODE_SUCCESS:
        logging.error('invalid param')
        return self.code2rsp(code)
    """
    # noinspection PyBroadException
    try:
        raw_body = request.get_data(as_text=True)
        print('dfafasdf:%s'% raw_body)
        all_js = json_decode(raw_body)
        # json_decode异常会返回{}，这里简单判断下是不是异常
        if len(raw_body) >= 16 and not all_js:
            return None, CODE_INVALID_JSON

        # 空json是允许的{}
        if not isinstance(all_js, dict):
            return None, CODE_INVALID_JSON

        if params:
            must = set()
            option = set()
            for k, v in params.items():
                if isinstance(v, tuple):
                    # 第一个是可选项，第二个是类型
                    param_option = v[0]
                    if k in all_js and not isinstance(all_js[k], v[1]):
                        logging.debug('invalid param type:%s' % k)
                        return None, CODE_INPUT_PARAM_INVALID_TYPE
                    # 扩展一下，第三个是默认值
                    elif k not in all_js and len(v) >= 3:
                        all_js[k] = v[2]
                else:
                    param_option = v
                if param_option:
                    must.add(k)
                else:
                    option.add(k)

        return all_js, CODE_SUCCESS

    except Exception as e:
        logging.debug('parser json got exception:%s' % str(e))
        return None, CODE_INPUT_PARAM_INVALID


def code2rsp(code, return_value=None):
    return dict2rsp(code, {}, return_value)


def dict2rsp(code, data, return_value=None):
    """
    生成应答dict，会自动将这个dict处理成json格式然后返回给调用方
    :param code: 错误码三元组，code[0]是returnCode，code[1]是returnMessage，code[2]是returnValue
    :param data: 应答的data值
    :param return_value:
    :return:
    """
    value = return_value if return_value else code[2]
    all_js = {'value': value, 'code': code[0], 'msg': code[1], 'data': data}
    raw_body = json_encode(all_js, False)
    print(code[0], value, raw_body)
    return code[0], value, raw_body


if __name__ == '__main__':
    pass

