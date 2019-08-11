"""Pathlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
# myapp
from path_search.views import main, pathway, path_search
from enzyme_selection.views import enzyme, Enzyme_Information
from parts_design.views import parts, sequence_validation 


#import os

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, 
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, 
        {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', admin.site.urls),

    url(r'^pathlab/$', main),
    url(r'^pathway/$', pathway),
    url(r'^enzyme/$', enzyme),
    url(r'^parts/$', parts),

    url(r'^pathway_result/$', path_search),
    url(r'^enzyme_result/$',Enzyme_Information),
    url(r'^parts_result/$',sequence_validation ),
]
