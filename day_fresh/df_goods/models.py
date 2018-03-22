# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TypeInfo(models.Model):
    ttitle=models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')# 数据库将文件传递到什么地方去，这个地址是和配置的图片根目录链接起来一起用的
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20,default='500g')
    gclick = models.IntegerField()
    gjangjie = models.CharField(max_length=300)
    gkucun = models.IntegerField()
    gcontent = models.TextField()
    # gadv = models.BooleanField(default=False)
    gtype = models.ForeignKey(TypeInfo)

    def __str__(self):
        return self.gtitle.encode('utf-8')

