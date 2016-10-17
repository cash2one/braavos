# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, Blueprint, flash, json, g, current_app
from flask import render_template as tpl

from models.user import (User, Okr, OKR_STATUS_APPLY, OKR_STATUS_NORMAL, OKR_QUARTER_CN, OKR_STATUS_EVALUATION_APPLY)
from libs.email_signals import account_okr_apply_signal

account_okr_bp = Blueprint(
    'account_okr', __name__, template_folder='../../templates/account/okr/')

YEAR_LIST = ['2016', '2017', '2018', '2019', '2020']
PRIORITY_LIST = ['P0', 'P1', 'P2', 'P3']


# 显示用户名下所有的okr记录,列表信息形式.点击季度quarter显示详情
@account_okr_bp.route('/')
def index():
    okrs = [k for k in Okr.all() if k.creator == g.user]
    # 后面接一个排序按照日期早晚
    return tpl('/account/okr/index.html', okrs=okrs)


# 填写okr表格
@account_okr_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        okr_json = request.values.get('okr_json')
        o_kr = json.loads(okr_json)
        status = int(o_kr['status'])
        year = int(o_kr['year'])
        quarter = int(o_kr['quarter'])
        okrtext = json.dumps(o_kr['okrs'])
        # 判断是否填写过,下拉框 id=quarter
        if Okr.query.filter_by(quarter=quarter, year=year,
                               creator=g.user).first():
            flash(u'您已经填写过该季度的OKR表了!', 'danger')
            return tpl('/account/okr/update_new.html',
                       okrlist=o_kr['okrs'],
                       year=year,
                       quarter=quarter,
                       year_list=YEAR_LIST,
                       quarters=OKR_QUARTER_CN,
                       priority_list=PRIORITY_LIST)
        newokr = Okr.add(
            year=year,
            quarter=quarter,
            status=status,
            o_kr=okrtext,
            creator=g.user,
        )
        if int(status) == OKR_STATUS_NORMAL:
            flash(u'添加成功', 'success')
        else:
            flash(u'已发送申请', 'success')
            account_okr_apply_signal.send(
                current_app._get_current_object(), okr=newokr)
        return redirect(url_for('account_okr.index'))
    return tpl('/account/okr/create.html',
               year_list=YEAR_LIST,
               quarters=OKR_QUARTER_CN,
               priority_list=PRIORITY_LIST)


# update the OKR by changing the content in database without creating new log
@account_okr_bp.route('/<user_id>/<lid>/update', methods=['GET', 'POST'])
def update(user_id, lid):
    okr_old = Okr.query.get(lid)
    if okr_old.creator != g.user:
        flash(u'没事改别人东西干嘛,有时间多写写代码!', 'danger')
        return redirect(url_for('account_okr.index'))
    if request.method == 'POST':
        okr_json = request.values.get('okr_json')
        o_kr = json.loads(okr_json)
        quarter = int(o_kr['quarter'])
        status = int(o_kr['status'])
        year = int(o_kr['year'])
        okrtext = json.dumps(o_kr['okrs'])
        if quarter == okr_old.quarter and year == okr_old.year:
            okr_update = Okr.query.get(lid)
            okr_update.year = year
            okr_update.quarter = quarter
            okr_update.status = status
            okr_update.o_kr = okrtext
            okr_update.creator_id = user_id
            okr_update.save()
            if int(status) == OKR_STATUS_APPLY:
                flash(u'已发送申请', 'success')
                account_okr_apply_signal.send(
                    current_app._get_current_object(), okr=okr_update)
            else:
                flash(u'修改成功', 'success')
            return redirect(url_for('account_okr.index'))
        elif Okr.query.filter_by(quarter=quarter, year=year, creator=g.user).first():
            flash(u'您已经填写过该季度的OKR表了!', 'danger')
            return tpl('/account/okr/update_new.html',
                       okrlist=o_kr['okrs'],
                       year=year,
                       quarter=quarter,
                       year_list=YEAR_LIST,
                       quarters=OKR_QUARTER_CN,
                       priority_list=PRIORITY_LIST)
        okr_update = Okr.query.get(lid)
        okr_update.year = year
        okr_update.quarter = quarter
        okr_update.status = status
        okr_update.o_kr = okrtext
        okr_update.creator_id = user_id
        okr_update.save()
        if int(status) == OKR_STATUS_APPLY:
            flash(u'已发送申请', 'success')
            account_okr_apply_signal.send(
                current_app._get_current_object(), okr=okr_update)
        else:
            flash(u'修改成功', 'success')
        return redirect(url_for('account_okr.index'))
    okr = Okr.query.get(lid)
    okrlist = json.loads(okr.o_kr)
    return tpl('/account/okr/update_new.html',
               okr=okr,
               okrlist=okrlist,
               year=str(okr.year),
               quarter=okr.quarter,
               year_list=YEAR_LIST,
               quarters=OKR_QUARTER_CN,
               priority_list=PRIORITY_LIST)


