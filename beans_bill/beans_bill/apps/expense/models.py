from django.db import models

from beans_bill.utils.models import BaseModel


# Create your models here.
class ExpenseInfo(BaseModel):
    """消费记录表"""
    expense_id = models.AutoField(verbose_name='表ID', primary_key=True)
    bill_id = models.IntegerField(verbose_name='账单记录id')
    user_id = models.IntegerField(verbose_name='用户ID', default=0)
    expense_name = models.CharField(max_length=20, verbose_name='消费记录名')
    expense_type = models.CharField(max_length=20, verbose_name='消费类型')
    expense_time = models.DateTimeField(verbose_name='消费时间')
    expense_cost = models.DecimalField(max_digits=12, decimal_places=3, verbose_name='消费金额')
    expense_content = models.CharField(max_length=100, verbose_name='消费备注', default='')

    class Meta:
        db_table = 'TAB_EXPENSE'
        verbose_name = '消费记录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.expense_id, self.expense_name)
