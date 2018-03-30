# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from df_user import user_decorator
from models import *
from df_goods.models import *


from django.shortcuts import render

# Create your views here.


@user_decorator.login
def cart(request):
    uid = request.session.get('user_id')
    cart_list= CartInfo.objects.filter(user_id=uid)
    # goods_list = []
    # for cart_obj in cart_list:
    #     goods_obj = GoodsInfo.objects.get(pk=int(cart_obj.goods_id))
    #     goods_list.append(goods_obj)

    context = {
        'val':'0',
        'goods_list':cart_list
    }
    return render(request, 'df_cart/cart.html',context)


@user_decorator.login
def add(request,goods_id,count):
    # 用户uid 购买了gid商品，数量为count
    uid = request.session.get('user_id')
    gid = int(goods_id)
    count = int(count)

    # 查询购物车中是否已经有此商品，如果有则数量增加，如果没有则新增
    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts)>=1:
        cart = carts[0]
        my_count = cart.count+count
        carts.update(count=my_count)
    else:
        purse_info = {
            'user_id':uid,
            'goods_id':gid,
            'count':count,
        }
        CartInfo.objects.create(**purse_info)

    myCount = CartInfo.objects.filter(user_id=request.session.get('user_id')).count()
    return JsonResponse({'count':myCount})
@user_decorator.login
def goods_count(request):
    myCount = CartInfo.objects.filter(user_id=request.session.get('user_id')).count()
    return JsonResponse({'count': myCount})

    pass

# 编辑更新数据
@user_decorator.login
def edit(request,goodsId,count):
    try:
        # 修改的是购物车，数据库中的数量
        res= CartInfo.objects.filter(goods_id=goodsId).update(count=count)
        return JsonResponse({"ok":[count,'ok']})

    except:
        cart_goods = CartInfo.objects.get(goods_id=goodsId)
        now_count = cart_goods.count
        return JsonResponse({'ok':[now_count,'no']})

# 删除数据
@user_decorator.login
def delete(request,cartId):
    try:
        res = CartInfo.objects.get(pk=int(cartId))
        res.delete()
        return JsonResponse({"ok":"ok"})
    except:
        return JsonResponse({'ok':"no"})

