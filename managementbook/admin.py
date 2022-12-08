from flask_admin import Admin, BaseView, expose
from managementbook import db, app
from managementbook.models import Category, Book
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', msg="Hello")


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class ProductView(ModelView):
    can_view_details = True


admin = Admin(app=app, name='Nhà sách OU', template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Book, db.session))
