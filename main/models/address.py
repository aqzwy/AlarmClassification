from django.db import models

__metaclass__ = type

# 地址实体
class Address(models.Model):
    address_id = models.CharField(max_length=100, null=True, verbose_name=u"地名Id")
    name = models.CharField(max_length=100, null=True, verbose_name=u"地名")
    fitst_type = models.CharField(max_length=100, null=True, verbose_name=u"地址一级类型")
    second_type = models.CharField(max_length=100, null=True, verbose_name=u"地址二级类型")
    url = models.CharField(max_length=100, null=True, verbose_name=u"地址详细信息链接")
    location = models.CharField(max_length=100, null=True, verbose_name=u"定位")
    contact = models.CharField(max_length=100, null=True, verbose_name=u"联系方式")