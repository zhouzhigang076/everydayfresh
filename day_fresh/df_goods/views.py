# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import models
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
    gtitle = goods_info.gtitle
    gjangjie = goods_info.gjangjie
    gprice = goods_info.gprice
    gcontent = goods_info.gcontent
    gpic = goods_info.gpic
    context = {
        'title': '天天生鲜-详情页',
        'gtitle':gtitle,
        'gjangjie':gjangjie,
        'gprice':gprice,
        'gcontent':gcontent,
        "gpic":gpic
    }




    return render(request,'df_goods/detail.html', context)
