from django.urls import path
from apis import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


urlpatterns =[
    path('signup/', views.SignupViewSet.as_view({'post':'signup'}), name='signup'),
    path('login/', views.LoginViewSet.as_view({'post':'login'}), name='login'),
    path('create/<int:pk>/', views.VideoViewSet.as_view({'post':'create',}), name='create'),
    path('update/<int:pk>/<int:video>/', views.VideoViewSet.as_view({'update':'update'}), name='update_video'),
    path('delete_video/<int:pk>/<int:video_pk>/', views.VideoViewSet.as_view({'delete':'delete_video'}), name='get_video'),
    path('get_video/<int:pk>/<int:video_pk>/', views.VideoViewSet.as_view({'get':'get_video'}), name='get_video'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
   
]
