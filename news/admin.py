from django.contrib import admin
from .models import Anews,BrandType
# Register your models here.
@admin.register(Anews)
class AnewsAdmin(admin.ModelAdmin):
    list_display = ('id','title','news_type','author','created_time','last_updated_time','get_read_num','broadcast_news')

@admin.register(BrandType)
class BrandType(admin.ModelAdmin):
    list_display = ('id','type_name')



