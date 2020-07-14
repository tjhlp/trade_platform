from django.db import models
from beans_bill.utils.models import BaseModel


# Create your models here.
class BillInfo(BaseModel):
    """账单表"""
    bill_id = models.AutoField(verbose_name='表ID', primary_key=True)
    account_id = models.IntegerField(verbose_name='账号ID')
    bill_name = models.CharField(max_length=60, verbose_name='表名')
    # bill_auth(1.admin 2.user)
    bill_auth = models.CharField(max_length=5, verbose_name='权限')
    bill_members = models.CharField(max_length=60, verbose_name='成员')

    class Meta:
        db_table = 'TAB_BILL'
        verbose_name = '账单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.bill_id, self.bill_name)
