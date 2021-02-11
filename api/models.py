from django.db import models

# Create your models here.



from accounts.models import *


from post.models import Post
from timeline.models import TimeLine 
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import default
from journey.models import Journey
from timeline.models import TimeLine
from django.utils import timezone
from django.template.defaultfilters import default
from journey.models import Journey

User = get_user_model()

class Chating(models.Model):
    sender_user = models.ForeignKey(User,related_name="chat_sender",on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(User,related_name="chat_receiver",on_delete=models.CASCADE)
    created_on = models.TextField(null=True,blank=True)
    deleted_by_sender = models.IntegerField(default=0,blank=True,null=True)
    deleted_by_receiver = models.IntegerField(default=0,blank=True,null=True)
      
    def __unicode__(self):
        return self.sender_user
    
class Message(models.Model):
    sender_user = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)   
    text = models.TextField(null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    image = models.ImageField(upload_to="chating",null=True,blank=True)
    chating = models.ForeignKey(Chating,related_name="messages",on_delete=models.CASCADE)
    created_on =models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False)
    share_post = models.IntegerField(default=False,null=True,blank=True)
    share_timeline = models.IntegerField(default=False,null=True,blank=True)
    share_journey = models.IntegerField(default=False,null=True,blank=True)
    post_detail = models.ManyToManyField(Post,blank=True,default=False)
    timeline_detail = models.ManyToManyField(TimeLine,blank=True,default=False)
    journey_detail = models.ManyToManyField(Journey,blank=True,default=False)
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    deleted_by_sender = models.IntegerField(default=0,blank=True,null=True)
    deleted_by_receiver = models.IntegerField(default=0,blank=True,null=True)
       
        
    def save(self,*args,**kwargs):
        return super().save(*args,**kwargs)
        
    class Meta:
        ordering = ['created_on']





class Student(models.Model):
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    skill_level=models.CharField(max_length=255,null=True,blank=True)
    instrument= models.CharField(max_length=255,null=True,blank=True)

    student_since=models.DateTimeField(auto_now_add=True)

    email=models.CharField(max_length=100, null=True, blank=True, unique=True)
    
  

    user=models.ForeignKey(User, related_name="teacher", on_delete=models.CASCADE, null=True,
                                   blank=True, editable=True)

    birthday= models.DateTimeField(null=True,blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'tbl_studenttt'
        verbose_name_plural = "studenttt"

    def __str__(self):
        return self.first_name if self.first_name else ''
    
class Device(models.Model):
       
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='device')
    device_type = models.PositiveIntegerField(choices=DEVICE_TYPE,null=True,blank=True)
    device_name = models.CharField(max_length=50,null=True,blank=True)
    device_token = models.CharField(max_length=500,null=True,blank=True)
    
    class Meta:
        managed = True
        db_table = 'tbl_device'
