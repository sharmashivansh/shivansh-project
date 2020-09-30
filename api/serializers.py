

import arrow
import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.flatpages.models import FlatPage
from rest_framework.validators import UniqueValidator

from accounts.models import *
from api.models import *
from rest_framework import serializers

class SchoolSerializer(serializers.ModelSerializer):
	class Meta:
	        model = School
	        fields = ['id', 'name', 'school', 'address', 'phone_number', 'created_on',"updated_on"]







class StudentSerializer(serializers.ModelSerializer):
	class Meta:
	        model = Student
	        fields = "__all__"






