

import arrow
import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.flatpages.models import FlatPage
from rest_framework.validators import UniqueValidator

from accounts.models import *
from api.models import *
from rest_framework import serializers

from api.serializers import *

class SnippetSerializer(serializers.ModelSerializer):
	school = SchoolSerializer()
	class Meta:
	        model = User
	        fields = ['id', 'first_name', 'last_name', 'school', 'email', 'teaching_since']