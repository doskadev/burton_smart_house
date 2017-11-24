from flask import g
from flask import request
from flask import url_for
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect
from wtforms import PasswordField
from app import app, db
from models import Entry, Tag, User


class AdminAuthentication():
    def if_accessible(self):
        return g.user.is_authenticated and g.user.is_admin()


class BaseModelView(AdminAuthentication, ModelView):
    pass


class SlugModelView(BaseModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(SlugModelView, self).on_model_change(form, model, is_created)


class EntryModelView(ModelView):
    column_searchable_list = ['title', 'body']
    column_list = ['title', 'status', 'tease', 'tag_list', 'created_timestamp']


class UserModelView(ModelView):
    column_filters = ('email', 'name', 'active')
    column_list = ['email', 'name', 'admin','active', 'created_timestamp']
    colunm_searchable_list = ['email', 'name']

    form_column = ['email', 'password', 'name', 'active']
    form_extra_fields = {'password': PasswordField('New password')}

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)


class SmartHouseFileAdmin(AdminAuthentication, FileAdmin):
    pass


class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (g.user.is_authenticated and g.user.is_admin()):
            return redirect(url_for('login', next=request.path))
        return self.render('admin/index.html')


admin = Admin(app, 'Blog Admin', index_view=IndexView())
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(SmartHouseFileAdmin(app.config['STATIC_DIR'], '/static/', name='Static Files'))
