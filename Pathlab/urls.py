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
from path_search.views import main, pathway,  pathway_information, complete,path_search_full,path_search_one,path_show,compound_info
from enzyme_selection.views import enzyme, Enzyme_Information
from parts_design.views import parts, sequence_validation, parts_search, show_sequence, sequence_validation_post, full_sequence

from account.views import Defaultlogin, Login, Defaultregister, Register, advice, guest_advice, logout, enzyme_comment
from report.views import sequence_download, Report


#import os

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, 
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, 
        {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', admin.site.urls),

    url(r'^$', main),
    url(r'^pathlab/$', main),
    url(r'^pathway/$', pathway),
    url(r'^enzyme/$', enzyme),
    url(r'^parts/$', parts),

    url(r'^pathway_result_full/$', path_search_full),
    url(r'^pathway_result_one/$', path_search_one),

    url(r'^pathway_information/(?P<cID>.*)/(?P<compounds>.*)/(?P<reactions>.*)/(?P<enzymes>.*)/$', pathway_information, name="pathway_information"),
    url(r'^enzyme_result/$',Enzyme_Information),
    url(r'^parts_result/(?P<seq>.*)/(?P<organism>.*)$',sequence_validation, name="sequence_validation"),
    url(r'^sequence_validation_post/$',sequence_validation_post),
    url(r'^parts_search/$',parts_search),
    url(r'^path_show/$',path_show),
    url(r'^compound_info/$',compound_info),
    

    url(r'^sequence_result/(?P<infor1>.*)$',show_sequence, name="sequence_result"),
    url(r'^full_sequence/(?P<seq>.*)$',full_sequence, name="full_sequence"),
    
    
    url(r'^advice/$',advice),
    url(r'^guest_advice/$', guest_advice),
    
    url(r'^login/$', Defaultlogin),
    url(r'^Login/$', Login),
    url(r'^register/$', Defaultregister),
    url(r'^Register/$', Register),
    url(r'^logout/$', logout),
    url(r'^enzyme_comment/$', enzyme_comment),
    
    url(r'^complete/$',complete),
    url(r'^sequence_download/$',sequence_download),
    # url(r'^Report/(?P<compounds>.*)/(?P<enzymes>.*)/(?P<seq_data>.*)$',Report, name="Report"),
    url(r'^Report/$',Report),
]




