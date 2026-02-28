from django.shortcuts import render, redirect
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError




def login_template(request):
    return render(request, "Frontend/index.html")

def register_template(request):
    return render(request, "Frontend/index.html")

def home_template(request):
    
    
    
        
    return render(request, "Frontend/index.html")


def search_template(request):
    return render(request, "Frontend/index.html")



def profile_template(request):
    return render(request, "Frontend/index.html")


def followers(request):
    return render(request, "Frontend/index.html")