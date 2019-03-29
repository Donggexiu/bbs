"""bbs URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from blog import views
from django.views.static import serve
from bbs import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.RegisterView.as_view(),name='regisrer'),
    url(r'^active/(.+)$',views.ActiveView.as_view(),name='active'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('index/',views.IndexVie.as_view(),name='index'),
    path('logout/',views.LogoutVie.as_view(),name='logout'),
    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^blog/',include('blog.urls')),#将所有的以blog开头的url都交给app下面的urls处理
    path('upload/',views.upload)


]
