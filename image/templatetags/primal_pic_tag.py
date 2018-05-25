from django import template
from image.models import Image
from news.models import Anews
from django.contrib.contenttypes.models import  ContentType

register = template.Library()

@register.simple_tag
def get_primal_pic(obj):
    content_type = ContentType.objects.get_for_model(obj)
    primal_pic = Image.objects.filter(content_type=content_type,object_id=obj.pk,primal_pic=True)[0]
    return primal_pic.image.url

@register.simple_tag
def get_primal_pic_id(id):
    content_type = ContentType.objects.get_for_model(Anews)
    primal_pic = Image.objects.filter(content_type=content_type,object_id=id,primal_pic=True)[0]
    return primal_pic.image.url