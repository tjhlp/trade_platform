from django.views import View

from expense.models import *
from beans_bill.utils.response_code import *
from beans_bill.utils.comm_utils import *


class ExpenseListView(View):
    """ 显示账户下所有消费记录"""

    def post(self, request):
        params = {'user_id': (1, str), 'bill_name': (0, str), 'expense_type': (0, str), 'expense_time': (0, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        # 判断数据源是否属于所属节点
        req_params = {''}
        try:
            info_models = ExpenseInfo.objects.filter(account_id=js['user_id'])
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


class ExpenseAddView(View):
    """ 添加消费记录"""

    def post(self, request):
        params = {'user_id': (1, str), 'bill_id': (1, str), 'expense_name': (1, str), 'expense_type': (1, str),
                  'expense_time': (1, str), 'expense_cost': (1, str), 'expense_content': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        ex_ = ExpenseInfo.objects.create(**js)

        rsp = {
            'expense_id': ex_.expense_id
        }
        return json_response(CODE_SUCCESS, rsp)
