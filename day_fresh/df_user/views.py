# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from hashlib import sha1
import models

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
    user = models.UserInfo.objects.create(**user_info)
    user.save()
    #注册成功，转到登录页面
    return redirect('/user/login/')

#验证该用户名是否已经注册
def uname_check(request):
    users= models.UserInfo.objects.all()
    list=[]
    for user in users:
        list.append({'name':user.uname})
    return JsonResponse({'data':list})

#查看邮箱是否已经被注册
def uemail_check(request):
    users = models.UserInfo.objects.all()
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
        # request.cookie['user_name']=name
        try:
            user = models.UserInfo.objects.get(uname__exact=name)
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
            response = HttpResponseRedirect('/user/user_center/')
            response.set_cookie('name',name)
            return response
        else:
            context = {
                'title': '天天生鲜-登录',
                'pwd_error': '密码错误，请重新输入'
            }
            return render(request,'df_user/login.html', context)


# 用户中心
def user_center(request):
    context={
        'index':"active"
    }
    return render(request,'df_user/user_center_info.html',context)

# 设置个人信息
def user_order(request):
    context ={
        'order':'active'
    }
    return render(request,'df_user/user_center_order.html',context)


# 设置收货地址
def user_adress(request):
    context ={
        'adress':'active'
    }
    return render(request,'df_user/user_center_site.html',context)







