from django.urls import path, include
from django.contrib import admin
from IVR_project.apps.IVR_web import views

urlpatterns = [
    path('', views.main_page, name='home'),
    path('login/', views.open_login, name='login'),
    path('confirm_login/', views.login_, name='confirm_login'),
    path('registration/', views.open_reg, name='registration'),
    path('confirm_reg/', views.registration, name='confirm_reg'),
    path('timeline/<int:timeline_id>/', views.open_tl, name='timeline'),
    path('event/<int:event_id>/', views.open_event, name='event'),
    path('profile/', views.profile, name='profile'),
    path('js/', views.js_test, name='test'),
    path('create_tl/', views.create_tl, name='create_tl'),
    path('create_event', views.create_event, name='create_event'),
    path('merge/', views.merge, name='merge'),
    path('reset/', views.send_reset_pass, name='reset'),
    path('set_new_pass/', views.set_new_pass, name='new_pass'),
    path('logout/', views.logout_, name='logout')
]