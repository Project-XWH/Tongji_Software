#coding=utf-8
# register login
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.template import RequestContext
from django.contrib import auth
from account.models import Advice
from django.contrib.auth.models import User
import pdb
import time,os

path = os.path.dirname(__file__)
def Defaultlogin(req):
    return render(req,'login.html')

def Defaultregister(req):
    return render(req,'register.html')

def Login(req):
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(username=username,password=password)
    # referer = req.META.get('HTTP_REFERER','/')
    if user is not None:
        auth_login(req, user)
        return redirect('/')
        # return render(req,'enzyme.html',{'username':username,'operation':"注册"})
        # return render(req,'success.html',{'operation':"登录"})
    else:
        return  HttpResponse("There is no exist this user <a href='/pathlab/'>HOME</a>")
        # return render(req,"login.html",{'uf':uf})


def Register(req):
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(username=username,password=password)
    # if user is not None:
    if User.objects.filter(username=username).exists():
        return render(req,'register.html',{"errors":"用户名已存在,请重新注册"})
    else:
        #将表单写入数据库
        user = User.objects.create_user(username=username,password=password)
        # user = authenticate(username=username,password=password)
        user.save()
        user = authenticate(username=username,password=password)
        # if user is not None:
        auth_login(req, user)
        #user = User(username=username,password=password,email=email)
        # users.save()
        #pdb.set_trace()
        #返回注册成功页面
        return render(req,'pathlab.html')
#     return render(req,'register.html',{'uf':uf})


def logout(req):
    auth_logout(req)
    return render(req,'pathlab.html')


def advice(req):
    return render(req,'advice.html', {'flag':'0'})
    
def guest_advice(req):
    ticks = str(time.time()).encode()
    advice_text = req.POST['advice'].encode()
    #localtime = str(time.asctime( time.localtime(time.time()) ))
    #localtime = localtime.encode()
    # advice_txt = path+'/../data/parts_design/advice.txt'
    # f = open(advice_txt, 'ab')
    # f.write(ticks +':\t'.encode() + advice+'\n\n'.encode())
    # f.close()
    advice = Advice()
    advice.user = req.user
    advice.text = advice_text
    advice.save()
    return render(req, 'advice.html', {"flag":"1"})
#     return render(req,'guest_advice.html',
#                                {'time':ticks})
                               
