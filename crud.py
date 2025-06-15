from sqlalchemy.orm import Session
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

from flask import Blueprint, request, jsonify
from models.lesson import Lesson, UserProgress
from database import SessionLocal

lessons_bp = Blueprint('lessons', __name__)
db = SessionLocal()

@lessons_bp.route('/api/lessons', methods=['GET'])
def get_lessons():
    user_email = request.args.get('email')
    lessons = db.query(Lesson).order_by(Lesson.order_index).all()
    progress = db.query(UserProgress).filter_by(user_email=user_email).all()
    progress_map = {p.lesson_slug: p for p in progress}

    result = []
    for lesson in lessons:
        p = progress_map.get(lesson.slug)
        result.append({
            "title": lesson.title,
            "slug": lesson.slug,
            "order": lesson.order_index,
            "completed": p.completed if p else False,
            "passed_quiz": p.passed_quiz if p else False
        })

    return jsonify(result)

@lessons_bp.route('/api/complete_lesson', methods=['POST'])
def complete_lesson():
    data = request.json
    user_email = data['email']
    lesson_slug = data['slug']

    progress = db.query(UserProgress).filter_by(user_email=user_email, lesson_slug=lesson_slug).first()
    if not progress:
        progress = UserProgress(user_email=user_email, lesson_slug=lesson_slug)

    progress.completed = True
    db.add(progress)
    db.commit()
    return jsonify({"message": "Lesson marked as complete"})