# delete the log in database
@account_okr_bp.route('/<user_id>/<lid>/delete')
def delete(user_id, lid):
    okr = Okr.get(lid)
    if okr.creator != g.user:
        flash(u'没事删别人东西干嘛,有时间多写写代码!', 'danger')
        return redirect(url_for('account_okr.index'))
    okr.delete()
    flash(u'删除成功', 'success')
    return redirect(url_for('account_okr.index'))


# find the logs for subordinates
def _get_all_under_users(self_user_id):
    under_users = []
    all_user = [{'uid': user.id, 'is_kpi_leader': user.is_kpi_leader, 'leaders': [
        k.id for k in user.team_leaders]} for user in User.all() if user.is_active()]

    def get_under(under_users, all_user, self_user_id):
        d_user = [user for user in all_user if self_user_id in user['leaders']]
        for k in d_user:
            under_users.append(k)
            if k['is_kpi_leader'] and self_user_id != k['uid']:
                under_users += get_under(under_users, all_user, k['uid'])
        return under_users
    return get_under(under_users, all_user, self_user_id)


@account_okr_bp.route('/subordinates', methods=['GET'])
def subordinates():
    user_id = int(request.values.get('user_id', 0))
    quarter = int(request.values.get('quarter', 0))
    status = int(request.values.get('status', 100))
    year = int(request.values.get('year', 0))
    status_list = [2, 3, 6, 8, 9, 11, 12, 13]
    if g.user.is_super_leader():
        okr = [k for k in Okr.all() if k.status in status_list]
        under_users = [{'uid': k.id, 'name': k.name} for k in User.all()]
    else:
        under_users = _get_all_under_users(g.user.id)
        sub = []
        for under in under_users:
            sub.append(User.query.get(under['uid']))
        okr = [k for k in Okr.all() if k.status in status_list and k.creator in sub]

    if user_id:
        okr = [k for k in okr if k.creator.id == int(user_id)]
    if status != 100:
        okr = [k for k in okr if k.status == status]
    if year:
        okr = [o for o in okr if o.year == year]
    if quarter:
        okr = [o for o in okr if o.quarter == quarter]
    okrs = sorted(okr, key=lambda x: x.year, reverse=True)
    return tpl('/account/okr/subordinates.html', okrs=okrs, user_id=user_id,
               quarter=quarter, year=year,
               title=u'下属的OKR申请审核列表', under_users=under_users, status=status,
               params="&user_id=%s&status=%s&year=%s&quarter=%s" % (
                   user_id, str(status), year, quarter),
               )


# display the detail okr content of the subordinates
@account_okr_bp.route('/<lid>/info', methods=['GET', 'POST'])
def info(lid):
    okr = Okr.query.get(lid)
    status_list_leader = [2, 3, 4, 6, 8, 9, 11, 12, 13]
    status_list_normal = [3, 6, 9, 10, 11, 12, 13]
    team_leaders = User.get(okr.creator.id).team_leaders
    if g.user == okr.creator:
        pass
    elif g.user in team_leaders or g.user.is_super_leader():
        if okr.status in status_list_leader:
            pass
        else:
            flash(u'您无权查阅', 'danger')
            return redirect(url_for('account_okr.index'))
    else:
        if okr.status not in status_list_normal:
            flash(u'您无权查阅', 'danger')
            return redirect(url_for('account_okr.index'))
    okrlist = json.loads(okr.o_kr)
    under_user = _get_all_under_users(g.user.id)
    if okr.creator_id not in [u['uid'] for u in under_user]:
        mark = False
    else:
        mark = True
    if not (g.user.is_super_leader() or g.user.is_HR_leader() or mark or g.user == okr.creator):
        okr.summary = u'您无权查看okr小结'
    users = []
    for u in under_user:
        if u['uid'] != okr.creator_id:
            users.append(User.query.get(u['uid']))
    return tpl('/account/okr/info.html', okrlist=okrlist, okr=okr, users=users)


@account_okr_bp.route('/<user_id>/<lid>/status', methods=['GET', 'POST'])
def status(user_id, lid):
    okr = Okr.query.get(lid)
    if okr.creator != g.user and not \
            (
            g.user.is_kpi_leader or
            g.user.is_HR_leader() or
            g.user.is_super_leader() or
            g.user.is_super_admin()
            ):
        flash(u'您无权操作', 'danger')
        return redirect(url_for('account_okr.index'))
    okr_status = int(request.values.get('status', okr.status))
    if okr_status == 9 or okr_status == 10:
        comment = request.values.get('comment', '')
        score_okr = request.values.get('score', None)
        okr.comment = comment
        okr.score_okr = score_okr
    okr.status = okr_status
    okr.save()
    flash(okr.status_cn, 'success')
    if okr_status in [0, 2, 3, 4, 7, 8, 9, 10]:
        account_okr_apply_signal.send(current_app._get_current_object(), okr=okr)
    return redirect(url_for('account_okr.index'))


