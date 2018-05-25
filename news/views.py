from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import BrandType,Anews
from read_statistic.utils import read_statistic_once_read
from comment.models import Commment
from comment.forms import CommentForm
from image.models import Image
from shoedog.forms import LoginForm

# Create your views here.
def list_process(request,all_news):
    page_num = request.GET.get('page',1)#获取页码参数，未给出参数时默认参数为1
    paginator = Paginator(all_news,10)
    page = paginator.get_page(page_num)#对参数的各类判断以及包含在get_page方法中，不需要考虑page_num是否是整数是否在范围内，一切不符合规范的都直接传1
    current_page_num = page.number#获取当前页码
    page_range = list(range(max(current_page_num-2,1),current_page_num))+\
                 list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    # 添加省略页码标记
    if page_range[0]-1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    #确保首页和尾页一直在page_range中
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}
    context['page_of_news'] = page#此处的page_of_news单指一页中所有的news，且是一个page类型的数据，在前端模版使用时需要注意
    context['news_types'] = BrandType.objects.annotate(news_count=Count('anews'))
    context['page_range'] = page_range
    context['news_dates'] = Anews.objects.dates('created_time','month',order='DESC')
    return context


def news_list(request):
    all_news = Anews.objects.all()
    context ={}
    context = list_process(request,all_news)
    return render(request,'news/news_list.html', context)


def news_type_list(request,news_type_pk):
    news_type = get_object_or_404(BrandType, pk=news_type_pk)
    all_news = Anews.objects.filter(news_type=news_type)
    context = {}
    context = list_process(request,all_news)
    context['type'] = news_type
    return render(request,'news/news_type_list.html', context)


def news_date_list(request,year,month):
    all_news = Anews.objects.filter(created_time__year=year,created_time__month=month)
    context = {}
    context = list_process(request,all_news)
    context['current_date'] = '%s-%s'%(year,month)
    return render(request,'news/news_date_list.html', context)



def news_detail(request,news_pk):#此处的news_pk与url文件中urlpatterns中的<int:news_pk>对应
    news = get_object_or_404(Anews,pk = news_pk)
    getcookies = read_statistic_once_read(request,news)
    content_type = ContentType.objects.get_for_model(news)
    comments = Commment.objects.filter(content_type=content_type,object_id=news_pk,parent=None)#显示一级评论

    #form的初始化
    data = {}
    data['content_type'] = content_type
    data['object_id'] = news_pk
    data['reply_comment_id'] = 0
    comment_form = CommentForm(initial=data)

    images = Image.objects.filter(content_type=content_type,object_id=news_pk)
    image_list = []
    for i in range(images.count()):
        image_list.append(i)
    images_list_tuple = zip(image_list,images)

    login_form = LoginForm()
    context = {}
    current_news = news
    context['loginform'] = login_form
    context['comment_count'] = Commment.objects.filter(content_type=content_type,object_id=news_pk).count()
    context['comment_form'] = comment_form
    context['image_list'] = image_list
    context['images'] = images_list_tuple
    context['comments'] = comments.order_by('-comment_time')
    context['news'] = current_news
    context['previous_news'] = Anews.objects.filter(created_time__gt=current_news.created_time).last()
    context['next_news'] = Anews.objects.filter(created_time__lt=current_news.created_time).first()
    response = render(request,'news/news_detail.html',context)
    response.set_cookie(getcookies,'true',max_age=60)
    return response