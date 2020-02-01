from django.conf.urls import url
from django.contrib import admin

from judge.views import *

urlpatterns = [
    # example : /professor
    url(r'^professor$', ProfessorMainLV.as_view(), name='professor'),
]
