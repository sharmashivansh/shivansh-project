'''
/**

 *
 * All Rights Reserved.
 * Proprietary and confidential :  All information contained herein is, and remains
 * the property and its partners.
 * Unauthorized copying of this file, via any medium is strictly prohibited.
 *
 *
 */
'''
from accounts import views
from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse_lazy

from .views import *

admin.autodiscover()

app_name = 'accounts'

urlpatterns = [
   
]
