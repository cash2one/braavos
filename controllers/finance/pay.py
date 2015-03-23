# -*- coding: utf-8 -*-
import datetime

from flask import request, redirect, Blueprint, url_for, flash, g, abort, current_app
from flask import render_template as tpl

from models.client_order import ClientOrder
from models.outsource import OutSource, OUTSOURCE_STATUS_APPLY_MONEY, OUTSOURCE_STATUS_PAIED
from models.user import User
from libs.signals import outsource_apply_signal


finance_pay_bp = Blueprint(
    'finance_pay', __name__, template_folder='../../templates/finance')


@finance_pay_bp.route('/', methods=['GET'])
def index():
    orders = [k for k in list(ClientOrder.all()) if k.get_outsources_by_status(
        OUTSOURCE_STATUS_APPLY_MONEY)]
    return tpl('/finance/pay/index.html', orders=orders)


@finance_pay_bp.route('/<order_id>/info', methods=['GET'])
def info(order_id):
    order = ClientOrder.get(order_id)
    if not order:
        abort(404)
    outsources_data = {
        'PAIED': [{'outsource': x} for x in order.get_outsources_by_status(OUTSOURCE_STATUS_PAIED)],
        'APPLY_MONEY': [{'outsource': x} for x in order.get_outsources_by_status(OUTSOURCE_STATUS_APPLY_MONEY)],
    }
    reminder_emails = [(u.name, u.email) for u in User.all_active()]
    return tpl('/finance/pay/info.html', order=order,
               outsources_data=outsources_data, reminder_emails=reminder_emails)


@finance_pay_bp.route('/<outsource_id>/pass', methods=['POST'])
def pass_outsource(outsource_id):
    outsource = OutSource.get(outsource_id)
    if not outsource:
        abort(404)
    outsources_ids = request.values.getlist('outsources')
    outsources = OutSource.gets(outsources_ids)
    if not outsources:
        abort(403)
    emails = request.values.getlist('email')
    msg = request.values.get('msg', '')
    action = int(request.values.get('action', 0))

    to_users = outsource.client_order.direct_sales + outsource.client_order.agent_sales + \
        [outsource.client_order.creator, g.user] + \
        outsource.client_order.leaders
    to_emails = list(set(emails + [x.email for x in to_users]))

    if action != 10:
        outsource_status = OUTSOURCE_STATUS_PAIED
        action_msg = u'外包款已打'
        for outsource in outsources:
            outsource.status = outsource_status
            outsource.create_time = datetime.date.today()
            outsource.save()
            flash(u'外包款已打，名称%s ' % (outsource.name), 'success')
            outsource.client_order.add_comment(
                g.user, u'外包款已打，名称%s ' % (outsource.name), msg_channel=2)
    else:
        action_msg = u'消息提醒'

    apply_context = {"sender": g.user,
                     "to": to_emails,
                     "action_msg": action_msg,
                     "msg": msg,
                     "order": outsource.client_order,
                     "outsources": outsources}
    outsource_apply_signal.send(
        current_app._get_current_object(), apply_context=apply_context)
    flash(u'外包款已打，名称%s ' % (outsource.name), 'info')
    return redirect(url_for("finance_pay.info", order_id=outsource.client_order.id))
