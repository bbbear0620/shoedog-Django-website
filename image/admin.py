from django.contrib import admin
from .models import Image
# Register your models here.
@admin.register(Image)
class ImageRegister(admin.ModelAdmin):
    list_display = ('content_object', 'image','primal_pic')