from .views import home,GoogleCalendarInitView,GoogleCalendarRedirectView
from django.urls import path,include

urlpatterns=[
    path('',home,name='home'),
    path('rest/v1/calendar/init',GoogleCalendarInitView.as_view()),
    path('rest/v1/calendar/redirect',GoogleCalendarRedirectView().as_view())
]