from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apis.serializer import Signup

# Create your views here.

class SignupViewSet(viewsets.Viewset):

    @action(detail=False, method=['Post'])
    def signup(self,request):
        serializer = Signup(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data=({'id': user.id,
                            **serializer.data})
            return Response(response_data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        

    
