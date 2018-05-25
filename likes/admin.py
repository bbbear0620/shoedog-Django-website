from django.contrib import admin
from .models import LikeRecord,LikesAllCount
# Register your models here.
@admin.register(LikesAllCount)
class LikesAllCountAdmin(admin.ModelAdmin):
    list_display = ('id','content_object','like_num')

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id','content_object','user')