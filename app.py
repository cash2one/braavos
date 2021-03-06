#-*- coding: utf-8 -*-
from flask import g, request, url_for, redirect, render_template
from flask.ext.login import LoginManager, current_user

from factory import create_app
from urls import register_blueprint
from config import config_object

from flask_debugtoolbar import DebugToolbarExtension
from models.user import UserHandBook
from models.account.data import Notice, PersonNotice

app = create_app(config_object)
# toolbar = DebugToolbarExtension(app)

login_manager = LoginManager()
login_manager.login_message = None
login_manager.init_app(app)
login_manager.login_view = "user.login"


def page_recipe(pages, adjacent_pages=3):
    paginator = pages.paginator
    page_numbers = [n for n in range(
        pages.number - adjacent_pages, pages.number + adjacent_pages + 1) if n > 0 and n <= paginator.num_pages]

    return page_numbers

app.jinja_env.filters['page_recipe'] = page_recipe


@app.route('/email')
def get_email_sigal():
    return render_template("/user/email_sigal.html")


@login_manager.user_loader
def load_user(userid):
    from models.user import User
    return User.get(userid)


@app.before_request
def request_user():
    if request.path.startswith(u'/files/') and current_user is None:
        return login_manager.unauthorized()
    if current_user and current_user.is_authenticated():
        g.user = current_user
    elif url_for('user.login') != request.path and not request.path.startswith(u'/static/') \
            and not request.path.startswith('/api/'):
        return login_manager.unauthorized()


@app.route('/')
def index():
    if not UserHandBook.query.filter_by(user=g.user).first() and not g.user.is_other_person():
        return redirect(url_for('account_data.handbook'))
    notices = Notice.all()[:4]
    person_notices = PersonNotice.query.filter_by(user=g.user)[:4]
    return render_template("wellcome.html", notices=notices, person_notices=person_notices)
    # if g.user.is_searchad_member() and (not g.user.is_admin()) and (not g.user.is_super_leader()):
    #     return redirect(url_for('searchAd_order.index'))
    # return redirect(url_for('order.index'))

# urls
register_blueprint(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

