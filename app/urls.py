from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('init',views.GoogleCalendarInitView),
	path('redirect',views.GoogleCalendarRedirectView)
]