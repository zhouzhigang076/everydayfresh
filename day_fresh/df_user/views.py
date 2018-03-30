# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from hashlib import sha1
from models import *
import user_decorator
from df_goods.models import *


# Create your views here.
#展示注册页面
def register(request):
    context = {
        'title':"天天生鲜-注册"
    }
    return render(request,'df_user/register.html',context)

#处理注册页面传递过来的数据
def register_handle(request):
    '''接受用户输入'''
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码
    if upwd != ucpwd:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd = s1.hexdigest()

    #创建数据对象
    user_info={
        'uname':uname,
        'upwd':upwd,
        'uemail':uemail,

    }
    user = UserInfo.objects.create(**user_info)
    user.save()
    #注册成功，转到登录页面
    return redirect('/user/login/')

#验证该用户名是否已经注册
def uname_check(request):
    users= UserInfo.objects.all()
    list=[]
    for user in users:
        list.append({'name':user.uname})
    return JsonResponse({'data':list})

#查看邮箱是否已经被注册
def uemail_check(request):
    users =UserInfo.objects.all()
    list = []
    for user in users:
        list.append({'email':user.uemail})
    return JsonResponse({'data':list})


#登录页面
def login(request):
    if request.method == 'GET':
        context={
            'title':'天天生鲜-登录'
        }
        return render(request,'df_user/login.html',context)
    else:
        post = request.POST
        name = post.get('username')
        pwd = post.get('pwd')
        jizhu = post.get('jizhu')
        # request.cookie['user_name']=name
        try:
            user =UserInfo.objects.get(uname__exact=name)
            print(user)
        except:
            context = {
                'title': '天天生鲜-登录',
                'user_error': '用户名不存在，请重新输入'
            }
            return render(request,'df_user/login.html',context)

        s1 = sha1()
        s1.update(pwd)
        pwd = s1.hexdigest()
        if user.upwd == pwd:
            url = request.COOKIES.get('url','/goods/')
            response = HttpResponseRedirect(url)
            if jizhu =="1":
                response.set_cookie('name',name)
            else:
                response.set_cookie('name','',max_age=-1)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.uname
            return response
        else:
            context = {
                'title': '天天生鲜-登录',
                'pwd_error': '密码错误，请重新输入'
            }
            return render(request,'df_user/login.html', context)

@user_decorator.login
# 用户中心
def user_center(request):
    id = request.session['user_id']
    user_obj =UserInfo.objects.get(pk=id)
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1  = goods_ids.split(',')
    print goods_ids1
    goods_list = []
    try:


        for goods_id in goods_ids1:
            print goods_id
            goods_obj = GoodsInfo.objects.get(pk=int(goods_id))
            goods_list.append(goods_obj)

        context={
            'index':"active",
            'obj':user_obj,
            'goods_list':goods_list,

        }

    except:
        context = {
            'index': "active",
            'obj': user_obj,
            'goods_list':'-1',

        }

    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
# 设置个人信息
def user_order(request):
    id = request.session['user_id']
    context ={
        'order':'active'
    }
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
# 设置收货地址
def user_adress(request):
    id = request.session['user_id']
    if request.method == 'GET':


        user_obj = UserInfo.objects.get(pk=id)

        context = {
            'adress': 'active',
            'user':user_obj,
        }
        return render(request, 'df_user/user_center_site.html', context)
    else:
        uname = request.POST.get('uname')
        detailAdress = request.POST.get('detailAdress')
        youbian = request.POST.get('youbian')
        phone = request.POST.get('phone')
        address_info = {
            'ushou':uname,
            'uaddress':detailAdress,
            'uyoubian':youbian,
            'uphone':phone,
        }
        UserInfo.objects.filter(pk=id).update(**address_info)
        context ={
            'adress':'active'
        }
        return render(request,'df_user/user_center_site.html',context)


@user_decorator.login
def logout(request):
    # 将session里的记录清空
    request.session.flush()
    return redirect('/goods/')







