from django.urls import path
from .views import * 
from . import views

app_name = 'raghavapp'
urlpatterns =[
	path('',HomeView.as_view(),name='home'),
	path('signup/',SignupFormView.as_view(),name="signup"),
	path('login/',LoginFormView.as_view(),name="login"),
	path('logout/',LogoutView.as_view(),name="logout"),
	path('profile/',BlogCreateView.as_view(),name='profile'),
	path('bloglist/',BloglistView.as_view(),name='bloglist'),
	path('blog/<int:pk>/update/',BlogUpdateView.as_view(),name='blogupdate'),
	path("forgot-password/", PasswordForgotView.as_view(), name="passworforgot"),
    path("password-reset/<email>/<token>/",
         PasswordResetView.as_view(), name="passwordreset"),
]