from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tutorials/', views.tutorials, name='tutorials'),
    path('add_general_info/', views.add_general_info, name='add_general_info'),
    path('update_general_info/<int:info_id>/',
         views.update_general_info, name='update_general_info'),
    path('delete_general_info/<int:info_id>/',
         views.delete_general_info, name='delete_general_info'),
    path('add_tutorial/', views.add_tutorial, name='add_tutorial'),
    path('update_tutorial/<int:tutorial_id>/',
         views.update_tutorial, name='update_tutorial'),
    path('delete_tutorial/<int:tutorial_id>/',
         views.delete_tutorial, name='delete_tutorial'),
    path('get_weather_data/<str:city>/',
         views.get_weather_data, name='get_weather_data'),


]
