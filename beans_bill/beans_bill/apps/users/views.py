import re
from django.views import View
from django.contrib.auth import authenticate

from beans_bill.utils.response_code import *
from beans_bill.utils.comm_utils import *

from users.models import UserModel
from bill.models import BillInfo

class LoginView(View):
    def post(self, request):
        params = {'username': (1, str), 'password': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        user = authenticate(request=request, username=js['username'], password=js['password'])
        if user is None:
            logger.error('user_login got exception: username or password is error, params:%s' % (js))
            return json_response(CODE_USER_LOGIN_ERROR)


        # 响应
        # rsp = user_token(user, js)
        rsp = {
            'user_id': user.user_id,
            'user_name': user.username,
        }
        return json_response(CODE_SUCCESS, rsp)


class LogoutView(View):
    def get(self, request):
        return json_response(CODE_SUCCESS)


class RegisterView(View):

    def post(self, request):

        params = {'username': (1, str), 'password': (1, str),'password2': (1, str), 'phone_num': (1, str)}
        js, code = valid_body_js(request, params)
        if code != CODE_SUCCESS:
            logger.error("invalid param")
            return json_response(code)

        # if not re.match('^[a-zA-Z0-9_-]{5,20}$', js['username']):
        #     return json_response(CODE_USERNAME_ERROR)
        # if not re.match('^[0-9A-Za-z]{8,20}$', js['password']):
        #     return json_response(CODE_PASSWORD_ERROR)
        # if not re.match('^1[345789]\d{9}$', js['phone_num']):
        #     return json_response(CODE_MOBILE_ERROR)

        password2 = js.pop('password2')
        # 判断两次接收密码
        if not js['password'] == password2:
            return json_response(CODE_PASSWORD_ERROR)


        try:
            user = UserModel.objects.create_user(**js)
            BillInfo.objects.create(
                account_id=user.user_id,
                bill_name='个人账单',
                bill_auth='1',
                bill_members='',
            )
        except Exception as e:
            logger.error('user_register got exception:%s, params:%s' % (str(e), js))
            return json_response(CODE_USER_REGISTER_ERROR)


        # 响应
        # rsp = user_token(user, js)
        rsp = {
            'user_id': user.user_id,
            'user_name': user.username,
        }

        return json_response(CODE_SUCCESS, rsp)
