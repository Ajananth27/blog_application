from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone


from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from blog.serializer import *
from blog.models import *

class UserRegisterForm(forms.Form):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserCreate(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        data = request.data
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        if not (username and email and password):
            return JsonResponse({"status": False, "message": "Please Check all the inputs."})
        register_form = UserRegisterForm(data)
        if register_form.is_valid():
            user, created = User.objects.get_or_create(
            username=username, email=email)
            if created:
                user.set_password(password)
                user.save()
                return JsonResponse({"status": True, "message": "User registered"})
            else:
                return JsonResponse({"status": False, "message": "User already Exists."})
        else:
            return JsonResponse({"status": False, "message": "Please Check all the inputs."})
    
class Login(APIView):

    # def get(self, request):
    #     return render(request, "login.html")

    def post(self, request):
        username = request.data.get("username").strip()
        password = request.data.get("password")
        if username is None or password is None:
            return JsonResponse({"error": "Please provide both username and password"})
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({"status": False, "message": "Invalid Credentials"})
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return JsonResponse({"status":True, "token":token})
            

class BlogView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            if "pk" in kwargs:
                blog = Blog.objects.filter(id=kwargs["pk"])
                serialize_data = BlobListSerializer(blog, many=True).data
            else:
                blog_lists = Blog.objects.filter(is_deleted=False).order_by("-created_at")
                serialize_data = BlobListSerializer(blog_lists, many=True).data
            return JsonResponse({"status": True, "data": serialize_data})
        except Exception as e:
            return JsonResponse({"status": False, "erroe":e})
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data["created_by_id"] = request.user.id
            if "pk" in kwargs:
                blog = Blog.objects.get(id=kwargs["pk"])
                serializ_data = BlobSerializer(blog, data=data)
            else:
                serializ_data = BlobSerializer(data=data)
            if serializ_data.is_valid():
                serializ_data.save()
                return JsonResponse({"status": True, "data": serializ_data.data})
            else:
                return JsonResponse({"status": False, "message":serializ_data.error_messages})
        except Exception as e:
            return JsonResponse({"status": False, "erroe":e})
    
    def delete(self, request, *args, **kwargs):
        try:
            blog = Blog.objects.get(id=request.data["blog_id"])
            blog.is_deleted = True
            blog.save()
            return JsonResponse({"status":True, "message": "Blog deleted."})
        except Exception as e:
            return JsonResponse({"status": False, "erroe":e})

class CommentView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        data["created_by_id"] = request.user.id
        comment_serializer = CommentSerializer(data=data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return JsonResponse({"status": True, "data": comment_serializer.data})
        else:
            return JsonResponse(comment_serializer.errors)
    
    def delete(self, request, *args, **kwargs):
        try:
            cmt = Comment.objects.get(id=request.data["comment_id"])
            cmt.is_deleted = True
            cmt.save()
            return JsonResponse({"status":True})
        except Exception as e:
            return JsonResponse({"status": False, "erroe":e})
