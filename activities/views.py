from django.shortcuts import render
from .models import Activity
from django.core.paginator import Paginator
# Create your views here.
def activitieslist(request):
    context = {}
    all_activity = Activity.objects.all()
    page_num = request.GET.get('page',1)#获取页码参数，未给出参数时默认参数为1
    paginator = Paginator(all_activity,10)
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
    context['page_range'] = page_range
    return render(request, 'activities/activities_page.html', context)