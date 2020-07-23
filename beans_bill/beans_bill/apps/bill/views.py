from django.views import View

from bill.models import *
from beans_bill.utils.response_code import *
from beans_bill.utils.comm_utils import *


class BillListView(View):
    """ 显示所有账户"""

    def post(self, request):
        params = {'user_id': (1, str), 'bill_id': (0, str), 'bill_name': (0, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        # 判断数据源是否属于所属节点
        try:
            print(js)
            filter_params = {'user_id': js['user_id']}
            if 'bill_id' in js:
                filter_params['bill_id'] = js['bill_id']
            if 'bill_name' in js:
                filter_params['bill_name'] = js['bill_name']
            info_models = BillInfo.objects.filter(**filter_params)
            # print(info_models)
        except Exception as error:
            logger.error("BillInfo got exception：%s, params:%s" % (str(error), js))
            return json_response(CODE_NODE_SOURCE_MISSING)
        res = []
        for info_model in info_models:
            rsp = {
                'bill_name': info_model.bill_name,
                'bill_id': info_model.bill_id,
                'bill_members': info_model.bill_members,
                'bill_auth': info_model.bill_auth
            }
            res.append(rsp)
        return json_response(CODE_SUCCESS, res)


class BillAddView(View):
    """ 添加账单"""

    def post(self, request):
        params = {'user_id': (1, str), 'bill_name': (1, str), 'bill_auth': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        try:
            info_models = BillInfo.objects.create(**js)
        except Exception as error:
            logger.error("BillInfo got exception：%s, params:%s" % (str(error), js))
            return json_response(CODE_NODE_SOURCE_MISSING)
        rsp = {
            'bill_id': info_models.bill_id
        }
        return json_response(CODE_SUCCESS, rsp)


class BillAddUserView(View):
    """ 添加账户"""

    def post(self, request):
        params = {'user_id': (1, str), 'bill_id': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        bill_id = js.pop('bill_id')
        try:
            bill_model = BillInfo.objects.get(bill_id=bill_id)

            param_bill = {
                'user_id': js['user_id'],
                'bill_members': bill_model.user_id,
                'bill_name': bill_model.bill_name,
                'bill_auth': 2,
            }
            info_models = BillInfo.objects.create(**param_bill)
        except Exception as error:
            logger.error("BillInfo got exception：%s, params:%s" % (str(error), js))
            return json_response(CODE_NODE_SOURCE_MISSING)

        rsp = {
            'bill_id': info_models.bill_id
        }
        return json_response(CODE_SUCCESS, rsp)
