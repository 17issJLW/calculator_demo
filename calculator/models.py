from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import json
# Create your models here.
from django.utils import timezone


class History(models.Model):

    input_str = models.CharField(verbose_name="计算器输入内容",max_length=255)
    result = models.CharField(verbose_name="计算结果",max_length=64,default="None")
    pub_time = models.DateTimeField(verbose_name="时间",default=timezone.now)

    def __str__(self):
        return "{}={}".format(self.input_str,self.result)

    class Meta:
        ordering = ['-id']