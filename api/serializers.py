

import arrow
import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.flatpages.models import FlatPage
from rest_framework.validators import UniqueValidator

from accounts.models import *
from api.models import *
from rest_framework import serializers
from rest_framework import serializers
from user.serializers import UserChatSerializer , UserSerializer
from .models import Chating, Message
from django.db.models import Q
from rest_framework.response import Response
from user.models import User
from journey.serializers import JourneySerializer
from post.serializers import PostAuthorSerializer
from timeline.serializers import TimelineAuthorSerializer
from rest_framework import serializers as Serializers
from rest_framework_jwt import serializers
from django.contrib.auth import get_user_model
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password
from post.models import Post
from user.models import *
from friendship.models import Friend
from friend.models import FollowUnfollow

User = get_user_model()

"""
User's friend serializer
"""
class FriendUserSerializer(Serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','full_name','first_name','last_name','description','avatar','user_status','dob','social_id','social_type','mobile_no','gender','state','user_status')


"""
user serializer
"""
class UserSerializer(Serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','full_name','username','email','description','avatar','user_status','dob','social_id','social_type','mobile_no','gender','state','user_status')
        read_only_fields=('username',)


"""
user chat serializer
"""
class UserChatSerializer(Serializers.ModelSerializer):
    avatar = Serializers.ImageField(read_only = True)
    class Meta:
        model = User
        fields = ('id','username','full_name','first_name','last_name','email','avatar','user_status')

        
"""
device serializer
"""
class DeviceSerializer(Serializers.ModelSerializer):
    
    class Meta:
       model = Device
       fields = "__all__"


"""
login serializer
"""
class LoginSerializer(serializers.JSONWebTokenSerializer):
    def validate_email(self,value):
        if not value or value == '':
            raise serializers.ValidationError("Please enter email.")
        return value
    
    def validate_password(self,value):
        if not value or value == '':
            raise serializers.ValidationError("Please enter password.")
        return value
    
"""
"""
chating list serializer
""" 
class ChatingListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chating
        fields = ('id',)

"""
message serializer
"""
class MessageSerializer(serializers.ModelSerializer):
    ids = ChatingListSerializer(read_only = True, many = True)
    link = serializers.URLField(required = False,read_only = False)
    created_on = serializers.SerializerMethodField()
    sender_user = UserChatSerializer(read_only = True)
    receiver_user = UserChatSerializer(read_only = True)
    share_journey = JourneySerializer(read_only = True)
    post_detail = PostAuthorSerializer(read_only = True, many = True)
    timeline_detail = TimelineAuthorSerializer(read_only = True, many = True)
    journey_detail = JourneySerializer(read_only = True, many = True)
    
    class Meta:
        model = Message
        fields = ('id','text','created_on','image','link','sender_user','receiver_user','is_read','share_post','post_detail','share_timeline','timeline_detail','chating_id','share_journey','journey_detail','ids')

    def get_created_on(self,obj):
        return obj.created_on#.strftime('%Y-%m-%d %H:%M:%S')

"""
chating serializer
"""
class ChatingSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only = False, many = True)
    sender_user = serializers.SlugRelatedField(many = False, slug_field = 'username', queryset = User.objects.all())
    receiver_user= serializers.SlugRelatedField(many = False, slug_field = 'username', queryset = User.objects.all())
    created_on = serializers.SerializerMethodField()


    class Meta:
        model = Chating
        fields = ('id','messages','sender_user','receiver_user','created_on','deleted_by_sender','deleted_by_receiver')

    def get_created_on(self,obj):
        return obj.created_on#.strftime('%Y-%m-%d %H:%M:%S')


class SchoolSerializer(serializers.ModelSerializer):
	class Meta:
	        model = School
	        fields = ['id', 'name', 'school', 'address', 'phone_number', 'created_on',"updated_on"]







class StudentSerializer(serializers.ModelSerializer):
	class Meta:
	        model = Student
	        fields = "__all__"






