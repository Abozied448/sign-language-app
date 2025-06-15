from database import SessionLocal
from models import Lesson

def add_initial_lessons():
    lessons = [
        Lesson(title='Size Clothes', slug='size-clothes', order_index=1),
        Lesson(title='Family', slug='family', order_index=2),
        Lesson(title='Places', slug='places', order_index=3),
    ]

    db = SessionLocal()

    for lesson in lessons:
        exists = db.query(Lesson).filter(Lesson.slug == lesson.slug).first()
        if not exists:
            db.add(lesson)

    db.commit()
    db.close()
    print("Initial lessons added successfully.")

if __name__ == "__main__":
    add_initial_lessons()
