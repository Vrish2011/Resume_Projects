from fastapi import FastAPI, Depends, Request, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import uvicorn
import sqlite3
import json
import uvicorn
from datetime import timedelta, datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="SECRET_KEY"
)
templates = Jinja2Templates(directory="templates")
def get_db():
    connection = None
    cursor = None
    try:
        connection = sqlite3.connect("main.db", check_same_thread=False)
        connection.row_factory = sqlite3.Row 
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS docs(doc_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS editors(user_id INTEGER NOT NULL, doc_id INTEGER NOT NULL)")
        
        connection.commit()
        yield cursor
    
    finally:
        if(cursor):
            cursor.close()
        if(connection):
            connection.commit()
            connection.close()
        


def authenticate(username, password, db):
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if(user):
        correct = check_password_hash(user["password"], password)
        if(correct):
            token = create_access_token({"sub" : "Logging in", "exp": datetime.now(timezone.utc) + timedelta(minutes=30)})

            return ({"error" : None, "access_token" : token, "user_id" : user["id"]})
        elif(not correct):
            return ({"error": "The Password is incorrect"})
    elif(not user):
        return ({"error": "User does not exist"})


    
def create_access_token(data):
    return jwt.encode(data, "creating_token", "HS256")

def check_user(username, password, db):
    user = db.execute("SELECT * FROM users WHERE username = ? ", (username,)).fetchone()
    if(user):
        return True
    elif(not user):
        return False

def create_user(username, password, db):
    user = db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))
    access_token = create_access_token({"sub": "registering", "exp" : datetime.now(timezone.utc) + timedelta(minutes=30)})
    return ({"user_id" : user.lastrowid, "access_token" : access_token})

def Verify_token(request : Request):
    headers = request.headers.get("Authorization")
    
    if(not headers):
        raise HTTPException(status_code=401, detail="No headers")
        return ({"error": "No headers"})
    elif(not headers.startswith("Bearer ")):
        raise HTTPException(status_code=401, detail="Wrong formatted request")
        return ({"error": "Wrong formatted headers"})
    
    else:
        token = headers.split()[1]
       
        
        try:
            payload =jwt.decode(token, "creating_token", algorithms=["HS256"])
           
            
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
            
        
           
            return({"error":"Token expired"})
        
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
            return ({"error":"Token expired"})
        return ({"error": None})

    
   
        
    
    


@app.api_route("/register", methods=["GET", "POST"], response_class=JSONResponse)
async def register(request: Request, db=Depends(get_db)):
    if(request.method == "POST"):
        RegisterForm = await request.json()
        username = RegisterForm.get("username")
        password = RegisterForm.get("password")
        
        user_exists = check_user(username=username, password=password, db=db)
        
        if(user_exists):
            return ({"error" : "User already exists"})
        if(not user_exists):
            hashed_password = generate_password_hash(password)
            user = create_user(username=username, password=hashed_password, db=db)
            request.session["user_id"] = user["user_id"]
            
            

            return(user)

@app.api_route("/login", methods=["GET", "POST"], response_class=JSONResponse)
async def login(request: Request, db=Depends(get_db)):
    if(request.method == "POST"):
        LoginData = await request.json()
        username = LoginData.get("username")
        password = LoginData.get("password")
        user = authenticate(username, password, db)
        
        

        if(user["error"]):
            return ({"error": user["error"]})
        request.session["user_id"] = user["user_id"]
        
        return (user)




@app.api_route("/website/home", methods=["GET", "POST"], response_class=HTMLResponse)
def home(request : Request):
    if(not request.session.get("user_id")):
        return RedirectResponse("/website/login")
    with open("templates/index.html", "r") as file:
        lines = file.read()
        lines_list = lines.split("\n")
        count = 0
        for line in lines_list:
            if line.strip():
                count += 1
        print(count)

            
    
    
        
        return HTMLResponse(content=lines)
    


   
@app.api_route("/website/login", methods=["GET", "POST"], response_class=HTMLResponse)
def login_template(request : Request):
    request.session.clear()
    with open("templates/index.html", "r") as file:
        lines = file.read()
        
        return HTMLResponse(content=lines)


@app.api_route("/website/register", methods=["GET", "POST"], response_class=HTMLResponse)
def register_template(request : Request):
    request.session.clear()
    with open("templates/index.html", "r") as file:
        lines = file.read()
        
        return HTMLResponse(content=lines)


    
@app.api_route("/create", methods=["GET", "POST"], response_class=JSONResponse)
async def create(request : Request, db=Depends(get_db), verify=Depends(Verify_token)):
    if(verify.get("error")):
        if(verify.get("error") == "Token expired"):
            return RedirectResponse("/website/login")
        
        
    else:
        if(request.method == "POST"):
            data = await request.json()
            title = data.get("title")
            last_row = db.execute("INSERT INTO docs(title, content) VALUES(?,?)", (title, ""))
            doc_id = last_row.lastrowid
            db.execute("INSERT INTO editors (doc_id, user_id) VALUES(?, ?)", (doc_id, request.session.get("user_id")))
            return JSONResponse({"doc_id" : doc_id})
        
        


