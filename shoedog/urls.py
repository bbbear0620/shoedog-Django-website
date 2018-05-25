"""shoedog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name='home'),#首页的处理方法在shoedog文件夹下新建一个views
    path('admin/', admin.site.urls),
    path('news/',include('news.urls')),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('login/',views.mylogin,name='login'),
    path('modallogin/',views.loginformodal,name='modal_login'),
    path('logout/',views.mylogout,name='logout'),
    path('register/',views.myregister,name='register'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('comment/',include('comment.urls')),
    path('like/',include('likes.urls')),
    path('activities/',include('activities.urls'))

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)