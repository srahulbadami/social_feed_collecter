"""snowdens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from feedsocial.views import index,login,logout,google,twitter,facebook,fb,gplus,postdata,post
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^home/$', index, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$',logout, name='logout'),
    url(r'^twitter/$',twitter, name='twitter'),
    url(r'^facebook/$',facebook, name='facebook'),
    url(r'^gplus/$',gplus, name='gplus'),
    url(r'^postdata/$',postdata, name='postdata'),
    url(r'^fb/$',fb, name='fb'),
    url(r'^post/$', post),
    url(r'^googleecf773c21f59ea69.html$',google, name='googleecf773c21f59ea69'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^admin/', admin.site.urls),
]

