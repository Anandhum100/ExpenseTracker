from django.urls import path
from Accounts import views 
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView





urlpatterns = [
    
path('register/', views.register, name='register'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('custom_password_reset/', views.custom_password_reset, name='custom_password_reset'),
path('forgetpassword/',views.FORGOTPASSWORD, name='forgotpassword'),
path('profileupdate/',views.profileupdate, name='profileupdate'),

path('password_reset/', PasswordResetView.as_view(template_name='custom_password_reset.html'), name='password_reset'),
path('password_reset/done/', PasswordResetDoneView.as_view(template_name='forgotpassword.html'), name='password_reset_done'),
path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_success.html'), name='password_reset_complete'),






    
]