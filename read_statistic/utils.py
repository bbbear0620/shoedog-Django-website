import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail
from news.models import Anews


def read_statistic_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    getcookies = "%s_%s_read" % (ct.model,obj.pk)
    if not request.COOKIES.get(getcookies):
        #检测当前总阅读数
        if ReadNum.objects.filter(content_type=ct,object_id=obj.pk).count():
            readnum = ReadNum.objects.get(content_type=ct ,object_id=obj.pk)
            readnum.read_num += 1
            readnum.save()
        else:
            readnum = ReadNum(content_type=ct ,object_id=obj.pk)
            readnum.read_num = 1
            readnum.save()
        #检测当天阅读数
        if ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,date=timezone.now().date()).count():
            readdetail = ReadDetail.objects.get(content_type=ct,object_id=obj.pk,date=timezone.now().date())
        else:
            readdetail = ReadDetail(content_type=ct,object_id=obj.pk,date=timezone.now().date())
        readdetail.read_num += 1
        readdetail.save()
    return getcookies

def get_seven_days_statistics(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(6,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums

def get_today_hot_news(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    return read_details[:7]

def get_week_hot_news(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    '''read_details = ReadDetail.objects.filter(content_type=content_type,date__lte=today,date__gt=date)\
                                     .values('content_type','object_id')\
                                     .annotate(read_num_sum=Sum('read_num'))\
                                     .order_by('-read_num_sum')'''
    read_details = Anews.objects.filter(read_details__date__lte=today,read_details__date__gt=date)\
                           .values('id','title')\
                           .annotate(read_num_sum=Sum('read_details__read_num'))\
                           .order_by('-read_num_sum')
    return read_details[:7]
