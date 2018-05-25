from django.urls import path
from . import views
#start with news
urlpatterns = [
    path('allnewslist/',views.news_list,name='news_list'),
    path('<int:news_pk>',views.news_detail,name='news_detail'),
    path('typelist/<int:news_type_pk>',views.news_type_list,name='news_type_list'),
    path('datelist/<int:year>/<int:month>',views.news_date_list,name='news_date_list')
]