from rest_framework.views import APIView
from rest_framework.response import Response
from .models import company_name
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import themes,SignInUser
import requests
from rest_framework import status
from.serializers import ThemesSerializer
from django.shortcuts import get_object_or_404

class ThemeView(APIView):
    def post(self,request):
        user_id=request.data.get("user_id")
        header=request.data.get("header")
        navbar=request.data.get("navbar")
        body=request.data.get("body")
        legs=request.data.get("legs")

        # Retrieve the user
        userr = get_object_or_404(SignInUser, user_id=user_id)

        # Check if a theme already exists for this user
        theme_instance, created = themes.objects.get_or_create(user_id=userr)

        # If theme exists, update the fields
        theme_instance.header = header
        theme_instance.navbar = navbar
        theme_instance.body = body
        theme_instance.legs = legs

        theme_instance.save()  # Save the changes

        return Response(
            {"message": "Theme updated" if not created else "Theme created"},
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
        )
        
class ThemeRetrive(APIView):
    def post(self,request):
        user_id=request.data.get("user_id")
        userr=SignInUser.objects.get(user_id=user_id)

        # Retrieve the theme for this user
        theme_instance = get_object_or_404(themes, user_id=userr)

        # Serialize the theme data
        serializer = ThemesSerializer(theme_instance)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    



