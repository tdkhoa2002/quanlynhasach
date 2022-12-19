import hashlib

import cloudinary.uploader
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required

from managementbook import app, utils, db
from managementbook.decorators import annonymous_user
from managementbook.models import User


def index():
    msg = ""
    category_id = request.args.get('category_id')
    keyword = request.args.get('keyword')

    books = utils.load_books(category_id=category_id, keyword=keyword)

    if not books:
        msg = "Không tìm thấy sách!"

    return render_template('index.html',
                           books=books, msg=msg)


def details(book_id):
    b = utils.get_product_by_id(book_id)
    return render_template('details.html', book=b)


def category_books(category_id):
    books = utils.load_books(category_id, keyword=None)
    return render_template('categories.html', books=books)


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

        if username:
            user_by_username = User.query.filter(User.username.__eq__(username.strip())).first()
            if user_by_username:
                err_msg="Ten tai khoan da co nguoi su dung"
            else:
                try:
                    if password.strip().__eq__(confirm.strip()):
                        avatar = request.files.get('avatar')
                        if avatar:
                            res = cloudinary.uploader.upload(avatar)
                            avatar_path = res['secure_url']

                        utils.add_user(name=name, username=username, phone=phone, password=password, email=email,
                                       avatar=avatar_path)
                        return redirect(url_for('index'))
                    else:
                        err_msg = "Xác nhận mật khẩu không đúng"
                except Exception as ex:
                    err_msg = "Hệ thống đang có lỗi: " + str(ex)


        # try:
        #     if password.strip().__eq__(confirm.strip()):
        #         avatar = request.files.get('avatar')
        #         if avatar:
        #             res = cloudinary.uploader.upload(avatar)
        #             avatar_path = res['secure_url']
        #
        #         utils.add_user(name=name, username=username, phone=phone, password=password, email=email,
        #                        avatar=avatar_path)
        #         return redirect(url_for('index'))
        #     else:
        #         err_msg = "Xác nhận mật khẩu không đúng"
        # except Exception as ex:
        #     err_msg = "Hệ thống đang có lỗi: " + str(ex)

    return render_template('register.html', err_msg=err_msg)


@annonymous_user
def user_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_user_login(username=username, password=password)
        if user:
            if user.active:
                login_user(user=user)
                return redirect(url_for('index'))
            elif not user.active:
                err_msg = "Người dùng đã bị admin chặn"
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng"
    return render_template('login.html', err_msg=err_msg)


def logout_my_user():
    logout_user()
    return redirect('/login')


def cart():
    return render_template('cart.html')


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


# @app.route('/api/cart/<book_id>', methods=['PUT'])
def update_cart(book_id):
    key = app.config['CART_KEY']  # 'cart'
    cart = session.get(key)

    if cart and book_id in cart:
        cart[book_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


# @app.route('/api/cart/<book_id>', methods=['DELETE'])  # /api/cart/${book_id}
def delete_cart(book_id):
    key = app.config['CART_KEY']  # 'cart'
    cart = session.get(key)

    if cart and book_id in cart:
        del cart[book_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


# @app.route('/api/books/<book_id>/comments')  # /api/products/<book_id>/comments
def comments(book_id):
    data = []
    for cmt in utils.load_comments(book_id=book_id):
        data.append({
            'id': cmt.id,
            'content': cmt.content,
            'created_date': str(cmt.created_date),
            'user': {
                'name': cmt.user.name,
                'avatar': cmt.user.avatar
            }
        })

    return jsonify(data)


# @app.route('/api/books/<book_id>/comments', methods=['post'])
def add_comment(book_id):
    try:
        c = utils.save_comment(book_id=book_id, content=request.json['content'])

    except:
        return jsonify({'status': 500})

    return jsonify({
        'status': 204,
        'comment': {
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.avatar
            }
        }
    })


# @app.route("/api/pay")
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
