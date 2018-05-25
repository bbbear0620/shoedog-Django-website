from django.contrib import admin
from .models import Commment
# Register your models here.
@admin.register(Commment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','content_object','text','comment_time','user')