# evaluate okr in the mid of a quarter
@account_okr_bp.route('/<user_id>/<lid>/mid_evaluate', methods=['GET', 'POST'])
def mid_evaluate(user_id, lid):
    okr = Okr.query.get(lid)
    if okr.creator != g.user:
        flash(u'对不起,限本人操作', 'danger')
        return redirect(url_for('account_okr.index'))
    okrlist = json.loads(okr.o_kr)

    if request.method == 'POST':
        okr_json = request.values.get('okr_json')
        o_kr = json.loads(okr_json)

        status = int(o_kr['status'])
        okrtext = json.dumps(o_kr['okrs'])
        okr_update = Okr.query.get(lid)
        okr_update.status = status
        okr_update.o_kr = okrtext
        okr_update.save()
        flash(u'修改成功', 'success')
        return redirect(url_for('account_okr.index'))

    if okr.status == 3:
        return tpl('/account/okr/mid_evaluate.html',
                   okrlist=okrlist,
                   okr=okr,
                   priority_list=PRIORITY_LIST)
    else:
        return tpl('/account/okr/update_mid_eval.html',
                   okrlist=okrlist,
                   okr=okr,
                   )


@account_okr_bp.route('/<user_id>/<lid>/final_evaluate', methods=['GET', 'POST'])
def final_evaluate(user_id, lid):
    okr = Okr.query.get(lid)
    if g.user != okr.creator:
        flash(u'对不起，您没有权给别人的绩效考核评分!', 'danger')
        return redirect(url_for('account_okr.index'))
    if okr.status not in [6, 7, 10]:
        flash(u'对不起，不是有效评分时间!', 'danger')
        return redirect(url_for('account_okr.index'))
    okrlist = json.loads(okr.o_kr)
    if request.method == 'POST':
        # 拿到评价的数据以及insert的查询字段
        okr_json = request.values.get('okr_json')
        o_kr = json.loads(okr_json)
        status = int(o_kr['status'])
        summary = o_kr['summary']
        okrtext = json.dumps(o_kr['okrs'])
        okr_update = Okr.query.get(lid)
        okr_update.status = status
        okr_update.summary = summary
        okr_update.o_kr = okrtext
        okr_update.save()

        if int(status) == OKR_STATUS_EVALUATION_APPLY:
            flash(u'已发送申请', 'success')
            account_okr_apply_signal.send(
                current_app._get_current_object(), okr=okr_update)
        else:
            flash(u'修改成功', 'success')
        return redirect(url_for('account_okr.index'))

    if okr.status == 6:
        return tpl('/account/okr/final_evaluate.html',
                   okrlist=okrlist,
                   okr=okr,
                   priority_list=PRIORITY_LIST)
    else:
        return tpl('/account/okr/update_final_eval.html',
                   okrlist=okrlist,
                   okr=okr,
                   )


@account_okr_bp.route('/all_okrs', methods=['GET'])
def allokrs():
    status = int(request.values.get('status', 100))
    user_id = int(request.values.get('user_id', 0))
    year = int(request.values.get('year', 0))
    quarter = int(request.values.get('quarter', 0))

    status_list = [3, 6, 9, 11, 12, 13]
    okrs = [o for o in Okr.query.filter(Okr.creator_id != g.user.id) if o.status in status_list]
    if status != 100:
        okrs = [o for o in okrs if o.status == status]
    if user_id:
        okrs = [o for o in okrs if o.creator_id == user_id]
    if year:
        okrs = [o for o in okrs if o.year == year]
    if quarter:
        okrs = [o for o in okrs if o.quarter == quarter]
    for k in okrs:
        if k.score_colleague:
            k.colleague_ids = json.loads(k.score_colleague).keys()
    return tpl('all_okrs.html', okrs=okrs, status=status, users=User.all_active(),
               params="&status=%s&user_id=%s$year=%s&quarter=%s" % (str(status), str(user_id), str(year), str(quarter)),
               user_id=user_id, year=year, quarter=quarter
               )


