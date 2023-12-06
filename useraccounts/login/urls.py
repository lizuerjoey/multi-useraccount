from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name="loginpage"),
    path('login/existinguser/', views.validatelogin, name="validatelogin"),
    path('register/', views.registerpage, name="registerpage"),
    path('register/createadmin/', views.registeradmin, name="registeradmin"),
    path('home/', views.homepage, name="homepage"),
    path('home/addmember/', views.addmemberpage, name="addmemberpage"),
    path('home/addmember/add/', views.addmember, name="addmember"),
    path('logout/', views.logoutpage, name="logout"),
]
