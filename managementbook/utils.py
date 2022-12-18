from flask_login import current_user
from sqlalchemy import func

from managementbook import db, app
from managementbook.models import User, UserRole, Category, Book, Receipt, ReceiptDetails, Comment
import hashlib


def add_user(name, username, phone, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                phone=phone.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Book.id, Book.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
        .join(ReceiptDetails, ReceiptDetails.book_id.__eq__(Book.id)) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if kw:
        query = query.filter(Book.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Book.id).order_by(-Book.id).all()


def count_product_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Book.id)) \
        .join(Book, Book.category_id.__eq__(Category.id), isouter=True) \
        .group_by(Category.id).all()


def check_user_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_categories():
    query = Category.query

    return query.all()


def load_books(category_id=None, keyword=None):
    query = Book.query

    if category_id:
        query = query.filter(Book.category_id.__eq__(category_id))

    elif keyword:
        query = query.filter(Book.name.contains(keyword))
    return query.order_by(Book.created_date.desc()).all()


def get_product_by_id(product_id):
    return Book.query.get(product_id)


# def get_product_by_category(category_id):
#     return Book.query.filter_by(category_id=category_id).all()


def cart_stats(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }


def save_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, book_id=c['id'])
            db.session.add(d)

        db.session.commit()


def load_comments(book_id):
    return Comment.query.filter(Comment.book_id.__eq__(book_id)).order_by(-Comment.id).all()


def save_comment(content, book_id):
    cmt = Comment(content=content, book_id=book_id, user=current_user)
    db.session.add(cmt)
    db.session.commit()
    return cmt
