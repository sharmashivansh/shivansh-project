from django.db import models

# Create your models here.



from accounts.models import *





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