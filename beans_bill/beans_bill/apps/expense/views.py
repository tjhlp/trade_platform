from django.views import View
import datetime
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
    """ 删除消费记录"""

    def post(self, request):
        params = {'expense_id': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        ExpenseInfo.objects.get(expense_id=js['expense_id']).delete()

        return json_response(CODE_SUCCESS)


class ExpenseUpdateView(View):
    """ 更改消费记录"""

    def post(self, request):
        params = {'expense_id': (1, str), 'expense_name': (0, str), 'expense_type': (0, str),
                  'expense_time': (0, str), 'expense_cost': (0, str), 'expense_content': (0, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        expense_id = js.pop('expense_id')

        ex_ = ExpenseInfo.objects.get(expense_id=expense_id)

        ex_.expense_name = js['expense_name'] if js['expense_name'] else ex_.expense_name
        ex_.expense_type = js['expense_type'] if js['expense_type'] else ex_.expense_type
        ex_.expense_time = js['expense_time'] if js['expense_time'] else ex_.expense_time
        ex_.expense_cost = js['expense_cost'] if js['expense_cost'] else ex_.expense_cost
        ex_.expense_content = js['expense_content'] if js['expense_content'] else ex_.expense_content

        ex_.save()

        return json_response(CODE_SUCCESS)


class ExpenseCostView(View):
    """ 个人消费总额"""

    def post(self, request):
        params = {'user_id': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)
        last_month = today - datetime.timedelta(days=30)
        last_year = today - datetime.timedelta(days=365)

        week_model = ExpenseInfo.objects.filter(expense_time__gt=last_week)
        week_cost = 0
        for week in week_model:
            week_cost += week.expense_cost

        month_model = ExpenseInfo.objects.filter(expense_time__gt=last_month)
        month_cost = 0
        for month in month_model:
            month_cost += month.expense_cost

        year_model = ExpenseInfo.objects.filter(expense_time__gt=last_year)
        year_cost = 0
        for year in year_model:
            year_cost += year.expense_cost

        rsp ={
            'week_cost': week_cost,
            'month_cost': month_cost,
            'year_cost': year_cost,
        }

        return json_response(CODE_SUCCESS, rsp)