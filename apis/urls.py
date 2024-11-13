from django.urls import path
from apis import views


urlpatterns =[
    path('signup/', views.SignupViewSet.as_view({'post':'signup'}), name='signup'),
    path('login/', views.LoginViewSet.as_view({'post':'login'}), name='login')
]
