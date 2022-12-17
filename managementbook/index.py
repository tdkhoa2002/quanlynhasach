# import controllers
# import utils
# from managementbook import app, login
#
#
# @app.add_url_rule("/", "index", controllers.index)
# @app.add_url_rule("/books/<int:book_id>", "book-detail", controllers.details)
# @app.add_url_rule("/category/<int:category_id>", "categories", controllers.category_books)
# @app.add_url_rule("/register", "register", controllers.user_register, methods=['GET', 'POST'])
# @app.add_url_rule("/login", "login", controllers.user_login, methods=['GET', 'POST'])
# @app.add_url_rule("/user-logout", "logout", controllers.logout_user)
# @app.add_url_rule("/admin-login", "admin-login", controllers.admin_login, methods=['POST'])
# @app.add_url_rule("/cart", "cart", controllers.cart)
# @app.add_url_rule("/api/cart", "add-cart", controllers.add_to_cart, methods=["POST"])
# @app.context_processor
# def common_response():
#     categories = utils.load_categories()
#     books = utils.load_books()
#     return {
#         'categories': categories,
#         'books': books,
#     }
#
#
# @login.user_loader
# def user_load(user_id):
#     return utils.get_user_by_id(user_id)
#
#
# if __name__ == '__main__':
#     from managementbook.admin import *
#
#     app.run(debug=True)

from flask import render_template, request, redirect, url_for, session, jsonify
from managementbook import app, login
from managementbook.models import UserRole
from flask_login import login_user, logout_user, login_required
from managementbook.decorators import annonymous_user
import utils, pdb
import cloudinary.uploader


@app.route("/")
def index():
    msg = ""
    category_id = request.args.get('category_id')
    keyword = request.args.get('keyword')

    books = utils.load_books(category_id=category_id, keyword=keyword)

    if not books:
        msg = "Không tìm thấy sách!"

    return render_template('index.html',
                           books=books, msg=msg)


@app.route('/books/<int:book_id>')
def details(book_id):
    b = utils.get_product_by_id(book_id)
    return render_template('details.html', book=b)


@app.route('/category/<int:category_id>')
def category_books(category_id):
    books = utils.load_books(category_id, keyword=None)
    return render_template('categories.html', books=books)


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username, phone=phone, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('index'))
            else:
                err_msg = "Xác nhận mật khẩu không đúng"
        except Exception as ex:
            err_msg = "Hệ thống đang có lỗi: " + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
@annonymous_user
def user_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_user_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng"
    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data['id'])

    key = app.config['CART_KEY']  # 'cart'
    cart = session[key] if key in session else {}
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        name = data['name']
        price = data['price']
        image = data['image']
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "image": image,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


@app.route('/api/cart/<book_id>', methods=['PUT'])
def update_cart(book_id):
    key = app.config['CART_KEY']  # 'cart'
    cart = session.get(key)

    if cart and book_id in cart:
        cart[book_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


@app.route('/api/cart/<book_id>', methods=['DELETE'])  # /api/cart/${book_id}
def delete_cart(book_id):
    key = app.config['CART_KEY'] # 'cart'
    cart = session.get(key)

    if cart and book_id in cart:
        del cart[book_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


@app.route("/api/pay")
@login_required
def pay():
    key = app.config['CART_KEY']  # 'cart'
    cart = session.get(key)

    try:
        utils.save_receipt(cart)
    except Exception as ex:
        print(str(ex))
        return jsonify({'status': 500})
    else:
        del session[key]

    return jsonify({'status': 200})


@app.context_processor
def common_response():
    categories = utils.load_categories()
    books = utils.load_books()
    return {
        'categories': categories,
        'books': books,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from managementbook.admin import *

    app.run(debug=True)
