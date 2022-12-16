from flask_admin import Admin, BaseView, expose
import flask_login as login
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from managementbook import db, app, utils
from managementbook.models import Category, Book, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user, logout_user
from flask import redirect, render_template, request


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        stats = utils.count_product_by_cate()
        if current_user.user_role == UserRole.user:
            return redirect('/')
        return self.render('/admin/index.html', stats=stats)


class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = utils.stats_revenue(kw=request.args.get('kw'),
                                    from_date=request.args.get('from_date'),
                                    to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductView(ModelView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Gía'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }

    def is_accessible(self):
        return current_user.is_authenticated

class CategoryView(ModelView):
    # column_searchable_list = ['name', 'description']
    # column_filters = ['name', 'price']
    can_view_details = True
    can_export = True
    # column_exclude_list = ['image']
    # column_labels = {
    #     'name': 'Tên sản phẩm',
    #     'description': 'Mô tả',
    #     'price': 'Gía'
    # }
    # extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    # form_overrides = {
    #     'description': CKTextAreaField
    # }

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name='Nhà sách OU', template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(CategoryView(Category, db.session, name="Danh mục"))
admin.add_view(ProductView(Book, db.session, name="Thực hiện tác vụ sách"))
admin.add_view(StatsView(name="Thống kê"))
admin.add_view(LogoutView(name="Logout"))
