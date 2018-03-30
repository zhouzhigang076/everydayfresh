# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect
from df_user import user_decorator
from django.db import transaction #这一个是处理事物的
from models import *
import datetime
from decimal import Decimal
from df_cart.models import *
from df_goods.models import *
from df_user.models import *


# Create your views here.
@user_decorator.login
def order(request):

    listId = request.GET.getlist('carts_id')
    uid = request.session.get('user_id')
    user_obj = UserInfo.objects.get(pk=uid)

    if listId == []:
        context = {
            'val': "1",
            'user_obj':user_obj,
        }
        return render(request, 'df_order/place_order.html', context)
    else:
        cart_list = []
        for id in listId:
            cart_obj = CartInfo.objects.get(id=id)
            cart_list.append(cart_obj)
        context={
            'val':"1",
            'cart_list':cart_list,
            'user_obj': user_obj,
        }
        print cart_list
        return render(request,'df_order/place_order.html',context)


"""
用事物来完成：一旦操作失败则全部回退
处理订单的思路：
    1.  创建订单对象
    2.判断商品的库存
    3.创建详单对象
    4.修改商品库存
    5.删除购物车
"""

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    carts_ids = request.GET.getlist('cart_id')
    total = request.GET.get('total')
    #django事物的应用
    #先保存一个点，如果操作失误，则能立马回到这个点上来，这个点o同时有保存数据的左右
    tran_id= transaction.savepoint()
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.datetime.now()
        uid= request.session.get('user_id')
        order.oid = "%s%d"%(now.strftime("%Y%m%d%H%M%S"), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(total)
        order.save()
    #     # 创建详单对象
        cart_ids1 = [int(item) for item in carts_ids]
        for id1 in cart_ids1:
            # 创建订购详单对象
            detail = OrderDetailInfo()
            # detail.order 表示的是外键所对应的对象
            # 表明属于哪个订单对象
            detail.order = order

    #         # 查询购物车的信息
            cart = CartInfo.objects.get(id=id1)
    #         # 判断商品库存
            goods = cart.goods
            if goods.gkucun >= cart.count:#如果库存大于钩盖数量
                print '-----------------1-------------'
                # 减少商品库存
                print "开始"+str(goods.gkucun)
                goods.gkucun = cart.goods.gkucun-cart.count

                print "开始" + str(goods.gkucun)
                goods.save()

    #             # 完善订单详情
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
    #             # 提交保存
                detail.save()
    #             # 删除购物车数据
                cart.delete()
            else:
                print '------------------2---------'
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
    #         # 到了最后要提交上去这个事物点保存的内容
        transaction.savepoint_commit(tran_id)


    except Exception as e:
        print "=================%s"%e

        transaction.savepoint_rollback(tran_id)
        # return HttpResponse('ok')
    return redirect('/user/user_order/')






