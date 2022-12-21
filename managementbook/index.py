from flask import session
from managementbook import app, login, controllers, utils, admin

app.add_url_rule("/", "index", controllers.index)
app.add_url_rule("/books/<int:book_id>", "book-detail", controllers.details)
app.add_url_rule("/admin/book/create/", "create_book", controllers.create_book, methods=['GET'])
app.add_url_rule("/admin/book/post", "post_book", controllers.post_book, methods=['POST'])
app.add_url_rule("/admin/book/delete/<int:book_id>", "delete_book", controllers.delete_book)
app.add_url_rule("/admin/book/edit/<int:book_id>", "edit_book", controllers.edit_book)
app.add_url_rule("/admin/book/update/<int:book_id>", "update_book", controllers.update_book, methods=['GET', 'POST'])
app.add_url_rule("/admin/book/import_books/<int:book_id>", "import_books", controllers.import_books,
                 methods=['GET', 'POST'])
app.add_url_rule('/admin/receipt-details/<int:receipt_id>', "receipt_details", controllers.receipt_details)
app.add_url_rule('/admin/receipts/reload_receipt', "reload_receipt", controllers.reload_receipt)
app.add_url_rule("/category/<int:category_id>", "categories", controllers.category_books)
app.add_url_rule("/register", 'register-user', controllers.user_register, methods=['GET', 'POST'])
app.add_url_rule("/login", 'user-login', controllers.user_login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule("/cart", "cart", controllers.cart)
app.add_url_rule("/api/cart", "add-cart", controllers.add_to_cart, methods=["POST"])
app.add_url_rule('/api/cart/<book_id>', "update_cart", controllers.update_cart, methods=['PUT'])
app.add_url_rule('/api/cart/<book_id>', "delete-cart", controllers.delete_cart, methods=['DELETE'])
app.add_url_rule('/api/books/<book_id>/comments', "comments", controllers.comments)
app.add_url_rule('/api/books/<book_id>/comments', "add_comment", controllers.add_comment, methods=['post'])
app.add_url_rule("/api/pay", "pay", controllers.pay)


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
    app.run(debug=True)
