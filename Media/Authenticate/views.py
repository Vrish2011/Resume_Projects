

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import json
from .models import User
from django.http import JsonResponse, HttpRequest
from datetime import datetime, timezone, timedelta
from django.views.decorators.csrf import csrf_exempt
import jwt
# Create your views here.

SECRET_KEY = "NP-0iij-0j0j--j--hhohp"

def create_access_token(data):
    return jwt.encode(data, SECRET_KEY, "HS256")

@csrf_exempt
def login_(request):
    if(request.method == "POST"):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        
        
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({"error" : "User does not exist"})
            
            
            
        
        
        access_token = create_access_token({"sub": "Logging in", "exp": datetime.now(timezone.utc) + timedelta(minutes=30)})
               
        login(request, user)
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        
        return JsonResponse({"user_id": user.id, "access_token": access_token }, safe=False)
       
        


@csrf_exempt
def register(request):
    if(request.method == "POST"):
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = User.objects.all()
        for u in user:
            print(u.username)
        if(request.method == "POST"):
            try:
                user = User.objects.get(username=username)
                if(user):
                    return JsonResponse({"error" : "User already exists"})
                    
                
            except:
               
                
                user = User(username=username, password=password)
                user.save()
                login(request, user)
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                access_token = create_access_token({"sub": "Registering", "exp": datetime.now(timezone.utc) + timedelta(minutes=30)})
                return JsonResponse({"error" : None, "user" : user.id, "access_token": access_token}, safe=False)
                


