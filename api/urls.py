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

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'accounts/password-reset/$', ResetPassword.as_view(), name="account_password_reset"),
    url(r'user/signup/', Registrations.as_view(), name="signup"),
    url(r'user/login/', UserLoginView.as_view(), name="login"),
]
