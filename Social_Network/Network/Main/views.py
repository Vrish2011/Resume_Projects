from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import json

from django.http import JsonResponse, HttpRequest
from datetime import datetime, timezone, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

SECRET_KEY = "NP-0iij-0j0j--j--hhohp"

def login_template(request):
    return render(request, "Main/index.html")

def home_template(request):
    return render(request, "Main/index.html")
    

def register_template(request):
    return render(request, "Main/index.html")


def verify_token(access_token):
    
    try:
        data = jwt.decode(access_token, SECRET_KEY, "HS256")
        
    
        return({"error" : None})
    except:
        if ExpiredSignatureError:
            return({"error" : "Token expired"})
        elif InvalidTokenError:
            return ({"error" : "Token is invalid"})
        
   
        


def home(request):
    return render(request, "Main/index.html")


def fetch_posts(request):
    posts = []
    all_posts = Post.objects.all()
    for post in all_posts:
        posts.append({"post_id": post.post_id, "content": post.post_content, "likes": len(post.likes.all())})
    return JsonResponse(posts)


@csrf_exempt
def add_post(request):
    if(request.method == "POST"):
        error = verify_token(request.headers.get("Authorization"))
        if error["error"]:
            return JsonResponse(error)
        else:
            data = json.loads(request.body)
            postContent = data.get("postContent")
            
           
        
            
            return JsonResponse({"post_id" : "", "content" : ""})
            

            
            
            
            

