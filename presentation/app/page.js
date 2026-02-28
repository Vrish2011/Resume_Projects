"use client";

import { useState, useRef, useEffect } from "react";

function Layout({ setPage, page }) {
  function handle_logout() {
    setPage("register");
  }

  if (page == "home" || page?.startsWith("slide")) {
    
    return (
      <nav id="layout">
        <ul>
          <li>
            <button id="logout" onClick={handle_logout}>
              Logout
            </button>
          </li>
          <li></li>
          <li>
            <button onClick={() => setPage("home")}>Home</button>
          </li>
        </ul>
      </nav>)
  
  }

  return (
    <nav id="layout">
      <ul>
        <li>
          <button onClick={() => setPage("login")}>Login</button>
        </li>
        <li></li>
        <li>
          <button onClick={() => setPage("register")}>Register</button>
        </li>
      </ul>
    </nav>
  );
}

function Register({ setPage, page }) {
  const passwordRef = useRef(null);
  const usernameRef = useRef(null);
  

  function handle_register() {
    if (usernameRef.current.value && passwordRef.current.value) {
      fetch("/api/register", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
          username: usernameRef.current.value,
          password: passwordRef.current.value
        })
      })
        .then(response => response.json())
        .then(function (data) {
          if (data.success) {
            setPage("home");
            localStorage.setItem("user_id", data.user_id);
          }
        });
    }
  }

  return (
    <div>
      <Layout setPage={setPage} page={page} />
      <div>
        <input
          id="username"
          placeholder="username"
          className="form-control"
          ref={usernameRef}
        />
        <input
          id="password"
          placeholder="password"
          className="form-control"
          ref={passwordRef}
        />
      </div>
      <button
        id="register"
        onClick={handle_register}
        className="btn btn-primary"
      >
        Register
      </button>
    </div>
  );
}

function Login({ setPage, page }) {
 
  const passwordRef = useRef(null);
  const usernameRef = useRef(null);

  function handle_login() {
    if (usernameRef.current.value && passwordRef.current.value) {
      fetch("/api/login", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
          username: usernameRef.current.value,
          password: passwordRef.current.value
        })
      })
        .then(response => response.json())
        .then(function (data) {
          if (data.success) {
            setPage("home");
            localStorage.setItem("user_id", data.user_id);
          }
        });
    }
  }

  return (
    <div>
      <Layout setPage={setPage} page={page} />
      <div>
        <input
          id="username"
          placeholder="username"
          className="form-control"
          ref={usernameRef}
        />
        <input
          id="password"
          placeholder="password"
          className="form-control"
          ref={passwordRef}
        />
      </div>
      <button
        id="register"
        onClick={handle_login}
        className="btn btn-primary"
      >
        Login
      </button>
    </div>
  );
}

function Contacts({ setPage, page, contacts, setContacts }) {
  const createRef = useRef(0);

  useEffect(function () {
    fetch("/api/docs", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ user_id: localStorage.getItem("user_id") })
    })
      .then(response => response.json())
      .then(function (data) {
        setContacts(data);
      });
  }, []);

  function handle_add() {
    fetch("/api/docs", {
      method: "PUT",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ user_id: localStorage.getItem("user_id") })
    })
      .then(response => response.json())
      .then(function (data) {
        let update_tasks = [...contacts];
        update_tasks.push({
          title: createRef.current.value,
          doc_id: data.doc_id,
          user_id: localStorage.getItem("user_id")
        });
        setContacts(update_tasks);
      });
  }

  return (
    <div>
      <Layout setPage={setPage} page={page} />
      <div id="create">
        <img src="https://static.vecteezy.com/system/resources/previews/021/498/877/original/add-new-document-file-upload-button-concept-illustration-flat-design-eps10-simple-and-modern-graphic-element-for-landing-page-empty-state-ui-infographic-button-icon-vector.jpg" />
        <button id="add" onClick={() => setPage("overlay_input")}></button>
      </div>
      <div className="docs">
        {contacts.map((task, index) => (
          <div className="doc" key={index}>
            <button
              onClick={() => setPage(`slide|${task.doc_id}`)}
              className="doc_button"
            ></button>
            <h1>{task.title}</h1>
          </div>
        ))}
      </div>
    </div>
  );
}

