from managementbook import db, app
from managementbook.models import User, UserRole, Category, Book
import hashlib


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_user_login(username, password, role=UserRole.user):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_cates():
    return Category.query.all()


def load_books():
    return Book.query.all()


def load_books_index():
    return Book.query.order_by(Book.created_date.desc()).all()


def get_product_by_id(product_id):
    return Book.query.get(product_id)


def get_product_by_category(category_id):
    return Book.query.filter_by(category_id=category_id).all()


def get_category_by_id(category_id):
    return Category.query.get(category_id)


def find_book_by_kw(keyword=None):
    return Book.query.filter(Book.name.contains(keyword))
