from django.shortcuts import render
import json
from .models import Post, Like, Follow
from django.http import JsonResponse
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
from django.views.decorators.csrf import csrf_exempt

SECRET_KEY = "NP-0iij-0j0j--j--hhohp"
def verify_token(access_token):
    
    try:
        data = jwt.decode(access_token, SECRET_KEY, "HS256")
        
    
        return({"error" : None})
    except ExpiredSignatureError:
        
        return({"error" : "Token expired"})
    except InvalidTokenError:
        return ({"error" : "Token is invalid"})
            

def get_all_posts(request):
    posts_json = []
   
    verify = verify_token(request.headers.get("Authorization"))
    is_log = True
    if(verify["error"]):
        print(verify["error"])
        is_log = False
    
    posts = Post.objects.order_by('?')[:5]
    for post in posts:
        like_len = len(Like.objects.filter(post_id=post.post_id))
        is_like = False
        if len(Like.objects.filter(user_id = request.session.get("user_id"), post_id=post.post_id)) !=0:
            is_like = True
        posts_json.append({"is_like" : is_like, "is_log" : is_log, "created_at" : post.created_at, "is_change" : post.username == request.session.get("username"), "post_id" : post.post_id, "likes": like_len, "postContent": post.postContent, "creator" : post.username })
    return JsonResponse(posts_json, safe=False)

@csrf_exempt
def search_query(request):
    posts_json = []
    
    query_ = json.loads(request.body)
    q = query_.get("query")
    posts = Post.objects.all()
   
    
    for post in posts:
        if q in post.username:
            
            like_len = len(Like.objects.filter(post_id=post.post_id))
            is_like = False
            if len(Like.objects.filter(user_id = request.session.get("user_id"), post_id=post.post_id)) > 0:
                is_like = True
       
            
            posts_json.append({"created_at" : post.created_at, "is_change" : post.creator_id == request.session.get("user_id"), "post_id" : post.post_id, "likes": like_len, "postContent": post.postContent, "creator" : post.username })
        
    return JsonResponse(posts_json, safe=False)



@csrf_exempt
def add_post(request):
    data = verify_token(request.headers.get("Authorization"))
    if data["error"]:
        return JsonResponse({"error" : data["error"]}, safe=False)
    if request.method == "POST":
        postForm = json.loads(request.body)
        postContent = postForm.get("postContent")
        print(postContent)
        new_post = Post(postContent=postContent, username=request.session.get("username"), creator_id=request.session.get("user_id"))
        new_post.save()
        return JsonResponse({"post_id" : new_post.post_id}, safe=False)
        

@csrf_exempt
def get_user_posts(request):
    if request.method == "POST":
        user_posts = []
        userForm = json.loads(request.body)
        username = userForm.get("username")
        posts = Post.objects.filter(username=username)
        for post in posts:
            like_len = len(Like.objects.filter(post_id=post.post_id))
            is_like = False
            if len(Like.objects.filter(user_id = request.session.get("user_id"), post_id=post.post_id)) !=0:
                is_like = True
            is_follow = False
            if len(Follow.objects.filter(username=username, follower=request.session.get("username"))) > 0:
                is_follow = True
                

            user_posts.append({"is_follow" : is_follow, "followers" : len(Follow.objects.filter(username=username)), "post_id" : post.post_id, "is_like" :is_like,  "likes" : like_len, "postContent" : post.postContent, "created_at" : post.created_at, "is_change": post.username == request.session.get("username")})
        return JsonResponse(user_posts, safe=False)


@csrf_exempt
def edit_post(request):
    if(request.method == "POST"):
        access_token = request.headers.get("Authorization")
        verify = verify_token(access_token)
        if(verify["error"]):
            return JsonResponse(verify)
        else:
            editForm = json.loads(request.body)
            post_id = int(editForm.get("post_id"))
            postContent = editForm.get("postContent")
            post = Post.objects.get(post_id=post_id)
            post.postContent = postContent
            post.save()
            return JsonResponse({"postContent" : postContent})


@csrf_exempt
def follow_unfollow(request):
        if request.method == "POST":
            followForm = json.loads(request.body)
            is_follow = followForm.get("is_follow")
            
            username = followForm.get("username")
            verify = verify_token(request.headers.get("Authorization"))
            if verify["error"]:
                return JsonResponse(verify, safe=False)
            print(is_follow)
            if(is_follow == "false"):
                follow = Follow.objects.create(username=username, follower=request.session.get("username"))
                return JsonResponse({"is_follow" : "true", "followers" : len(Follow.objects.filter(username=username))})
            else:
                follow = Follow.objects.filter(username=username, follower=request.session.get("username"))
                print(len(Follow.objects.filter(username=request.session.get("username"), follower=username)))
                follow.delete()
                return JsonResponse({"is_follow" :"false", "followers" : len(Follow.objects.filter(username=username))})
            
        
        
def get_followers(request):
    followers = []
    verify = verify_token(request.headers.get("Authorization"))
    if(verify["error"]):
        return JsonResponse(verify)
    follo_ = Follow.objects.filter(follower=request.session.get("username"))
    for follow in follo_ :
        followers.append({"creator": follow.username})

    

    return JsonResponse(followers, safe=False)
        
        
        
            
            
        

@csrf_exempt
def delete_post(request):
    if(request.method == "POST"):
        access_token = request.headers.get("Authorization")
        verify = verify_token(access_token)
        if(verify["error"]):
            return JsonResponse(verify)
        else:
            deleteForm = json.loads(request.body)
            post_id = int(deleteForm.get("post_id"))
            post = Post.objects.get(post_id=post_id)
            post.delete()
            post.save()
            likes = Like.objects.filter(post_id=post_id)
            for like in likes:
                like.delete()
                like.save()
            return JsonResponse({"post_id" : post_id})
            

@csrf_exempt
def like_unlike(request):
    if request.method == "POST":
        likeForm = json.loads(request.body)
        is_like = likeForm.get("is_like")
        post_id = likeForm.get("post_id")
        verify = verify_token(request.headers.get("Authorization"))
        if verify["error"]:
            return JsonResponse(verify, safe=False)
        if(is_like):
            like = Like.objects.create(user_id=request.session.get("user_id"), post_id=post_id)
            return JsonResponse({"post_id" : post_id})
        else:
            like = Like.objects.get(post_id=post_id, user_id=request.session.get("user_id"))
            like.delete()
            
            return JsonResponse({"post_id": post_id})
        



    