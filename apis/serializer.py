from rest_framework import serializers
from apis.models import User, Notification, Video

class Signup(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['profile_image','first_name','last_name','email','password']
    
    def validate(self,data):
        email = data.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':'email with this user already exists'})
        
        password = data.get('password')
        if len(password) < 7:
            raise serializers.ValidationError({'password':'password must be atleast 7 digit long'})
        
        if not any (char.isupper() for char in password):
            raise serializers.ValidationError({'password':'password should have at least one upper case'})
        
        return data
        

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class VideoSerializer(serializers.Serializer):

    class Meta:
        Model = Video
        fields = ['id','name','user','created_at','views','link']
        




