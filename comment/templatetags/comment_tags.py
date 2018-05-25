from django import template
from comment.models import Commment
from django.contrib.contenttypes.models import  ContentType

register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Commment.objects.filter(content_type=content_type,object_id=obj.pk).count()