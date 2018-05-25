from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from news.models import Anews
from django.urls import reverse
from read_statistic.utils import get_seven_days_statistics,get_today_hot_news,get_week_hot_news
from .forms import LoginForm,RegisterForm

def home(request):
    news_ct = ContentType.objects.get_for_model(Anews)
    dates,read_nums = get_seven_days_statistics(news_ct)
    today_hot_data = get_today_hot_news(news_ct)

    #获取7天热门博客的缓存数据
    week_hot_data = cache.get('week_hot_data')
    if week_hot_data is None:
        week_hot_data = get_week_hot_news(news_ct)
        cache.set('week_hot_data',week_hot_data,3600)
        print('calculate')
    else:
        print('cache')

    #首页轮播图数据
    broadcast_news = Anews.objects.filter(broadcast_news=True)
    broadcast_news_order = []
    for  i in range(broadcast_news.count()):
        broadcast_news_order.append(i)
    broadcast_news_tuple = zip(broadcast_news_order,broadcast_news)

    context = {}
    context['broadcast_news'] = broadcast_news_tuple
    context['news_list'] = broadcast_news_order
    context['read_nums'] = read_nums
    context['week_hot_data'] = week_hot_data
    context['today_hot_data'] = today_hot_data
    context['dates'] = dates
    return render(request,'home.html',context)

def mylogin(request):
    '''username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(request,username=username,password=password)
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    if user is not None:
        login(request,user)
        return redirect(referer)#跳转到首页
    else:
        return  render(request,'error.html',{'message':'username or password error'})'''
    #如果是POST请求
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
                user = login_form.cleaned_data['user']
                login(request,user)
                return redirect(request.GET.get('from'))
    #如果是GET请求
    else:
        login_form = LoginForm()
    context = {}
    context['loginform'] = login_form
    return render(request,'login.html',context)

def loginformodal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        login(request,user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def myregister(request):
    if request.method == 'POST':
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            username = registerform.cleaned_data['username']
            email = registerform.cleaned_data['email']
            password = registerform.cleaned_data['password_again']
            user = User.objects.create_user(username,email,password)
            user.save()
            #登录用户
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect(request.GET.get('from',reverse('home')))

    else:
        registerform = RegisterForm
    context = {}
    context['registerform'] = registerform
    return render(request,'register.html',context)

def mylogout(request):
    logout(request)
    return redirect(request.GET.get('from'))

def userprofile(request):
    context = {}
    return render(request,'userprofile.html',context)
