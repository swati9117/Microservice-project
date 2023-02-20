from django.urls import path,include
from .views import RegisterView,LoginView,LogoutView,AppointmentUpdateAPIView,AppointmentAPIView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
   # path('look/',appview.as_view()),
   
    path('appointment/',AppointmentAPIView.as_view()),
    path('editappointment/<int:slug>/',AppointmentUpdateAPIView.as_view())
    # path('deleteappointment/<int:slug>/',AppointmentDeleteAPIView.as_view())




]