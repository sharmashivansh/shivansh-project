
import datetime
from datetime import datetime, timedelta
import arrow

from copy import deepcopy



from datetime import datetime



from math import ceil
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from accounts.serializers import *
from rest_framework import serializers
#administrator can add update delete and view the student and user


#am decalring user as a teacher and cerate a token 
class AdminsteratorViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SnippetSerializer

   
    def list(self, request):
        #on the basis of token it can be identify they are administerator or asistance or regular teacher
        if self.request.query_params.get('value')=='teacher':
            if self.request.user.role_id == 1:
                #declaring role_id which defines the constants of teacher in User model
                teacher=User.objects.filter(role_id=1,school__isnull=False)
                #in this we tak a snipperseralizer which is of User model (teacher )
                data= SnippetSerializer(teacher, many=True,context={"request": request}).data
                #then we give the response of teacher acording to its serializer 
                #we used serilaizer for two reason first is for required response and second is for validations 
                return Response({"data": data, "status":  status.HTTP_201_CREATED},
                                    status=status.HTTP_200_OK)

            elif self.request.user.role_id == 2:
                #now we havedefine 
                teacher=User.objects.filter(role_id=2,school__isnull=False)
                data= SnippetSerializer(teacher, many=True,context={"request": request}).data
                return Response({"data": data, "status":  status.HTTP_201_CREATED},
                                    status=status.HTTP_200_OK)
            elif self.request.user.role_id == 3:
                teacher=User.objects.filter(role_id=3,school__isnull=False)
                data= SnippetSerializer(teacher, many=True,context={"request": request}).data
                return Response({"data": data, "status":  status.HTTP_201_CREATED},
                                    status=status.HTTP_200_OK)


            else:
                #we used exclude to make sure only that techer (user) come which has no school in field
                teacher=User.objects.all().exclude(school__isnull=True)
                #then same we used snipet serializer of teacher 
                data= SnippetSerializer(teacher, many=True,context={"request": request}).data
                return Response({"data": data, "status":  status.HTTP_201_CREATED},
                                    status=status.HTTP_200_OK)
        else:
            #if we did not give any parma then eror comes with status 400 bad request
            return Response({"message": "please set a param of value", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_200_OK)





    

      

    def create(self, request, *args, **kwargs):
        #now we haveto create teacher and we hav eto store that ids of user which hav eno school
        school_null_user=User.objects.all().exclude(school__isnull=True)
        school_anomys=[]
        for i in school_null_user:
            school_anomys.append(i.id)

        if request.user.role_id == 1:
            
           
            teacher = User.objects.create( 

                first_name= request.data.get("first_name"),
                username=request.data.get('username'),
                last_name= request.data.get("last_name"),
                instrument= request.data.get("instrument"),
                email=request.data.get("email"),

                role_id=request.user.id)
            if request.data.get('school_id'):
                teacher.school_id=request.data.get('school_id')
                teacher.save()
                #used school _id foriegn key and used 
            
          
           
          
            return Response({"data":SnippetSerializer(teacher,context={"request": request}).data, 
                         "message": " Teacher is created succesfuly by Adminsterator message"}, status=status.HTTP_200_OK)
        
        elif request.user.id in school_anomys:
            #this define which have no permisiokn s
             teacher = User.objects.create( 

                first_name= request.data.get("first_name"),
                username=request.data.get('username'),
                last_name= request.data.get("last_name"),
                instrument= request.data.get("instrument"),
                email=request.data.get("email"),

                role_id=request.user.id)
            if request.data.get('school_id'):
                teacher.school_id=request.data.get('school_id')
                teacher.save()
            
          
           
          
            return Response({"data":SnippetSerializer(teacher,context={"request": request}).data, 
                         "message": " Teacher is created succesfuly by Adminsterator message"}, status=status.HTTP_200_OK)


        

        else:
             return Response({"message": "please check He is not an adminsterator", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_200_OK)


      



    @action(detail=False, methods=["delete"], url_path="delete")
    def delete(self, request):
        school_null_user=User.objects.all().exclude(school__isnull=True)
        school_anomys=[]
        for i in school_null_user:
            school_anomys.append(i.id)


        if request.user.role_id == 1:
            teacher_delete=User.objects.filter(id=request.query_params.get('id'))
                  
            teacher_delete.delete()
            return Response({"msg": "Teacher Deleted  Successfully ", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)


        elif request.user.id == 3:

            print(request.query_params.get('id'))
            
            usig=User.objects.filter(role_id=request.user.id)
            using=[]
            for i in usig:
                using.append(i.id)
            if request.query_params.get('id') in using:
                teacher_delete=User.objects.filter(id=request.query_params.get('id'))
                  
                teacher_delete.delete()
                return Response({"msg": "Teacher Deleted  Successfully ", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                    return Response({"message": "teacher id is  not present given requested Token", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_200_OK)

        elif request.user.id in school_anomys:
                teacher_delete=User.objects.filter(id=request.query_params.get('id'))
                  
                teacher_delete.delete()
                return Response({"msg": "Teacher Deleted  Successfully ", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        else:
             return Response({"message": "Provide  requested Token", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_200_OK)



     


    @action(detail=False, methods=["post"], url_path="edit_adminteacher")
    def edit_adminteacher(self, request, *args, **kwargs):
        if not request.user.role_id == 3:

            if request.query_params.get('teacher_id'):


                user = User.objects.get(id=request.query_params.get('teacher_id'))

                if (request.data.get("first_name", None)):
                    user.first_name = request.data.get("first_name", None)

                if (request.data.get("last_name", None)):
                    user.last_name = request.data.get("last_name", None)

               
                if (request.data.get("instrument", None)):
                    user.instrument = request.data.get("instrument", None)

                if (request.data.get("email", None)):
                    user.email = request.data.get("email", None)

                if (request.data.get("role_id", None)):
                    user.role_id = request.data.get("role_id", None)

               
                user.save()

                return Response({"msg": "user Updated sucessfully"}, status=status.HTTP_201_CREATED)

            else:
                return Response({"message": "please check teacher id is not in Token(instead of administrator and regular)", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_200_OK)


        else:
             return Response({"message": "asistance has no permissions to update records)", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_200_OK)










class AdminsteratorStudentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = StudentSerializer

   
    def list(self, request):
        if self.request.query_params.get('value')=='teacher':
            print(self.request.user)
            if self.request.user.role_id == 1:
                

                student=Student.objects.filter(user__isnull=False)
                data= StudentSerializer(student, many=True,context={"request": request}).data
                return Response({"data": data, "status":  status.HTTP_201_CREATED},
                                    status=status.HTTP_200_OK)

            elif self.request.user.role_id == 2:
                student=Student.objects.filter(user__isnull=False)
                data= StudentSerializer(student, many=True,context={"request": request}).data
                return Response({"data": data, "status":  status.HTTP_201_CREATED},
                                    status=status.HTTP_200_OK)
            elif self.request.user.role_id == 3:
                student=Student.objects.filter(user__role_id=3,user__isnull=False)
                data= StudentSerializer(student, many=True,context={"request": request}).data
                return Response({"data": data, "status":  status.HTTP_201_CREATED},
                                    status=status.HTTP_200_OK)

            else:
                return Response({"message": "Authorized Token is not of Administerator", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_200_OK)
        else:
            return Response({"message": "please set a param of value", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_200_OK)







    def create(self, request, *args, **kwargs):
        if request.user.role_id == 1:
            
           
            studnet = Student.objects.create( 

                first_name= request.data.get("first_name"),
                last_name= request.data.get("last_name"),
                skill_level=request.data.get("skill_level"),
                instrument= request.data.get("instrument"),
                email=request.data.get("email"),
                user=request.user.id,
                birthday=request.data.get("birthday")
                )

                
         
            
          
           
          
            return Response({"data":StudentSerializer(studnet,context={"request": request}).data, 
          
                         "message": " Teacher is created succesfuly by Adminsterator message"}, status=status.HTTP_200_OK)

    

        else:
             return Response({"message": "please check He is not an adminsterator", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_200_OK)



      




    @action(detail=False, methods=["post"], url_path="edit_adminteacher")
    def edit_adminstudent(self, request, *args, **kwargs):
        if not request.user.role_id == 2:


            if request.query_params.get('student_id'):


                student = Student.objects.get(user_id=request.query_params.get('student_id'))

                if (request.data.get("first_name", None)):
                    student.first_name = request.data.get("first_name", None)

                if (request.data.get("last_name", None)):
                    student.last_name = request.data.get("last_name", None)

               
                if (request.data.get("skill_level", None)):
                    student.instrument = request.data.get("skill_level", None)

                if (request.data.get("birthday", None)):
                    student.role_id = request.data.get("birthday", None)

                if (request.data.get("email", None)):
                    student.email = request.data.get("email", None)

                if (request.data.get("birthday", None)):
                    student.role_id = request.data.get("birthday", None)

               
                student.save()

                return Response({"msg": "student Updated sucessfully"}, status=status.HTTP_201_CREATED)

            else:
                return Response({"message": "please check teacher id is not in Token(instead of administrator and regular)", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_200_OK) last_name = models.CharField(max_length=255,null=True,blank=True)

        else:
            return Response({"message": "Assitance has no permission to update his student", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_200_OK) last_name = models.CharField(max_length=255,null=True,blank=True)


   