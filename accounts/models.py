from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone




TEACHER_ROLE = ((1, "Administrator"), (2, "Assistant"), (3, "Regular teacher"))


class School(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    school = models.CharField(max_length=255,null=True,blank=True)
    address=models.CharField(max_length=255,null=True,blank=True)
    phone_number= models.CharField(max_length=255,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'tbl_scho'
        verbose_name_plural = "scho"

    def __str__(self):
        return self.name if self.name else ''

        


class User(AbstractUser):
   first_name = models.CharField(max_length=255,null=True,blank=True)
   last_name = models.CharField(max_length=255,null=True,blank=True)
   username = models.CharField(max_length=255,null=True,blank=True, unique=True)
   teaching_since=models.DateTimeField(auto_now_add=True,null=True,blank=True)
   instrument= models.CharField(max_length=255,null=True,blank=True)
   school=models.ForeignKey(School, on_delete=models.CASCADE, related_name="teachers",null=True,blank=True)

   email=models.CharField(max_length=100, null=True, blank=True, unique=True)
   role_id = models.PositiveIntegerField(choices=TEACHER_ROLE, null=True,blank=True)
   created_on = models.DateTimeField(auto_now_add=True)
   updated_on = models.DateTimeField(auto_now_add=True)

   class Meta:
        managed = True
        db_table = 'tbl_user'

   def __str__(self):
        if self.email:
            return "{} ({})".format(self.email, self.id)



        


