from django.urls import path

from .controllers import *


urlpatterns = [
    path('login', login_controller.login, name='login'),
    path('logout', login_controller.logout, name='logout'),
    path('teachers/', teacher_controller.teachers, name='response'),
    path('talk/response', talk_controller.do_response, name='response')
]
