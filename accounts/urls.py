from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
	path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
	path('sign_in/', views.SignInView.as_view(), name='sign_in'),
	path('sign_out/', views.SignOutView.as_view(), name='sign_out'),
	path('dashboard/<int:pk>/', views.DashboardView.as_view(), name='dashboard'),
]