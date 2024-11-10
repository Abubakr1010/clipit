from django.urls import path
from apis import views


urlpatterns =[
    path('signup/', views.SignupViewSet.as_view({'post':'signup'}), name='signup')
]
