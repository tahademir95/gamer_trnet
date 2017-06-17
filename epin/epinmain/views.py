from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from .models import Profile,Game
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

import json


def shop(request):

    if request.user.is_authenticated():
        c = {}
        c.update(csrf(request))
        return render_to_response('create_cart.html',c)
    else:
        return HttpResponseRedirect('/accounts/login/')

def cart_status(request):
    c = {}
    c.update(csrf(request))
    s = SessionStore()
    s['count']=45
    s.save()
    key = s.session_key
    s_new = Session.objects.get()

    print(s_new.get_decoded())
    return render_to_response('index.html')


def games(request):
    if request.user.is_authenticated():
        print("Hello")
        return render(request,'index.html')
    else:
        return render_to_response('joinus.html')

def login(request):
    c = {}
    c.update(csrf(request))


    return render_to_response('login.html',c)##look to the source code.

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        request.session['login_status'] = True
        return HttpResponseRedirect('/accounts/loggedin/')
    else:
        return HttpResponseRedirect('/accounts/invalid/')##Javascript ile bir hareket cekicez.
def loggedin(request):

    return render_to_response('loggedin.html',{'full_name':request.user.username})
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')

def signup(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('signup.html',c)


def createaccounts(request):
    name = request.POST.get('name', '')
    surname = request.POST.get('surname', '')
    username = request.POST.get('username','')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    birth_date = request.POST.get('birth_date', '')

    user_obj = User.objects.create(username ="{}".format(name),email="{}".format(email),password="{}".format(password))
    user_obj.save()
    profile_data = Profile.objects.create(user=user_obj)
    profile_data.birth_date="2010-12-23"
    return HttpResponseRedirect('/games/games/')
