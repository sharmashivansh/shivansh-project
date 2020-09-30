'''
/**

 *
 * All Rights Reserved.
 * Proprietle, via any medium is strictly prohibited.
 *
 *
 */
'''
from django.conf.urls import url, include
from rest_framework import routers

from .views import *
from .viewsets import *

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'admins', AdminsteratorViewSet, basename='admins')
router.register(r'students', AdminsteratorStudentViewSet, basename='students')


urlpatterns = [
    url(r'', include(router.urls)),
   
]
