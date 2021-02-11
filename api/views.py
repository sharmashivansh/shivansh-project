from django.shortcuts import render

# Create your views here.
from rest_framework import views,response,status,viewsets,permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.hashers import make_password
from project.constants import * 
from rest_framework_jwt.views import *
from django.contrib.auth import authenticate,login,get_user_model,logout
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from .permissions import BlacklistPermission
from _curses import OK
from .models import *
from .serializers import *
from post.serializers import SearchUserSerializer
from friend.models import FollowUnfollow
User = get_user_model()


"""
user login
"""
class LoginView(ObtainJSONWebToken):
    
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        
        data={}
        

        full_name = request.data.get('full_name', None)

        if not request.data.get("email",None):
            return Response({"error":"Plese enter email"},status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get("password",None):
            return Response({"error":"Plese enter password"},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(**request.data)
        if not user:
            return response.Response({"message":"Invalid login credentials."},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = Token.objects.get(user = user)
        except:
            token = Token.objects.create(user = user)
        
        try:
            device = Device.objects.get(created_by = user)
        except Device.DoesNotExist:
            device = Device.objects.create(created_by = user,device_type = 1)
            
        device.device_type = request.data['device_type']
        device.device_name = request.data['device_name']
        device.device_token = request.data['device_token']
        device.save()

        data = UserSerializer(user,context = {"request":request}).data
        data.update({"token":token.key})

        return Response({"data":data,"token":token.key,"status":status.HTTP_200_OK,"msg":"Login Successful",'url' : self.request.path}, status=status.HTTP_200_OK)

"""
delete user
"""
class DeleteUser(views.APIView):
    
    def post(self,request,*args,**kwargs):
        user = User.objects.filter(id = request.user.id)
        if not user:
            return response.Response({"msg":"You are not valid user"},status = status.HTTP_400_BAD_REQUEST)
        user = user[0]
        user.delete()
        return response.Response({"msg":"Successfully delete your self"},status = status.HTTP_200_OK)
    
"""
User registration
""" 
class UserRegister(views.APIView):
    def post(self,request,*args,**kwargs):
        if not request.data.get("full_name",None):

            return response.Response({"message":"Please enter full name of user."},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("username",None):

            return response.Response({"message":"Please enter username of user."},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("email",None):
            return response.Response({"message":"Please enter email of user."},status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get("password",None):
            return response.Response({"message":"Please enter password ."},status=status.HTTP_400_BAD_REQUEST)

        if len(request.data.get("password")) < 8:
            return response.Response({"message":"Please enter minimum 8 digit password."},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=request.data.get("email")):
            return response.Response({"message":"User allready exist with same email."},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=request.data.get("username")):
            return response.Response({"message":"User already exist with same username."},status=status.HTTP_400_BAD_REQUEST)
        dt={
            "full_name":request.data.get("full_name"),
            "username":"_".join(request.data.get("username").lower().split(" ")),
            "email":request.data.get("email"),
            "gender":request.data.get("gender"),
            "dob":request.data.get("dob"),
            "password":make_password(request.data['password']),
        }
        

        try:
            user = User.objects.get(**dt)
        except User.DoesNotExist:
            user = User.objects.create(**dt)        
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        data = UserSerializer(user,context={"request":request}).data
        data.update({"token":token.key})

        return Response({"data":data,"token":token.key,"status":status.HTTP_200_OK,"msg":"Registration done Successful",'url' : self.request.path}, status=status.HTTP_200_OK)

"""
Check username 
"""
class CheckUserName(views.APIView):
    permission_classes = (permissions.AllowAny,)


    def post(self, request, *args, **kwargs):
        user_name = User.objects.filter(username = request.data.get("username"))
        if user_name:
            return Response({"error":"This username is already taken. please try again!"},status = status.HTTP_400_BAD_REQUEST)
        
        return Response({"msg":"success"})

"""
user logout
"""
class UserLogout(views.APIView): 
    permission_classes = (permissions.IsAuthenticated,) 
        
    def get(self, request):     
        logout(request)       
        response = {

            'message':'Successfully logout.',
            'status' : 200,  
            'url' : request.path,
            }
          
        return Response(response)

"""
user check api
"""
class UserCheckApi(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        try:
            token = Token.objects.get(user = user)
        except:
            token = Token.objects.create(user = user)
        msg="Check User Api"
        data=UserSerializer(user,context = {"request":request}).data
        data.update({"token":token.key})
            
        response = {
            "data":data,
            'msg': msg,
            "status": status.HTTP_200_OK,
            'url' : request.path
        }   
        
        return Response(response)

"""
forgot password
"""
class ForgotPassword(views.APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        if not request.data.get("email", None):
            return Response({
                'message': "Please enter email.",
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email = request.data.get("email"))
        if not user:
            if request.data.get("email").isdigit():
                return Response({
                    'message': "Mobile number does not exist",
                }, status = status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': "Email does not exist",
            }, status = status.HTTP_400_BAD_REQUEST)

        user = user[0]
        activation_link = user.id
        message = "Hello {0},\n {1}".format(user.username, activation_link)
        mail_subject = 'Reset your account.'
        to_email = request.data.get('email')
        
        try:
            send_mail(mail_subject, message, recipient_list = [to_email], from_email=settings.EMAIL_HOST_USER)
        except Exception as e:
            print(e)
            pass
        
        response = {
            'message': "Email has been send to your email id. please Check to reset your password",
            'to_email': to_email,
        }
        return Response(response, status = status.HTTP_200_OK)

"""
reset password
"""
class PasswordReset(views.APIView):
    
    def post(self,request,*args,**kwargs):
        if  request.data.get("email",None):
            
            user = User.objects.filter(email=request.data.get("email"))
        else:
            user = User.objects.filter(id=request.user.id)
    
            
        if not user:
            return response.Response({"error":"Not a valid user"},status = status.HTTP_400_BAD_REQUEST)
        user = user[0]
        user.set_password(request.data.get("password",None))
        user.save()
        return response.Response({"msg":"Successfully update you password"},status = status.HTTP_200_OK)

"""
user profile edit 
"""
class ProfileEditView(views.APIView):  
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        data={}

        if request.data.get("username",None):
            data["username"] = request.data.get("username")

        if  request.data.get("full_name",None):
            data["full_name"] = request.data.get("full_name")

        if  request.data.get("dob",None):
            data["dob"]=request.data.get("dob")

        if  request.data.get("description",None):
            data["description"] = request.data.get("description")

        if  request.data.get("gender",None):
            data["gender"] = request.data.get("gender")

        user = request.user

        for attr,value in data.items():
            setattr(user, attr, value)

        if request.FILES.get("avatar",None):
            user.avatar=request.FILES.get("avatar") 

        user.save()

        return Response({"data":UserSerializer(user,context={"request":request}).data,
                         "msg":"Profile updated successfully.","url":request.path},
                         status=status.HTTP_200_OK) 


"""
change password view
"""
class ChangePasswordView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not request.data.get("new_password", None):
            return Response({"message": "Please set a password"}, status=status.HTTP_400_BAD_REQUEST)

        self.user = request.user
        self.user.set_password(request.data.get("new_password"))
        self.user.save()
        try:
            self.user.auth_token.delete()
        except Exception as e:
            print(e)
            pass
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        

"""
terms and conditions view
"""
class TermsViewsets(viewsets.ModelViewSet):
    serializer_class = FlatPageSerializer

    def list(self, request):
        contact = FlatPage.objects.filter(title = 'Terms of use').first()
        if not contact:
            response = {
                'data': '',
                'error': 'No data found',
                'url': request.path,
            }
        else:
            response = {
                'data': {
                    "title": contact.title,
                    "content": contact.content
                },
                'url': request.path,
            }
        return Response(response, status = status.HTTP_200_OK)
    
class Registrations(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserssSerializers(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message": "User successfully register."}, status=status.HTTP_201_CREATED)
        else:
            error_msg = ""
            for index, err in serializer.errors.items():
                error_msg = err[0]
                break

            return Response({"message": error_msg}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):


        username = request.data.get('username', None)
        password = request.data.get('password', None)
       
        data = {}

        user = authenticate(username=username, password=password)


        if not user:
            return Response({"message": "Email/Mobile no or Password is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({"message": "Please check you email and click on link to activate your account"},
                            status=status.HTTP_403_FORBIDDEN)

        if user.role_id != request.data.get('role_id', None):
            return Response({"message": "You are not allowed to perform this action"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not (user.status == 1):
            return Response({"message": "Please contact admin to approve your account"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user.auth_token.delete()
        except Exception as e:
            print(e)
            pass

        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        try:
            device = Device.objects.get(created_by=user)
        except Device.DoesNotExist:
            device = Device.objects.create(created_by=user)

        device.device_type = request.data.get('device_type', None)
        device.device_name = request.data.get('device_name', None)
        device.device_token = request.data.get('device_token', None)
        device.save()

        data = UserSerializers(user, context={"request": request}).data
        data.update({"token": token.key, "timing": [model_to_dict(t) for t in user.timing.all()]})
        try:
            if user.role_id == 4:
                driver = user.driver
                data.update({"age": driver.age, "driving_license": request.build_absolute_uri(
                    driver.driving_license.url) if driver.driving_license else "",
                             "rc_number": driver.rc_number,
                             "vehicle_type": driver.vehicle_type})
        except:
            pass
        cart_count = Cart.objects.filter(user=user).count()

        return Response({"data": data, "cart_count": cart_count, "message": "Login Successful"},
                        status=status.HTTP_200_OK)

      
      
class ChatingViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChatingSerializer

    def get_queryset(self):
        if self.request.query_params.get("receiver_user") is None:
            return Chating.objects.filter(Q(sender_user = self.request.user.id)|Q(receiver_user = self.request.user.id ))
        else:
            chatings = Chating.objects.filter(
                Q(sender_user = self.request.user.id,receiver_user_id = self.request.query_params.get("receiver_user"))|
                Q(sender_user =self.request.query_params.get("receiver_user"),receiver_user_id =  self.request.user.id)
            )
            print(chatings)
            if not chatings:
                response.Response({"message":"Invialid chating."},status = status.HTTP_400_BAD_REQUEST)
           
            return chatings    



#send a message to Muliplte users  
    def create(self,request,*args,**kwargs):
        user = request.user

        if not request.query_params.get("receiver_user",None):
            response.Response({"message":"Please select a receiver user to start chat."},status=status.HTTP_400_BAD_REQUEST)

        id = request.query_params.get("receiver_user",None)

        if not id:
            return Response({"error":"Please set receiver user to start chat."},status = 400)

        users = User.objects.filter(id__in = [int(x) for x in id.split(',')]).values_list("id",flat = True)
        image =[]
        imagelink = []
        post_detail = []
        timeline_detail = []
        journey_detail = []

        for user_id in users:

            try:
                chating = Chating.objects.get(Q(sender_user = user,receiver_user_id = user_id)|Q(sender_user = user_id,receiver_user_id = user))
            
            except Chating.DoesNotExist:
                chating = Chating.objects.create(sender_user = user,receiver_user_id = user_id)

            if request.data.get("post_detail",None):
                user_post = Post.objects.filter(id__in = request.data.get("post_detail")).values_list("date",flat = True)
                post_detail.append(request.data.get("post_detail"))

            if request.data.get("timeline_detail",None):
                user_post = TimeLine.objects.filter(id__in = request.data.get("timeline_detail")).values_list("created_on",flat = True)
                timeline_detail.append(request.data.get("timeline_detail"))

            if request.data.get("journey_detail",None):
                user_post = Journey.objects.filter(id__in = request.data.get("journey_detail")).values_list("date",flat = True)
                journey_detail.append(request.data.get("journey_detail"))

            for i in range(0,int(request.data.get("image_count",'0'))+1):
                if request.FILES.get("image{}".format(i),None):
                    message = Message.objects.create(sender_user=user,chating_id = chating.id,image = request.FILES.get("image{}".format(i)),text = request.data.get("text"),link = request.data.get("link"),share_post = request.data.get("share_post"),share_timeline = request.data.get("share_timeline"),share_journey = request.data.get("share_journey"),receiver_user_id = user_id,created_on=datetime.now(pytz.timezone(my_tz_name)).strftime('%Y-%m-%d %H:%M:%S'))                                       
                    image.append(message)
                    imagelink.append("/media/chating/"+request.FILES.get("image{}".format(i)).name)

            if not request.FILES.get("image{}".format(i)):
                message = Message.objects.create(sender_user = user,chating_id = chating.id,text = request.data.get("text"),link = request.data.get("link"),share_post = request.data.get("share_post"),share_timeline = request.data.get("share_timeline"),share_journey = request.data.get("share_journey"),receiver_user_id = user_id,created_on=datetime.now(pytz.timezone(my_tz_name)).strftime('%Y-%m-%d %H:%M:%S'))
                image.append(message)

            if post_detail:
                for p in post_detail:
                    message.post_detail.add(str(p))

            if timeline_detail:
                for t in timeline_detail:
                    message.timeline_detail.add(str(t))

            if journey_detail:
                for j in journey_detail: 
                    message.journey_detail.add(str(j))

        message.save()
        data= MessageSerializer(message,context = {"request":request}).data
        chating_ids=data['chating_id']

        chating=Chating.objects.filter(id=chating_ids)
        chating.update(deleted_by_sender = 0)
        chating.update(deleted_by_receiver = 0)
        chating.update(created_on=datetime.now(pytz.timezone(my_tz_name)).strftime('%Y-%m-%d %H:%M:%S'))

        data.update({"images":imagelink}) 
       

        return Response({"data":data,"message":"Message send Successfully."},status=200)