@account_okr_bp.route('/<lid>/qualification_score', methods=['GET', 'POST'])
def qualification(lid):
    if not (g.user.is_kpi_leader or g.user.is_super_leader()):
        flash(u'对不起，您没有权给别人的绩效考核评分!', 'danger')
        return redirect(url_for('account_okr.index'))
    okr = Okr.query.get(lid)
    if okr.status not in [9, 11, 12]:
        flash(u'对不起，不是有效评分时间!', 'danger')
        return redirect(url_for('account_okr.index'))
    okr_status = int(request.values.get('status', okr.status))
    under_user = _get_all_under_users(g.user.id)
    users = []
    for u in under_user:
        if u['uid'] != okr.creator_id and User.get(u['uid']) not in users:
            users.append(User.query.get(u['uid']))
    if request.method == 'POST':
        personnals = request.form.getlist('personnals')
        okr.score_colleague = json.dumps(dict((p, {}) for p in personnals))

        score_leader = {}
        score_leader['knowledge_res'] = request.values.get('knowledge_res', '')
        score_leader['positive_res'] = request.values.get('positive_res', '')
        score_leader['team_res'] = request.values.get('team_res', '')
        score_leader['teach_res'] = request.values.get('teach_res', '')
        score_leader['abide_res'] = request.values.get('abide_res', '')
        score_leader['knowledge_s'] = float(
            request.values.get('knowledge_s', 0.00))
        score_leader['positive_s'] = float(
            request.values.get('positive_s', 0.00))
        score_leader['team_s'] = float(request.values.get('team_s', 0.00))
        score_leader['teach_s'] = float(request.values.get('teach_s', 0.00))
        score_leader['abide_s'] = float(request.values.get('abide_s', 0.00))
        okr.score_leader = json.dumps(score_leader)
        okr.status = okr_status
        okr.save()
        flash(u'已发送申请', 'success')
        account_okr_apply_signal.send(
            current_app._get_current_object(), okr=okr)
        okrs = [k for k in Okr.all() if k.creator == g.user]
        return tpl('/account/okr/index.html', okrs=okrs)
    scores = [float(k) / 10 for k in range(1, 51)]
    scores.append(0.00)
    scores.reverse()
    score_leader = json.loads(okr.score_leader)
    return tpl('/account/okr/qualification_score.html', okr=okr, scores=scores, users=users, score_leader=score_leader)


@account_okr_bp.route('/<uid>/<lid>/mutual_evaluate', methods=['GET', 'POST'])
def mutual_evaluate(lid, uid):
    okr = Okr.get(lid)
    score_colleague = json.loads(okr.score_colleague)
    if str(uid) not in score_colleague.keys():
        flash(u'对不起，您没有权给别人的绩效考核评分!', 'danger')
        return redirect(url_for('account_okr.index'))
    if okr.status == 13:
        flash(u'考核已经归档,无法重新评分!', 'danger')
        return redirect(url_for('account_okr.index'))
    if request.method == 'POST':
        total_score = 0.0
        attitude_param = {}
        ability_param = {}
        for k in range(6):
            key = 'work_attitude_' + str(k) + '_s'
            attitude_param[key] = float(request.values.get(key, 0))
            if k == 0:
                total_score += attitude_param[key] * 0.05
            elif k == 1:
                total_score += attitude_param[key] * 0.1
            elif k == 2:
                total_score += attitude_param[key] * 0.1
            elif k == 3:
                total_score += attitude_param[key] * 0.05
            elif k == 4:
                total_score += attitude_param[key] * 0.05
            elif k == 5:
                total_score += attitude_param[key] * 0.05
        for k in range(9):
            key = 'work_ability_' + str(k) + '_s'
            ability_param[key] = float(request.values.get(key, 0))
            if k == 0:
                total_score += ability_param[key] * 0.1
            elif k == 1:
                total_score += ability_param[key] * 0.05
            elif k == 2:
                total_score += ability_param[key] * 0.1
            elif k == 3:
                total_score += ability_param[key] * 0.05
            elif k == 4:
                total_score += ability_param[key] * 0.05
            elif k == 5:
                total_score += ability_param[key] * 0.05
            elif k == 6:
                total_score += ability_param[key] * 0.05
            elif k == 7:
                total_score += ability_param[key] * 0.1
            elif k == 8:
                total_score += ability_param[key] * 0.05
        okr.total_score = total_score * 0.2
        score_colleague = json.loads(okr.score_colleague)
        score_colleague[str(uid)] = {'attitude_param': attitude_param, 'ability_param': ability_param}
        okr.score_colleague = json.dumps(score_colleague)
        if okr.is_mutual_evaluation_done():
            okr.status = 12
        okr.save()
        return redirect(url_for('account_okr.index'))
    body_obj = score_colleague[str(uid)]
    attitude_param = {}
    ability_param = {}
    if 'attitude_param' in body_obj:
        attitude_param = body_obj['attitude_param']
    if 'ability_param' in body_obj:
        ability_param = body_obj['ability_param']
    scores = [float(k) / 10 for k in range(1, 51)]
    scores.append(0.00)
    scores.reverse()
    return tpl('/account/okr/mutual_evaluate.html', okr=okr,
               scores=scores, attitude_param=attitude_param, ability_param=ability_param)


@account_okr_bp.route('/<lid>/to_excel', methods=['GET'])
def to_excel(lid):
    return redirect(url_for('account_okr.index'))
