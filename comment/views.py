from django.shortcuts import render,redirect
from .models import Commment
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .forms import CommentForm
# Create your views here.
def update_comment(request):
    '''text = request.POST.get('comment-content','').strip()
    if text == '':
        return render(request,'error.html',{'message':'comment content is null'})
    try:
        content_type = request.POST.get('content_type','')
        object_id = int(request.POST.get('object_id',''))
        model_class = ContentType.objects.get(model=content_type).model_class()#获得具体的model类，比如Anews
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request,'error.html',{'message':'comment object is not exist'})

    comment = Commment()
    comment.user = request.user
    comment.text = text+request.GET.get('para')
    comment.content_object = model_obj
    comment.save()

    referer = request.META.get('HTTP_REFERER','/')
    return redirect(referer)'''
    comment_form = CommentForm(request.POST,user=request.user)
    referer = request.META.get('HTTP_REFERER', '/')
    data = {}
    if comment_form.is_valid():
        comment = Commment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            if parent.root is None:
                comment.root = parent
            else:
                comment.root = parent.root
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        #return redirect(referer)
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
    else:
        #return render(request, 'error.html', {'message': comment_form.errors,'redirect_to':referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)