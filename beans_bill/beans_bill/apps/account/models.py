from django.db import models
from beans_bill.utils.models import BaseModel


# Create your models here.
class AccountInfo(BaseModel):
    """账号表"""
    account_id = models.AutoField(verbose_name='表ID', primary_key=True)
    account_name = models.CharField(max_length=60, verbose_name='表名')
    account_photo = models.ImageField(max_length=200, default='', null=True, blank=True, verbose_name='默认图片')

    class Meta:
        db_table = 'TAB_Account'
        verbose_name = '账号表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.account_id, self.account_name)
