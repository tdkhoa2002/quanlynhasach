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

    name = Column(String(100), nullable=False)
    price = Column(Float, default=0)
    description = Column(String(255))
    image = Column(String(200))
    author = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='book', lazy=True)
    comments = relationship('Comment', backref='book', lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    phone = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.user)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=True)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=True)


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
                     category_id=1)
        p4 = Book(name='Gấu anh gấu em - tập 7', description='mô tả 4', price=27000, author="Thái Bá Tân",
                     image='https://res.cloudinary.com/de3yhowd4/image/upload/v1669606884/gauanhgauem-tap7_gqbtib.webp',
                     category_id=1)
        p5 = Book(name='Trẻ con có phải siêu nhân đâu', description='mô tả 4', price=27000, author="Thái Bá Tân",
                     image='https://res.cloudinary.com/de3yhowd4/image/upload/v1669607005/sachvanhocvietnam_adsrpn.webp',
                     category_id=2)
        p6 = Book(name='Dế mèn phiêu lưu ký', description='mô tả 4', price=27000, author="Thái Bá Tân",
                  image='https://res.cloudinary.com/de3yhowd4/image/upload/v1671198205/de-men-phieu-luu-ky-_13x19_bia_tb2019-1_306f580015064449ae2aa6db2f05a6b7_large_svngxv.jpg',
                  category_id=2)
        p7 = Book(name='Phòng thiết kế', description='mô tả 4', price=27000, author="Thái Bá Tân",
                  image='https://res.cloudinary.com/de3yhowd4/image/upload/v1671198196/1_8b2c4187760845c2a79b31ddb44def57_large_kenusq.jpg',
                  category_id=2)
        p8 = Book(name='Những bài diễn văn làm thay đổi thế giới', description='mô tả 4', price=27000, author="Thái Bá Tân",
                  image='https://res.cloudinary.com/de3yhowd4/image/upload/v1671198139/nhung-bai-dien-van-lam-thay-doi-the-gioi_bia-1_7ae332181a444ac5911d06c7f066f410_large_rttrzz.jpg',
                  category_id=2)
        p9 = Book(name='Siêu thông minh', description='mô tả 4', price=27000, author="Thái Bá Tân",
                  image='https://res.cloudinary.com/de3yhowd4/image/upload/v1671198196/sieu-thong-minh-tu-duy_xa-hoi-hoc_52be9ef2039c4dddb53f94b23d7e269e_large_g1tode.webp',
                  category_id=3)
        p10 = Book(name='Một nửa của thế giới', description='mô tả 4', price=27000, author="Thái Bá Tân",
                  image='https://res.cloudinary.com/de3yhowd4/image/upload/v1671198139/mot-nua-cua-the-gioi_355acaa917f944aaa915d6d52f82bea7_large_heta52.webp',
                  category_id=3)
        p11 = Book(name='Sự hình thành của thế giới', description='mô tả 4', price=27000, author="Thái Bá Tân",
                  image='https://res.cloudinary.com/de3yhowd4/image/upload/v1671198093/su-sinh-thanh-the-gioi_622ef45f13a2438899e450bb4228d48f_master_nzipng.webp',
                  category_id=3)
        p12 = Book(name='Đất nước gấm hoa', description='mô tả 4', price=27000, author="Thái Bá Tân",
                  image='https://res.cloudinary.com/de3yhowd4/image/upload/v1671198139/dat-nuoc-gam-hoa---bia_0ffe3dbcbff248f49887a556b86b5502_large_lmmvdj.webp',
                  category_id=3)

        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12])

        password = str(hashlib.md5('123123'.encode('utf-8')).hexdigest())
        u = User(name="Admin",
                 username="admin",
                 phone="0123456789",
                 password=password,
                 email="admin123@gmail.com",
                 user_role=UserRole.admin,
                 avatar="https://res.cloudinary.com/de3yhowd4/image/upload/v1669481858/dxyigbm1fnl2dmokkeh2.jpg")
        db.session.add(u)
        cmt1 = Comment(content='Sach nay hay qua', user_id=1, book_id=1)
        cmt2 = Comment(content='Xung dang de mua', user_id=1, book_id=1)

        db.session.add_all([cmt1, cmt2])
        db.session.commit()


