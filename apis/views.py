from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apis.serializer import Signup, VideoSerializer
from apis.models import User, Video, Notification
from django.db import connection

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
    action(detail=False, method=['Post'])
    def create(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        video_data = request.data

        if not video_data.get('name') or not video_data.get('link'):
            return Response({"error":"Name and link required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with connection.cursor() as cursor:
                query = """INSERT INTO apis_video(user_id,name,created_at,views,link)
                VALUES (%s, %s, NOW(), %s, %s)"""

                cursor.execute(query,[
                    user.id,
                    video_data['name'],
                    video_data.get('views',0),
                    video_data['link']
                    
                ])

            return Response ({
                'user': user.first_name,
                'message':'Video Saved Successfully!'
            })
        
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, method=['Get'])
    def get_video(self, request, pk=None, video_pk=None):

        try:
            with connection.cursor() as cursor:
                user_query = """SELECT id, first_name 
                             FROM apis_user
                             WHERE id = %s"""
                cursor.execute(user_query,[pk])
                user = cursor.fetchone()

                if not user:
                    return Response({"status":"User Not Found"},
                                     status=status.HTTP_404_NOT_FOUND)
                
                user_id, first_name = user
                
            with connection.cursor() as cursor:
                video_query = """SELECT name, views, link, created_at
                                FROM apis_video
                                WHERE user_id = %s AND id = %s"""
                cursor.execute(video_query,[pk, video_pk])
                video = cursor.fetchone()

            if not video:
                return Response({"status":"Video Not Found"},
                                status=status.HTTP_404_NOT_FOUND)
            

            video_data = {
                'name': video[0],
                'views': video[1],
                'link': video[2],
                'created_at': video[3]
            }

            return Response({"user":first_name, "video":video}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response ({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=False, method= 'Delete')
    def delete_video(self,request, pk=None, video_pk=None):
            
        try:
            with connection.cursor() as cursor:
                user_query = """SELECT id, first_name
                                FROM apis_user 
                                WHERE id = %s"""
                
                cursor.execute(user_query,[pk])
                user = cursor.fetchone()

                if not user:
                    return Response({"error":"User Not Found"},
                                    status=status.http)
                
            
                user_id,first_name = user      

            with connection.cursor() as cursor:
                video_query = """SELECT name
                                FROM apis_video
                                WHERE id =%s and user_id=%s"""
                    
                cursor.execute(video_query,[video_pk,pk])
                video = cursor.fetchone()

                if not video:
                    return Response({"error":"Video Not Found"}, 
                                status=status.HTTP_404_NOT_FOUND)
                
                video_name = video[0]
            
            with connection.cursor() as cursor:
                delete_query = """DELETE FROM apis_video
                               WHERE id=%s AND user_id=%s"""
                cursor.execute(delete_query, [video_pk,pk])
            
            return Response({"status":"Deleted successfully",
                             "video":{"name":video[0]}},
                            status=status.HTTP_200_OK)
            

        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    @action(detail=True, method='Put')
    def update(self,request, pk=None, video_pk=None):
        try:
            new_name = request.data.get('name')
            with connection.cursor() as cursor:
                user_query = """SELECT id 
                             FROM apis_user
                             WHERE id = %s"""
                cursor.execute(user_query,[pk])
                user = cursor.fetchone()

                if not user:
                    return Response({"error":"User Not Found"},
                                    status=status.HTTP_404_NOT_FOUND)


            with connection.cursor() as cursor:
                video_query = """SELECT id
                                FROM apis_video
                                WHERE id = %s AND user_id = %s"""

                cursor.execute(video_query,[video_pk,pk])
                video = cursor.fetchone()

                if not video:
                    return Response({"error":"Video Not Found"},
                                    status=status.HTTP_404_NOT_FOUND)


            with connection.cursor() as cursor:
                update_query = """UPDATE apis_video
                               SET name = %s
                               WHERE id = %s"""
                
                cursor.execute(update_query,[new_name, video_pk])
                
                return Response({"status":"Video name updated",
                                "video":{"id":video_pk, "new_name": new_name}
                                })
            
        except Exception as e:
            return Response({"error":str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, method=['get'])   
    def all_videos(self, request, pk=None):

        try:
            with connection.cursor() as cursor:
                user_query = """SELECT first_name,id
                            FROM apis_user
                            WHERE id = %s"""
                           
                cursor.execute(user_query,[pk])
                user = cursor.fetchone()

                if not user:
                    return Response({"error":"user not found"},
                                    status=status.HTTP_404_NOT_FOUND)

            with connection.cursor() as cursor:
                all_videos_query = """SELECT *
                             FROM apis_video
                             WHERE user_id = %s"""
                
                cursor.execute(all_videos_query,[pk])
                videos = cursor.fetchall()

                if not videos:
                    return Response({"error":"videos not found"},
                                    status=status.HTTP_404_NOT_FOUND)
            
            return Response({"user":user,
                             "videos":videos},
                             status = status.HTTP_200_OK
                             )
        
        
        except Exception as e:
            return Response({'error':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SettingsViewSet(viewsets.ViewSet):
    @action(detail=False, method='Put')
    def profile(self,request,pk=None):

        try:
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            profile_image = request.data.get('profile_image')

            with connection.cursor() as cursor:
                if first_name is not None:
                    cursor.execute(
                                    """UPDATE apis_user
                                    SET first_name = %s
                                    WHERE id = %s""",
                                    [first_name,pk]
                    )
                
                                    

                if last_name is not None:
                    cursor.execute(
                                    """UPDATE apis_user
                                    SET last_name = %s
                                    WHERE id = %s""",
                                    [last_name,pk]
                    )

                if profile_image is not None:
                    cursor.execute(
                                     """UPDATE apis_user
                                     SET profile_image = %s
                                     WHERE id = %s""",
                                     [profile_image,pk]
                    )

                return Response({"status":"updated successfully"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error':str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FiltersViewSet(viewsets.viewset):
    def filter(self,request,method=['Get']):

        try:
            with connection.cursor() as cursor:
                if first_name = user.name

        


        



                

            
            







        
            
            
            




            
                    
            
                             

        
        

        
        

        





                




            
