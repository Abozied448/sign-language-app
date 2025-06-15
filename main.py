
# from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# import shutil
# import os
# import json
# import numpy as np

# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image

# import models
# from database import SessionLocal, engine, Base
# from schemas import UserCreate, UserOut, Token
# from pydantic import BaseModel

# app = FastAPI()

# # إعداد CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # مسار الملفات الثابتة
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # مسار رئيسي
# @app.get("/")
# def root():
#     return RedirectResponse(url="/static/index.html")

# # إنشاء الجداول
# Base.metadata.create_all(bind=engine)

# # تحميل النموذج وقائمة الأصناف
# model = load_model("sign_language_model.h5")
# with open('class_names.json', 'r', encoding='utf-8') as f:
#     class_names = json.load(f)

# UPLOAD_DIRECTORY = "uploads"
# os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# # إعداد التشفير و JWT
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY = "your_secret_key_here"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # الدوال المساعدة
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def authenticate_user(db: Session, email: str, password: str):
#     user = get_user(db, email)
#     if not user or not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials. You must login first.",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, email=email)
#     if user is None:
#         raise credentials_exception
#     return user

# # تسجيل مستخدم جديد
# @app.post("/register", response_model=UserOut)
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = get_user(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     hashed_password = get_password_hash(user.password)
#     new_user = models.User(email=user.email, hashed_password=hashed_password, is_admin=False)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# # تسجيل الدخول وإعطاء توكن
# @app.post("/token", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Incorrect email or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/users/me", response_model=UserOut)
# def read_users_me(current_user: models.User = Depends(get_current_user)):
#     return current_user

# # الصفحات المحمية
# @app.get("/camera")
# def camera_page(current_user: models.User = Depends(get_current_user)):
#     return FileResponse("static/open_camera.html")

# @app.get("/learn_letters")
# def learn_letters(current_user: models.User = Depends(get_current_user)):
#     return FileResponse("static/learn_letters.html")

# @app.get("/videos")
# def learn_videos(current_user: models.User = Depends(get_current_user)):
#     return FileResponse("static/videos.html")

# @app.get("/stages")
# def stages_page(current_user: models.User = Depends(get_current_user)):
#     return FileResponse("static/stages.html")

# # رفع الفيديوهات
# VIDEO_DIR = "static/videos"
# @app.get("/api/videos")
# def get_videos(current_user: models.User = Depends(get_current_user)):
#     files = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith((".mp4", ".webm", ".ogg"))]
#     return JSONResponse(content={"videos": files})

# # التنبؤ بالصورة
# @app.post("/predict")
# async def predict_image(file: UploadFile = File(...)):
#     try:
#         file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         img = image.load_img(file_location, target_size=(64, 64))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)

#         prediction = model.predict(img_array)
#         predicted_class = class_names[np.argmax(prediction)]

#         os.remove(file_location)

#         return {"prediction": predicted_class}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"حدث خطأ في التنبؤ: {str(e)}")

# # عرض الدروس والمرحلة الحالية
# @app.get("/api/lessons")
# def get_lessons(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
#     lessons = db.query(models.Lesson).order_by(models.Lesson.order_index).all()
#     progresses = db.query(models.UserProgress).filter(models.UserProgress.user_email == current_user.email).all()

#     progress_dict = {p.lesson_slug: p.completed for p in progresses}

#     result = []
#     allow_next = True
#     for lesson in lessons:
#         completed = progress_dict.get(lesson.slug, False)
#         is_unlocked = allow_next
#         if not completed:
#             allow_next = False

#         result.append({
#             "title": lesson.title,
#             "slug": lesson.slug,
#             "order": lesson.order_index,
#             "completed": completed,
#             "unlocked": is_unlocked,
#         })

#     return result

# # إضافة الدروس الأساسية
# @app.post("/api/add_initial_lessons")
# def add_initial_lessons(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
#     if not current_user.is_admin:
#         raise HTTPException(status_code=403, detail="Only admin can add initial lessons.")

#     lessons = [
#         models.Lesson(title='Food', slug='food', order_index=1),
#         models.Lesson(title='Animals', slug='animals', order_index=2),
#         models.Lesson(title='Time', slug='time', order_index=3),
#     ]

#     for lesson in lessons:
#         exists = db.query(models.Lesson).filter(models.Lesson.slug == lesson.slug).first()
#         if not exists:
#             db.add(lesson)

#     db.commit()
#     return {"message": "Initial lessons added successfully."}

# # استلام نتيجة الاختبار وتحديث التقدم
# class QuizResult(BaseModel):
#     lesson_slug: str
#     score: int

# @app.post("/api/submit_quiz")
# def submit_quiz(result: QuizResult, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
#     lesson = db.query(models.Lesson).filter(models.Lesson.slug == result.lesson_slug).first()
#     if not lesson:
#         raise HTTPException(status_code=404, detail="Lesson not found")

#     total_questions = 2  # عدد الأسئلة الحالي
#     passed = (result.score >= int(0.9 * total_questions))

#     progress = db.query(models.UserProgress).filter(
#         models.UserProgress.user_email == current_user.email,
#         models.UserProgress.lesson_slug == lesson.slug
#     ).first()

#     if not progress:
#         progress = models.UserProgress(user_email=current_user.email, lesson_slug=lesson.slug)

#     progress.completed = passed
#     progress.passed_quiz = passed

#     db.add(progress)
#     db.commit()

#     return {"passed": passed}
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import shutil
import os
import json
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import models
from database import SessionLocal, engine, Base
from schemas import UserCreate, UserOut, Token
from pydantic import BaseModel

app = FastAPI()

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مسار الملفات الثابتة
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

Base.metadata.create_all(bind=engine)

model = load_model("sign_language_model.h5")
with open('class_names.json', 'r', encoding='utf-8') as f:
    class_names = json.load(f)

UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. You must login first.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password, is_admin=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/camera")
def camera_page(current_user: models.User = Depends(get_current_user)):
    return FileResponse("static/open_camera.html")

@app.get("/learn_letters")
def learn_letters(current_user: models.User = Depends(get_current_user)):
    return FileResponse("static/learn_letters.html")

@app.get("/videos")
def learn_videos(current_user: models.User = Depends(get_current_user)):
    return FileResponse("static/videos.html")

@app.get("/stages")
def stages_page(current_user: models.User = Depends(get_current_user)):
    return FileResponse("static/stages.html")

VIDEO_DIR = "static/videos"
@app.get("/api/videos")
def get_videos(current_user: models.User = Depends(get_current_user)):
    files = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith((".mp4", ".webm", ".ogg"))]
    return JSONResponse(content={"videos": files})

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        img = image.load_img(file_location, target_size=(64, 64))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        predicted_class = class_names[np.argmax(prediction)]

        os.remove(file_location)

        return {"prediction": predicted_class}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ في التنبؤ: {str(e)}")

