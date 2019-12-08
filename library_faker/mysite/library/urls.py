from django.urls import path

from . import views

app_name = 'library'
urlpatterns = [
    path('', views.log_in, name="log_in"),
    path('library/', views.library_form, name='library'),
    path("check/", views.ssid_check, name="ssid"),
    path("get_room/", views.get_room, name="get_room")
]