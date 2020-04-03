from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import json
# Create your models here.
from django.utils import timezone


class MyUser(models.Model):
    user = models.OneToOneField(verbose_name="内置用户",to=User,on_delete=models.CASCADE)
    sex = models.CharField(verbose_name="性别", max_length=10,choices=[("男生","男生"), ("女生","女生")])

    def __str__(self):
        return "{} {}".format(self.user.username,self.sex)

    class Meta:
        ordering = ['id']

class History(models.Model):

    myuser = models.ForeignKey(verbose_name="对应用户",to=MyUser,on_delete=models.CASCADE,null=True,blank=True)
    input_str = models.CharField(verbose_name="计算器输入内容",max_length=255)
    result = models.CharField(verbose_name="计算结果",max_length=64,default="None")
    pub_time = models.DateTimeField(verbose_name="时间",default=timezone.now)

    def __str__(self):
        return "{}={}".format(self.input_str,self.result)

    class Meta:
        ordering = ['-id']