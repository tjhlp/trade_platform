from django.db import models


class BaseModel(models.Model):
    # 为模型类添加字段
    Crt_Time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    Upd_Time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True


class FixedCharField(models.Field):
    """
    自定义的 char 类型的字段类
    """

    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(FixedCharField, self).__init__(max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        """
        限定生成数据库表的字段类型为 char，长度为 max_length 指定的值
        """
        return 'char(%s)' % self.max_length