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

        req_params = {''}
        try:
            info_models = ExpenseInfo.objects.filter(user_id=js['user_id'])
        except Exception as error:
            logger.error("BillInfo got exception：%s, params:%s" % (str(error), js))
            return json_response(CODE_NODE_SOURCE_MISSING)
        res = []
        for info_model in info_models:
            rsp = {
                'expense_name': info_model.expense_name,
                'expense_type': info_model.expense_type,
                'expense_time': info_model.expense_time,
                'expense_cost': info_model.expense_cost,
                'expense_content': info_model.expense_content
            }
            res.append(rsp)
        return json_response(CODE_SUCCESS, res)


class ExpenseAddView(View):
    """ 添加消费记录"""

    def post(self, request):
        params = {'user_id': (1, str), 'bill_id_list': (1, list), 'expense_name': (1, str), 'expense_type': (1, str),
                  'expense_time': (1, str), 'expense_cost': (1, str), 'expense_content': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        bill_id_list = js.pop('bill_id_list')
        ex_list = []
        for bill_id in bill_id_list:
            js['bill_id'] = bill_id
            ex_ = ExpenseInfo.objects.create(**js)
            ex_list.append(ex_.expense_id)
        rsp = {
            'expense_id': ex_list
        }
        return json_response(CODE_SUCCESS, rsp)

class ExpenseRemoveView(View):
    """ 添加消费记录"""

    def post(self, request):
        params = {'expense_id': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        ExpenseInfo.objects.get(expense_id=js['expense_id']).delete()

        return json_response(CODE_SUCCESS)
