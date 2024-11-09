from django.urls import path
from apis import views


urlpatterns =[
    path('signup/', views.SignupViewSet({'post':'signup'}, name='signup'))
]
