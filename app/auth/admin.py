from flask import redirect, url_for
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from .. import db
from ..models import roles, stocks, users


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 3

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 3

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


admin = Admin(
    template_mode="bootstrap3", index_view=CustomAdminIndexView(url="/auth/admin")
)
admin.add_view(AdminModelView(users.User, db.session))
admin.add_view(AdminModelView(roles.Role, db.session))
admin.add_view(AdminModelView(stocks.Stock, db.session))
admin.add_view(AdminModelView(stocks.StockPrice, db.session))
admin.add_link(MenuLink("Back to site", url="/"))
