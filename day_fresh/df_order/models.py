# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# 当单列表类
class OrderInfo(models.Model):
    # 订单编号,采用的是主键值
    oid = models.CharField(max_length=20,primary_key=True)
    # 订单客户
    user = models.ForeignKey('df_user.UserInfo')
    # 下订单时间
    odate = models.DateTimeField(auto_now=True)
    # 默认情况下是还没有付款
    oIsPay = models.BooleanField(default=False)
    # 设置最大交易额为9999.99
    ototal = models.DecimalField(max_digits=6,decimal_places=2)
    # 收货地址
    oaddress = models.CharField(max_length=150)

# 订购商品详情类
class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo')
    # 属于哪个订单
    order = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    count = models.IntegerField()


