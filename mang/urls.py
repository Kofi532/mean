"""mang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from users import views as uvs
from report import views as rvs
from uploading.views import SignUpView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('uploading.urls', namespace="uploading")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("add/", uvs.adduser, name='adduser'),
    path("display/", uvs.display, name='display'),
    path("download/", uvs.download3, name='download'),
    path("fees/", uvs.fees, name='fees'),
    path("deleteclass/", uvs.deleteclass, name='deleteclass'),
    path("addsub/", rvs.report_reg, name='subj'),
    path("downloadsub/", rvs.download_sub, name='download_subj'),
    path("uploadsub/", rvs.upload_report, name='upload_subj'),
    path("reportcards/", rvs.report_cards, name='report_cards'),
    path("signup/", SignUpView.as_view(), name='signup'),
    path("addclass/", uvs.addclass, name='addclass'),    
    path("sem/", uvs.sem, name='sem'),
    path("registerschool/", uvs.registerschool, name='registerschool'),    
    path("updateschool/", uvs.updateschool, name='updateschool'),    
]

