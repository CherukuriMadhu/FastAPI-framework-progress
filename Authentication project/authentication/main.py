from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from database import engine, Base, get_db
from models import User

from pwdlib import PasswordHash


# -------------------------
# APP CONFIGURATION
# -------------------------

app = FastAPI()

templates = Jinja2Templates(directory="templates")

password_hash = PasswordHash.recommended()


# Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="change-this-to-a-random-secret-key"
)


# Create tables
Base.metadata.create_all(bind=engine)


# -------------------------
# LOGIN PAGE
# -------------------------

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# -------------------------
# REGISTER PAGE
# -------------------------

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


# -------------------------
# REGISTER USER
# -------------------------

@app.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Check email
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return {
            "message": "Email already registered"
        }

    # Hash password
    hashed_password = password_hash.hash(password)

    # Create user
    user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    # Save user
    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(
        url="/",
        status_code=303
    )


# -------------------------
# LOGIN
# -------------------------

@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Find user
    user = db.query(User).filter(
        User.email == email
    ).first()

    # User doesn't exist
    if not user:
        return {
            "message": "Invalid email or password"
        }

    # Verify password
    if not password_hash.verify(
        password,
        user.password
    ):
        return {
            "message": "Invalid email or password"
        }

    # Store user ID in session
    request.session["user_id"] = user.id

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# -------------------------
# DASHBOARD
# -------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    # Get user ID from session
    user_id = request.session.get("user_id")

    # User is not logged in
    if not user_id:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    # Get user from database
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    # User doesn't exist
    if not user:
        request.session.clear()

        return RedirectResponse(
            url="/",
            status_code=303
        )

    # Send user information to HTML
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user
        }
    )


# -------------------------
# LOGOUT
# -------------------------

@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )