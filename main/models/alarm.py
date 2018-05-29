from django.db import models

__metaclass__ = type


class alarm(models.Model):
    alarm_id = models.CharField(max_length=100,verbose_name=u"警情ID")
    first_type = models.CharField(max_length=100, verbose_name=u"警情一级类型")
    second_type = models.CharField(max_length=100, verbose_name=u"警情二级类型")
    third_type = models.CharField(max_length=100, verbose_name=u"警情三级类型")
    fourth_type = models.CharField(max_length=100, verbose_name=u"警情四级类型")
    content = models.CharField(max_length=100, verbose_name=u"警情描述")
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:  # 按时间下降排序
        ordering = ['-alarm_id']

