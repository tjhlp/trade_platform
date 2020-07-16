from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

"""
TAB_USER_INFO
字段Id	字段名称	类型/长度	必填	功能描述
userID	用户ID	CHAR(8)	Y	PK
userName	用户名	VARCHAR(60)	Y	
passWord	密码	VARCHAR(120)	Y	加密存储
phoneNum	联系电话	CHAR(20)	Y	
crtTime	创建时间	datetime	Y	默认值当前时间戳
updTime	更新时间	datetime	Y	默认值当前时间戳

"""


class UserModel(AbstractUser):
    user_id = models.AutoField(verbose_name='用户ID', primary_key=True)
    phone_num = models.CharField(max_length=20, verbose_name='联系电话')
    crt_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    upd_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        db_table = 'TAB_USER_INFO'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
