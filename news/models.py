from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistic.models import ReadNumExpandMethod,ReadDetail,ReadNum
from comment.models import Commment
from image.models import Image
from likes.models import LikeRecord,LikesAllCount
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

class BrandType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

class Anews(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    #main_image = models.ImageField(upload_to='news_image/%Y/%m/%d',default=None,null=True,blank=True)
    news_type = models.ForeignKey(BrandType,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_time  = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    broadcast_news = models.BooleanField(default=False)

    read_details = GenericRelation(ReadDetail)
    read_num = GenericRelation(ReadNum)
    comments = GenericRelation(Commment)
    image = GenericRelation(Image)
    likerecord = GenericRelation(LikeRecord)
    likeallcount = GenericRelation(LikesAllCount)

    def __str__(self):
            return '<news:%s>'%self.title

    class Meta:
        ordering = ['-created_time']






