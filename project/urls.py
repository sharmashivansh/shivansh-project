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

from django.conf import settings
from django.conf.urls import *

from django.contrib import admin

from accounts.views import *
from api import views

admin.autodiscover()

urlpatterns = [
                  url(r'^pages/', include('django.contrib.flatpages.urls')),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                
           
                  url(r'^admin/', admin.site.urls),
                  url(r'^jet/', include('jet.urls', 'jet')),
                  url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
         
                  url(r'accounts/', include('accounts.urls')),

                  url(r'api/', include('api.urls')),
       
                  
                  url('^accounts/', include('django.contrib.auth.urls')),
                 
                


              ] 
admin.site.site_header = "Welcome shivansh-project  Admin"
admin.site.index_title = "welcome Administration"