@app.api_route("/get_docs", methods=["GET", "POST"], response_class=JSONResponse)
def docs(request:Request, db=Depends(get_db), verify=Depends(Verify_token)):
    if(verify.get("error")):
        return ({"error" : verify.get("error")})
    docs_list = []
    docs = db.execute("SELECT * FROM docs").fetchall()
    
    editors = db.execute("SELECT * FROM editors WHERE user_id = ? ORDER BY doc_id DESC LIMIT 9", (request.session.get("user_id"),)).fetchall()
    for editor in editors:
        doc = db.execute("SELECT * FROM docs WHERE doc_id = ?", (editor["doc_id"],)).fetchone()
        docs_list.append({"doc_id" : doc["doc_id"], "content": doc["content"], "title": doc["title"]})
    return JSONResponse(docs_list)

    
        

@app.api_route("/website/search", methods=["GET", "POST"], response_class=JSONResponse)
def search(request: Request, db=Depends(get_db)):
    if(not request.session.get("user_id")):
        return RedirectResponse("/website/login")
    with open("templates/index.html", "r") as file:
        lines = file.read()
    
    
        
        return HTMLResponse(content=lines)      



@app.api_route("/website/get", methods=["GET", "POST"], response_class=JSONResponse)
def get_(request: Request, db=Depends(get_db), verify=Depends(Verify_token)):
    if(verify.get("error")):
        return ({"error" : verify.get("error")})
    query = request.query_params.get("q")
    docs_list = []
    
    
    editors = db.execute("SELECT * FROM editors WHERE user_id = ? ORDER BY doc_id DESC LIMIT 9", (request.session.get("user_id"),)).fetchall()
    for editor in editors:
        doc = db.execute("SELECT * FROM docs WHERE doc_id = ?", (editor["doc_id"],)).fetchone()
        if(query in doc["title"]):
            docs_list.append({"doc_id" : doc["doc_id"], "content": doc["content"], "title": doc["title"]})
        
    print(docs_list)
    return JSONResponse(docs_list)


@app.api_route("/doc/get", methods=["GET", "POST"], response_class=JSONResponse)
async def get(request: Request, db=Depends(get_db), verify=Depends(Verify_token)):
    if(request.method == "POST"):
        data = await request.json()
        doc_id = data.get("doc_id")
        doc = db.execute("SELECT * FROM docs WHERE doc_id = ?", (doc_id,)).fetchone()
        return JSONResponse({"doc_id" : doc["doc_id"], "title": doc["title"], "content": doc["content"]})


@app.api_route("/website", methods=["GET", "POST"], response_class=HTMLResponse)
def website(request : Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.api_route("/share", methods=["GET", "POST"], response_class=JSONResponse)
async def share(request : Request, db=Depends(get_db), verify=Depends(Verify_token)):
    if(request.method == "POST"):
        data = await request.json()
        doc_id = data.get("doc_id")
        username = data.get("username")
        try:
            raw_id = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            user_id = raw_id["id"]
            if(not user_id):
                return({"error" : "User Does not exist"})
            if(user_id == request.session.get("user_id")):
                return ({"error" : "You cannot send to your self"})
            try:
                editor = db.execute("SELECT * FROM editors WHERE doc_id = ? AND user_id = ?", (doc_id, user_id))
                if(editor):
                    return JSONResponse({"error" : "User is already an editor"})
                else:
                    pass
            except:
                return JSONResponse({"error" : "Nothing"})
            db.execute("INSERT INTO editors (doc_id, user_id) VALUES (?, ?)", (doc_id,  user_id))
            return JSONResponse({"error" : None})
        except:
            return JSONResponse({"error": "Exception"})
        
            

clients = []
@app.websocket("/ws")
async def websocket_handler(websocket : WebSocket):
    await websocket.accept()
    clients.append(websocket)
    conn = sqlite3.connect("main.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    while True:
        
        
        try:
            data = await websocket.receive_json()
            content= data.get("content")
            doc_id = data.get("doc_id")
            cursor.execute("UPDATE docs SET content = ? WHERE doc_id = ?", (content, doc_id))
            conn.commit()
            for client in clients:
                if client != websocket:
                    await client.send_json({"doc_id" : doc_id, "content" : content})
            
        except WebSocketDisconnect:
            clients.remove(websocket)
        
        
        
        
            
                



        

            

        
        
        




@app.api_route("/", methods=["GET", "POST"], response_class=RedirectResponse)
def Redirect_function(request : Request):
    return RedirectResponse("/website/home")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8005)