# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, url_for, abort, g
from flask import render_template as tpl, flash, current_app
from flask.ext.login import login_user, logout_user, current_user

from . import admin_required
from models.user import Team, User, USER_STATUS_CN, DEFAULT_BIRTHDAY, DEFAULT_RECRUITED_DATE
from forms.user import LoginForm, PwdChangeForm, NewTeamForm, NewUserForm
from config import DEFAULT_PASSWORD
from local_config import DevelopmentConfig
from libs.email_signals import password_changed_signal
from libs.mail import check_auth_by_mail
from libs.files import all_files_set

user_bp = Blueprint('user', __name__, template_folder='../templates/user')
page_num = 50


@user_bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('user.users'))


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        is_pwd = request.values.get('is_pwd', '')
        if is_pwd:
            username = request.values.get('email', '')
            password = request.values.get('password', '')
            if check_auth_by_mail(username, password):
                user = User.query.filter_by(email=username).first()
            else:
                return tpl('login.html', form=form, msg=u"用户名或者密码错误.")
        else:
            password = request.values.get('password')
            if password == DEFAULT_PASSWORD and not DevelopmentConfig.DEBUG:
                return tpl('login.html', form=form, msg=u"用户名或者密码错误.")
            user = form.validate()
        if user:
            login_user(user)
            if user.check_password(DEFAULT_PASSWORD) and not is_pwd:
                flash(u'您还在使用默认密码, 请及时<a href="%s">修改您的密码!</a>' %
                      url_for('user.pwd_change'), 'danger')
            return redirect(request.args.get("next", "/"))
        return tpl('login.html', form=form, msg=u"用户名或者密码错误.")
    return tpl('login.html', form=form)


@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("user.login"))


@user_bp.route('/password_change', methods=['GET', 'POST'])
def pwd_change():
    form = PwdChangeForm(request.form)
    if request.method == 'POST':
        user = current_user
        if form.validate(user):
            user.set_password(form.password.data)
            password_changed_signal.send(
                current_app._get_current_object(), user=user)
            logout_user()
            return redirect('/')
    return tpl('pwd_change.html', form=form)


@user_bp.route('/teams')
@admin_required
def teams():
    teams = Team.all()
    return tpl('teams.html', teams=teams)


@user_bp.route('/users')
@admin_required
def users():
    users = User.all()
    return tpl('users.html', users=users)


@user_bp.route('/new_team', methods=['GET', 'POST'])
@admin_required
def new_team():
    form = NewTeamForm(request.form)
    if request.method == 'POST' and form.validate():
        db_team_name = Team.name_exist(form.name.data)
        if not db_team_name:
            team = Team.add(name=form.name.data,
                            type=form.type.data,
                            location=form.location.data,
                            admins=User.gets(form.admins.data))
            flash(u'新建团队(%s)成功!' % team.name, 'success')
        else:
            flash(u'新建团队(%s)失败，团队名称已经存在!' % form.name.data, 'danger')
            return tpl('new_team.html', form=form)
        if request.values.get('next'):
            return redirect(request.values.get('next'))
        return redirect(url_for("user.team_detail", team_id=team.id))
    return tpl('new_team.html', form=form)


@user_bp.route('/team/<team_id>', methods=['GET', 'POST'])
@admin_required
def team_detail(team_id):
    team = Team.get(team_id)
    if not team:
        abort(404)
    form = NewTeamForm(request.form)
    if request.method == 'POST':
        if form.validate():
            team.name = form.name.data
            team.type = form.type.data
            team.location = form.location.data
            team.admins = User.gets(form.admins.data)
            team.save()
            flash(u'保存成功!', 'success')
    else:
        form.name.data = team.name
        form.type.data = team.type
        form.location.data = team.location
        form.admins.data = [u.id for u in team.admins]
    return tpl('team_detail.html', team=team, form=form)


@user_bp.route('/new_user', methods=['GET', 'POST'])
@admin_required
def new_user():
    form = NewUserForm(request.form)
    if request.method == 'POST':
        if form.validate():
            db_user_name = User.name_exist(form.name.data)
            if not db_user_name:
                user = User.add(form.name.data, form.email.data, DEFAULT_PASSWORD,
                                Team.get(form.team.data), form.status.data,
                                team_leaders=User.gets(form.team_leaders.data),
                                birthday=form.birthday.data,
                                recruited_date=form.recruited_date.data,
                                positive_date=form.positive_date.data,
                                quit_date=form.quit_date.data,
                                cellphone=form.cellphone.data,
                                position=form.position.data,
                                sn=form.sn.data)
                flash(u'新建用户(%s)成功!' % user.name, 'success')
            else:
                flash(u'新建用户(%s)失败，用户名已经存在!' % form.name.data, 'danger')
                return tpl('new_user.html', form=form)
            return redirect(url_for("user.users"))
    return tpl('new_user.html', form=form)