function Slides({ setPage, page, doc_id }) {
  let [slides, setSlides] = useState([]);
  let [slideIndex, setIndex] = useState(0);
  let [slideContent, setContent] = useState([{}]);
  let [elements, setElements] = useState([{}]);
  

  useEffect(function () {
    fetch("/api/slides", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ doc_id: doc_id })
    })
      .then(response => response.json())
      .then(function (data) {
      
        setSlides(data);
        setIndex(data[0].slide_id);
        if (data[0]) {
          setContent(data[0]);
        }
      });
  }, []);

  useEffect(function () {
   
    const currentslide = document.querySelector(".currentslide");
   
    let elements = document.querySelectorAll("#nice")

    for(let i = 0; i < elements.length; i++){
      elements[i].remove()
    }



    if(!currentslide || !slideContent.elements){
      
      return;

    }


    for (let e = 0; e < slideContent.elements.length; e++) {
      const element = document.createElement("div");
      element.style.width = "200px"
      element.style.height = "50px"
      element.contentEditable = true
     
      let isDragging = false
      let offSetX = 0
      let offSetY = 0
      element.addEventListener("mousedown", function(event){
        element.style.position = "absolute"
        isDragging = true
        offSetX = event.clientX - element.offsetLeft
        offSetY = event.clientY - element.offsetTop
        element.style.cursor = "grabbing"
      })
      document.addEventListener("mousemove", function(event){
        if(!isDragging){
          return;
        }

        element.style.top = event.clientY - offSetY + "px";
        element.style.left = event.clientX - offSetX + "px";
        fetch("/api/position", {method: "POST", headers : {"Content-type" : "application/json"}, body : JSON.stringify({element_id : slideContent.elements[e].element_id, top : element.style.top, left : element.style.left})})


      })
      document.addEventListener("mouseup", function(event){
        isDragging = false
        element.style.cursor = "grab";
      })

      element.oninput = function(event){
        fetch("/api/textContent", {method : "POST", headers : {"Content-type" : "application/json"}, body : JSON.stringify({element_id : slideContent.elements[e].element_id, textContent: element.textContent})})

      }

      element.id = "nice"
      element.style.border = "solid 2px black"

      if (slideContent.elements[e].top != "no") {
        element.style.position = "absolute"
        element.style.top = slideContent.elements[e].top;
      }

      if (slideContent.elements[e].left != "no") {
        element.style.position = "absolute"
        element.style.left = slideContent.elements[e].left;
      }

      if (slideContent.elements[e].textContent) {
        element.textContent = slideContent.elements[e].textContent;
      }

      if (slideContent.elements[e].type == "header") {
        element.style.fontSize = "40px";
        element.style.fontWeight = "500";
      }
      

      currentslide.appendChild(element);
    }
  }, [slideContent]);

  function addSlide() {
    fetch("/api/slides", {
      method: "PUT",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ doc_id: doc_id })
    })
      .then(response => response.json())
      .then(function (data) {
        let update_slides = [...slides];
        let json_ = {
          slide_id: data.lastID,
          doc_id: parseInt(doc_id[0], 10),
          content: ""
        };
        update_slides.push(json_);
        setSlides(update_slides);
      });
  }

  return (
    <div>
      <div className="slides">
        {slides.length != 0
          ? slides.map((slide, index) => (
              <div className="slide" key={index}>
                {slide.content}
                <button
                  className="addslidebutton"
                  onClick={() => {
                    setIndex(slide.slide_id);
                    setContent(slide);
                  }}
                ></button>
              </div>
            ))
          : null}
      </div>

      {slideContent.content !== null ? (
        <div className="currentslide">{slideContent.content}</div>
      ) : null}

      <button
        id="add_element"
        className="btn btn-primary"
        onClick={() =>
          setPage(`overlay|${slideContent.slide_id}|${slideContent.doc_id}`)
        }
      >
        Add an element
      </button>

      <div className="addslide">
        <button className="addslidebutton" onClick={addSlide}></button>
        Add button
      </div>
    </div>
  );
}

function Overlay_slide({ setPage, page, doc_id, slide_id }) {
  const typeRef = useRef(null);

  function add_element() {
    if (typeRef.current.value) {
      fetch("/api/elements", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
          slide_id: slide_id,
          type: typeRef.current.value
        })
      })
        .then(response => response.json())
        .then(function (data) {
          
          setPage(`slide|${doc_id}`);
        });
    }
  }

  return (
    <div>
      <div className="overlay"></div>
      <Slides setPage={setPage} page={page} doc_id={doc_id} />
      <div id="input_div">
        <select name="type" className="form-select" ref={typeRef}>
          <option className="form-option" disabled>
            Type
          </option>
          <option className="form-option" value="header">
            Header
          </option>
          <option className="form-option" value="textbox">
            Text Box
          </option>
          <option className="form-option" value="l">
            {doc_id}, {slide_id}
          </option>
        </select>
        <button
          id="add_document"
          className="btn btn-primary"
          onClick={add_element}
            
            
          
        >
          Add an Element
        </button>
      </div>
    </div>
  );
}

function Overlay_input({setPage, page}){
  const addRef = useRef(null)
  function add_Doc(){
    if(addRef.current.value){
      fetch("/api/docs", {method : "PUT", headers: {"Content-type": "application/json"}, body : JSON.stringify({title: addRef.current.value, user_id: localStorage.getItem("user_id")})})
      .then(res => res.json())
      .then(function(data){
      
        setPage("home")
      })

    }

  }
  return (
    <div>
      <div className="overlay">

      </div>

      <div id="input_div">
        <div>
          <input placeholder="Add a presentation" ref={addRef}/>
          <button onClick={add_Doc}>Add</button>

        </div>
      </div>
    </div>
  )
}

export default function Home() {
  let [page, setPage] = useState("register");
  let [contacts, setContacts] = useState([{}]);
 


  useEffect(function () {
    if (localStorage.getItem("user_id")) {
      setPage("home");
    }
  }, []);

  


  if (page.startsWith("slide")) {
    let doc_id = page.split("|").splice(1, 1);
    return (
      <div>
        <Layout page={page} setPage={setPage} />
        <Slides page={page} doc_id={doc_id} setPage={setPage} />
      </div>
    );
  }

  if (page == "register") {
    return <Register setPage={setPage} page={page} />;
  }

  if (page == "login") {
    return <Login setPage={setPage} />;
  }

  if (page == "home") {
    return (
      <Contacts
        setPage={setPage}
        page={page}
        contacts={contacts}
        setContacts={setContacts}
      />
    );
  }

  if (page == "overlay_input") {
    return (
      <div><Overlay_input
        setPage={setPage}
        page={page}
        
      />
      <Contacts page={page} setPage={setPage} contacts={contacts} setContacts={setContacts}/>
      </div>
    );
  }

  if (page.startsWith("overlay")) {
    let slide_id = page.split("|");
    slide_id = parseInt(slide_id[1], 10);
    let doc_id = page.split("|").splice(2, 2);

    return (
      <Overlay_slide
        slide_id={slide_id}
        doc_id={doc_id}
        setPage={setPage}
        page={page}
      />
    );
  }
}
