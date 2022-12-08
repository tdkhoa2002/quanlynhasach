from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from managementbook import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin
import hashlib


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    admin = 1
    user = 2


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(30), nullable=False)
    books = relationship('Book', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(30), nullable=False)
    price = Column(Float, default=0)
    description = Column(String(255))
    image = Column(String(100))
    author = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.user)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():

        # db.create_all()

        c1 = Category(name="Lịch sử truyền thống")
        c2 = Category(name="Truyện tranh")
        c3 = Category(name="Văn học Việt Nam")

        db.session.add_all([c1, c2, c3])

        p1 = Book(name='Tranh truyện lịch sử Việt Nam', description='mô tả 1', price=13500, author="Thái Bá Tân",
                     image='https://res.cloudinary.com/de3yhowd4/image/upload/v1669606587/tranhtruyenlsvn_zlls4o.webp',
                     category_id=1)
        p2 = Book(name='Ước mơ đến trường', description='mô tả 2', price=27000, author="Thái Bá Tân",
                     image='https://res.cloudinary.com/de3yhowd4/image/upload/v1669606692/uocmodentruong_vpdnjv.webp',
                     category_id=1)
        p3 = Book(name='Gấu anh gấu em - tập 8', description='mô tả 3', price=27000, author="Thái Bá Tân",
                     image='https://res.cloudinary.com/de3yhowd4/image/upload/v1669606785/gauanh-gauem-tap8_gwtvgs.jpg',
                     category_id=2)
        p4 = Book(name='Gấu anh gấu em - tập 7', description='mô tả 4', price=27000, author="Thái Bá Tân",
                     image='https://res.cloudinary.com/de3yhowd4/image/upload/v1669606884/gauanhgauem-tap7_gqbtib.webp',
                     category_id=2)
        p5 = Book(name='Trẻ con có phải siêu nhân đâu', description='mô tả 4', price=27000, author="Thái Bá Tân",
                     image='https://res.cloudinary.com/de3yhowd4/image/upload/v1669607005/sachvanhocvietnam_adsrpn.webp',
                     category_id=3)

        db.session.add_all([p1, p2, p3, p4, p5])

        password = str(hashlib.md5('123123'.encode('utf-8')).hexdigest())
        u = User(name="Admin",
                 username="admin",
                 password=password,
                 email="admin123@gmail.com",
                 user_role=UserRole.admin,
                 avatar="https://res.cloudinary.com/de3yhowd4/image/upload/v1669481858/dxyigbm1fnl2dmokkeh2.jpg")
        db.session.add(u)
        db.session.commit()


