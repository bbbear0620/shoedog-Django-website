from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeRecord,LikesAllCount
# Create your views here.
def SuccessResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = like_num
    return JsonResponse(data)
def ErrorResponse(code,message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def like_change(request):
    #obtain data
    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(404,'object not exist')

    is_like = request.GET.get('is_like')
    user = request.user
    #process data
    if not user.is_authenticated:
        return ErrorResponse(400,'please login first')


    if is_like =='true':
        #like
        like_record,record_created= LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
        if record_created:
            #新增点赞数据
            like_count,count_created = LikesAllCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if count_created:
                like_count.like_num = 1
                like_count.save()
                #do nothing
            else:
                like_count.like_num += 1
                like_count.save()
            return SuccessResponse(like_count.like_num)
        else:
            return ErrorResponse(402,'you were liked')
    else:
        #dislike
        if LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete()
            like_count = LikesAllCount.objects.get(content_type=content_type,object_id=object_id)
            like_count.like_num -= 1
            like_count.save()
            return SuccessResponse(like_count.like_num)
        else:
            return ErrorResponse(403,'you were not liked')