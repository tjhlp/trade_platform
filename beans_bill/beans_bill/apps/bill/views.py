from django.views import View

from bill.models import *
from beans_bill.utils.response_code import *
from beans_bill.utils.comm_utils import *


class BillListView(View):
    """ 显示所有账户"""

    def post(self, request):
        params = {'user_id': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        # 判断数据源是否属于所属节点
        try:
            info_models = BillInfo.objects.filter(account_id=js['user_id'])
        except Exception as error:
            logger.error("BillInfo got exception：%s, params:%s" % (str(error), js))
            return json_response(CODE_NODE_SOURCE_MISSING)
        res = []
        for info_model in info_models:
            rsp = {
                'bill_name': info_model.bill_name,
                'bill_members': info_model.bill_members,
                'bill_auth': info_model.bill_auth
            }
            res.append(rsp)
        return json_response(CODE_SUCCESS, res)


class BillAddView(View):
    """ 添加账户"""

    def post(self, request):
        params = {'user_id': (1, str), 'bill_name': (1, str),'bill_auth': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        # 判断数据源是否属于所属节点
        try:
            info_models = BillInfo.objects.create(**js)
        except Exception as error:
            logger.error("BillInfo got exception：%s, params:%s" % (str(error), js))
            return json_response(CODE_NODE_SOURCE_MISSING)
        rsp = {
            'bill_id': info_models
        }
        return json_response(CODE_SUCCESS, rsp)
