from django.urls import path

from . import views

urlpatterns = [
    path('sign_out/', views.SignOut, name="signout"),
    path('login/', views.SignIn.as_view(), name="signin"),
]