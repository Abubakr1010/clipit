from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apis.serializer import Signup, VideoSerializer
from apis.models import User, Video, Notification

# Create your views here.

class SignupViewSet(viewsets.ViewSet):

    @action(detail=False, method=['Post'])
    def signup(self,request):
        serializer = Signup(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data=({'id': user.id,
                            'email':user.email
                            })
            return Response(response_data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        

class LoginViewSet(viewsets.ViewSet):

    @action(detail=False, method=['Post'])
    def login(self,request):

        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error":"fill all fields"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"User not found"}, status=status.HTTP_400_BAD_REQUEST)

        
        if not user.check_password(password):
            return Response({"error":"Invalid Password"})
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"refresh": str(refresh),
                         "acess": access_token,
                         "success":f"{user} logged in successfully"}, status=status.HTTP_200_OK)


class VideoViewSet(viewsets.ViewSet):
    action(detail=False, method=['Post','Get'])
    def video(self, request, pk=None):
        user = User.objects.get(pk=pk)
        video = Video.objects.get(pk=pk)
        
        if request.method == 'Post':
            serializer = VideoSerializer()
            if serializer.is_valid():
                serializer.save()
                return Response({'user':user.first_namea,
                             'data':serializer.data})
        else:
            return Response({'error':'Your video was not saves'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if user.request == 'Get':
            serializer = VideoSerializer(video)
            if serializer.is_valid():
                serializer.save()
                return Response({'video':serializer.data},
                                 status=status.HTTP_200_OK)