@app.get("/api/lessons")
def get_lessons(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    lessons = db.query(models.Lesson).order_by(models.Lesson.order_index).all()
    progresses = db.query(models.UserProgress).filter(models.UserProgress.user_email == current_user.email).all()

    progress_dict = {p.lesson_slug: p.completed for p in progresses}

    result = []
    allow_next = True
    for lesson in lessons:
        completed = progress_dict.get(lesson.slug, False)
        is_unlocked = allow_next
        if not completed:
            allow_next = False

        result.append({
            "title": lesson.title,
            "slug": lesson.slug,
            "order": lesson.order_index,
            "completed": completed,
            "unlocked": is_unlocked,
        })

    return result

@app.post("/api/add_initial_lessons")
def add_initial_lessons(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can add initial lessons.")

    lessons = [
        models.Lesson(title='Food', slug='food', order_index=1),
        models.Lesson(title='Animals', slug='animals', order_index=2),
        models.Lesson(title='Time', slug='time', order_index=3),
    ]

    for lesson in lessons:
        exists = db.query(models.Lesson).filter(models.Lesson.slug == lesson.slug).first()
        if not exists:
            db.add(lesson)

    db.commit()
    return {"message": "Initial lessons added successfully."}

class QuizResult(BaseModel):
    lesson_slug: str
    score: int

@app.post("/api/submit_quiz")
def submit_quiz(result: QuizResult, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    lesson = db.query(models.Lesson).filter(models.Lesson.slug == result.lesson_slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    total_questions = 10
    passed = (result.score >= int(0.9 * total_questions))

    progress = db.query(models.UserProgress).filter(
        models.UserProgress.user_email == current_user.email,
        models.UserProgress.lesson_slug == lesson.slug
    ).first()

    if not progress:
        progress = models.UserProgress(user_email=current_user.email, lesson_slug=lesson.slug)

    progress.completed = passed
    progress.passed_quiz = passed

    db.add(progress)
    db.commit()

    return {"passed": passed}

# الـ API الجديد للتحكم في المراحل
@app.get("/api/progress")
def get_user_progress(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    progresses = db.query(models.UserProgress).filter(models.UserProgress.user_email == current_user.email).all()
    progress_dict = {p.lesson_slug: (100 if p.completed else 0) for p in progresses}
    return progress_dict
