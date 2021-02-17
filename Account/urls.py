from django.urls import path,include,re_path
from knox import views as knox_views
from .views import *
app_name = 'Account'

urlpatterns = [
    re_path('^validate_phone/',ValidatePhoneSendOTP.as_view()),
    re_path('^register/',Register.as_view()),
    re_path('^login/',LoginAPI.as_view()),
    re_path('^logout/$',knox_views.LogoutView.as_view()),
]