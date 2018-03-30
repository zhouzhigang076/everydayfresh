# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import models
import sys
# Create your views here.
# 首页展示
def index(request):
    type_info = models.TypeInfo.objects.all()
    type00 = type_info[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = type_info[0].goodsinfo_set.order_by('-gclick')[0:4]
    type10 = type_info[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = type_info[1].goodsinfo_set.order_by('-gclick')[0:4]
    type20 = type_info[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = type_info[2].goodsinfo_set.order_by('-gclick')[0:4]
    type30 = type_info[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = type_info[3].goodsinfo_set.order_by('-gclick')[0:4]
    type40 = type_info[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = type_info[4].goodsinfo_set.order_by('-gclick')[0:4]
    type50 = type_info[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = type_info[5].goodsinfo_set.order_by('-gclick')[0:4]

    context={
        'title':'天天生鲜-首页',
        'type00':type00,'type01':type01,'type10':type10,'type11':type11,'type20':type20,
        'type21': type21,'type30':type30,'type31':type31,'type40':type40,'type41':type41,
        'type50':type50,'type51':type51
    }
    return render(request,'df_goods/index.html', context)

# 列表页展示
def list(request,num):
    val = request.GET.get('a')
    print val
    type_info = models.TypeInfo.objects.all()
    num = int(num)
    if val is None:

        val=1
    val = int(val)
    if val == 1:
        type000 = type_info[num-1].goodsinfo_set.order_by('-id')
        context = {
            'title': '天天生鲜-列表页',
            'goods_list': type000,
            "index01":"active"
        }
        return render(request, 'df_goods/list.html', context)
    if val == 2:
        type010 = type_info[num-1].goodsinfo_set.order_by('gprice')
        context = {
            'title': '天天生鲜-列表页',
            'goods_list': type010,
            "price": "active"

        }
        return render(request, 'df_goods/list.html', context)
    if val == 3:
        type011 = type_info[num-1].goodsinfo_set.order_by('-gclick')
        context = {
            'title': '天天生鲜-列表页',
            'goods_list':type011,
            "click": "active"

        }

        return render(request,'df_goods/list.html', context)

# 细节页展示
def detail(request,id):
    goods_info = models.GoodsInfo.objects.get(pk=id)
    gclick = goods_info.gclick
    gtitle = goods_info.gtitle
    gjangjie = goods_info.gjangjie
    gprice = goods_info.gprice
    gcontent = goods_info.gcontent
    gpic = goods_info.gpic
    gclick = int(gclick)
    gclick += 1
    # 首先，从cookie中读取看看这个用户有没有参看过该产品
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_id = '%d'%goods_info.id
    if goods_ids != '':#判断是否有浏览记录，如果有就继续判断，cookie的值应该是这样的键值对{‘goods_ids’:"1,2,4,3,4,3"}
        goods_ids1= goods_ids.split(',')#将cookie记录进行拆分成列表
        if goods_ids1.count(goods_id)>=1:# 这表明该商品已经浏览过，并且记录了下来，再次进入，证明客户比较心怡这个产品这个产品应该在浏览记录里往前排
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)# 如果是上面的情况，该商品根据点击量应该排在最前头，如果是最新浏览，也按理说应该排在最前头，所以
                                    # 这一步是无论如何都要进行的
        if len(goods_ids1)>=6: # 这里值记录5种商品，经最后的浏览记录清楚
            del goods_ids1[5]
        goods_ids=','.join(goods_ids1)
    else:
        goods_ids = goods_id# 如果没有浏览记录就直接添加

    context = {

        'title': '天天生鲜-详情页',
        'goods_info': goods_info,
        'gtitle':gtitle,
        'gjangjie':gjangjie,
        'gprice':gprice,
        'gcontent':gcontent,
        "gpic":gpic
    }

    models.GoodsInfo.objects.filter(pk=id).update(gclick=gclick)
    response = render(request, 'df_goods/detail.html', context)
    # 这个浏览了就做个记录
    response.set_cookie('goods_ids',goods_ids)

    return response
