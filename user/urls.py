from django.urls import path, include

from user import views

urlpatterns = [
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('users/<str:username>/', views.get_user_details, name='get-user-details'),
    path('wallet/<str:username>/', views.find_user_wallet, name='find-user-wallet'),

]