@user_bp.route('/user/<user_id>', methods=['GET', 'POST'])
def user_detail(user_id):
    user = User.get(user_id)
    if not user:
        abort(404)
    form = NewUserForm(request.form)
    if request.method == 'POST':
        c_user = User.get_by_email(email=form.email.data.lower())
        if c_user and form.email.data.lower() != user.email:
            flash(u'保存保存失败，该邮箱已存在!', 'danger')
            return redirect(url_for('user.user_detail', user_id=user_id))
        if form.validate(vali_email=False):
            if g.user.team.is_admin() or g.user.is_HR() or g.user.is_HR_leader():
                # 只有管理员才有权限修改 username email team status
                user.name = form.name.data
                user.email = form.email.data
                user.team = Team.get(form.team.data)
                user.status = form.status.data
                user.team_leaders = User.gets(form.team_leaders.data)
                user.birthday = form.birthday.data
                user.recruited_date = form.recruited_date.data
                user.positive_date = form.positive_date.data
                user.quit_date = form.quit_date.data
                user.cellphone = form.cellphone.data
                user.position = form.position.data
                user.sn = form.sn.data
            elif g.user.id == user.id:
                user.birthday = form.birthday.data
                user.recruited_date = form.recruited_date.data
                user.cellphone = form.cellphone.data
                user.position = form.position.data
            user.save()
            flash(u'保存成功!', 'success')
            return redirect(url_for('user.user_detail', user_id=user_id))
    else:
        form.name.data = user.name
        form.email.data = user.email
        form.team.data = user.team_id
        form.status.data = user.status
        form.cellphone.data = user.cellphone
        form.position.data = user.position
        form.team_leaders.data = [u.id for u in user.team_leaders]
        form.birthday.data = user.birthday or DEFAULT_BIRTHDAY
        form.recruited_date.data = user.recruited_date or DEFAULT_RECRUITED_DATE
        form.positive_date.data = user.positive_date or DEFAULT_RECRUITED_DATE
        form.quit_date.data = user.quit_date or DEFAULT_RECRUITED_DATE
        form.sn.data = user.sn or ''
    if not (g.user.team.is_admin() or g.user.is_HR() or g.user.is_HR_leader()):
        form.name.readonly = True
        form.email.readonly = True
        form.team.readonly = True
        form.status.readonly = True
        form.sn.readonly = True
        form.status.choices = [(user.status, USER_STATUS_CN[user.status])]
        form.team_leaders.disabled = True
        form.team.choices = [(user.team_id, user.team.name)]
        form.team_leaders.choices = [(u.id, u.name) for u in user.team_leaders]
    return tpl('user_detail.html', user=user, form=form, DEFAULT_PASSWORD=DEFAULT_PASSWORD)


@user_bp.route('/<uid>/pic_upload', methods=['POST'])
def pic_upload(uid):
    user = User.get(uid)
    try:
        request.files['file'].filename.encode('gb2312')
    except:
        flash(u'文件名中包含非正常字符，请使用标准字符', 'danger')
        return redirect(url_for('user.user_detail', user_id=uid))
    filename = all_files_set.save(request.files['file'])
    user.add_user_pic_file(g.user, filename)
    flash(u'头像上传成功', 'success')
    return redirect(url_for('user.user_detail', user_id=uid))


@user_bp.route('/mine')
def mine():
    return redirect(url_for('user.user_detail', user_id=g.user.id))


@user_bp.route('/contact')
def contact():
    if g.user.is_super_leader() or g.user.is_leader() or g.user.is_HR() or g.user.is_OPS():
        users = User.all_active()
    else:
        abort(403)
    return tpl('contact.html', users=users)


@user_bp.route('/pwd_reset/<user_id>')
@admin_required
def pwd_reset(user_id):
    user = User.get(user_id)
    if not user:
        abort(404)
    user.set_password(DEFAULT_PASSWORD)
    user.save()
    return redirect(url_for('user.users'))
