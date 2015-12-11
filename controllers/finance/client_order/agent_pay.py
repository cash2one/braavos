# -*- coding: utf-8 -*-
import datetime
from flask import request, redirect, Blueprint, url_for, flash, g, abort, current_app
from flask import jsonify, render_template as tpl

from models.user import TEAM_LOCATION_CN
from models.client_order import ClientOrder, CONTRACT_STATUS_CN
from models.invoice import (AgentInvoice, AgentInvoicePay, AGENT_INVOICE_STATUS_PASS,
                            INVOICE_TYPE_CN, AGENT_INVOICE_STATUS_APPLY)
from models.user import User
from forms.invoice import AgentInvoiceForm
from libs.email_signals import agent_invoice_apply_signal
from libs.paginator import Paginator
from controllers.saler.client_order.agent_invoice import (new_invoice as _new_invoice,
                                                          update_invoice as _update_invoice, get_invoice_from)


finance_client_order_agent_pay_bp = Blueprint(
    'finance_client_order_agent_pay', __name__, template_folder='../../templates/finance/client_order')
ORDER_PAGE_NUM = 50


@finance_client_order_agent_pay_bp.route('/', methods=['GET'])
def index():
    if not g.user.is_finance():
        abort(404)
    orders = list(ClientOrder.all())
    if request.args.get('selected_status'):
        status_id = int(request.args.get('selected_status'))
    else:
        status_id = -1

    orderby = request.args.get('orderby', '')
    search_info = request.args.get('searchinfo', '')
    location_id = int(request.args.get('selected_location', '-1'))
    page = int(request.args.get('p', 1))
    # page = max(1, page)
    # start = (page - 1) * ORDER_PAGE_NUM
    if location_id >= 0:
        orders = [o for o in orders if location_id in o.locations]
    if status_id >= 0:
        orders = [o for o in orders if o.contract_status == status_id]
    if search_info != '':
        orders = [
            o for o in orders if search_info.lower() in o.search_invoice_info.lower()]
    if orderby and len(orders):
        orders = sorted(
            orders, key=lambda x: getattr(x, orderby), reverse=True)
    select_locations = TEAM_LOCATION_CN.items()
    select_locations.insert(0, (-1, u'全部区域'))
    select_statuses = CONTRACT_STATUS_CN.items()
    select_statuses.insert(0, (-1, u'全部合同状态'))
    paginator = Paginator(orders, ORDER_PAGE_NUM)
    try:
        orders = paginator.page(page)
    except:
        orders = paginator.page(paginator.num_pages)
    return tpl('/finance/client_order/agent_pay/index.html', orders=orders, title=u'全部客户付款',
               locations=select_locations, location_id=location_id,
               statuses=select_statuses, status_id=status_id,
               orderby=orderby, now_date=datetime.date.today(),
               search_info=search_info, page=page,
               params='&orderby=%s&searchinfo=%s&selected_location=%s&selected_status=%s' %
                      (orderby, search_info, location_id, status_id))


@finance_client_order_agent_pay_bp.route('/apply', methods=['GET'])
def apply():
    if not g.user.is_finance():
        abort(404)
    orders = list([
        invoicepay.agent_invoice.client_order for invoicepay in
        AgentInvoicePay.get_agent_invoices_pay_status(3)])
    return tpl('/finance/client_order/agent_pay/index_pass.html', orders=orders, title=u'申请中的客户付款')


@finance_client_order_agent_pay_bp.route('/pass', methods=['GET'])
def index_pass():
    if not g.user.is_finance():
        abort(404)
    orders = list([
        invoicepay.agent_invoice.client_order for invoicepay in
        AgentInvoicePay.get_agent_invoices_status(AGENT_INVOICE_STATUS_PASS)])
    return tpl('/finance/client_order/agent_pay/index.html', orders=orders, title=u'已打的款媒体信息')


@finance_client_order_agent_pay_bp.route('/<order_id>/info', methods=['GET'])
def info(order_id):
    if not g.user.is_finance():
        abort(404)
    order = ClientOrder.get(order_id)
    if not order:
        abort(404)
    invoices = AgentInvoice.query.filter_by(client_order=order)
    reminder_emails = [(u.id, u.name) for u in User.all_active()]
    new_invoice_form = AgentInvoiceForm()
    new_invoice_form.client_order.choices = [(order.id, order.name)]
    new_invoice_form.agent.choices = [(k.id, k.name) for k in order.agents]
    new_invoice_form.add_time.data = datetime.date.today()
    return tpl('/finance/client_order/agent_pay/info.html',
               order=order, invoices=invoices, new_invoice_form=new_invoice_form,
               reminder_emails=reminder_emails, INVOICE_TYPE_CN=INVOICE_TYPE_CN)


@finance_client_order_agent_pay_bp.route('/<invoice_id>/pay_info', methods=['GET'])
def pay_info(invoice_id):
    if not g.user.is_finance():
        abort(404)
    invoice = AgentInvoice.get(invoice_id)
    form = get_invoice_from(invoice)
    reminder_emails = [(u.name, u.email) for u in User.all_active()]
    return tpl('/finance/client_order/agent_pay/pay_info.html',
               form=form, invoice=invoice, reminder_emails=reminder_emails,
               INVOICE_TYPE_CN=INVOICE_TYPE_CN)


@finance_client_order_agent_pay_bp.route('/<invoice_id>/pay_time/update', methods=['POST'])
def invoice_pay_time_update(invoice_id):
    pay_time = request.values.get('pay_time', '')
    invoice = AgentInvoicePay.get(invoice_id)
    invoice.pay_time = pay_time
    invoice.save()
    flash(u'保存成功!', 'success')
    invoice.client_order.add_comment(g.user,
                                     u"更新了付款时间:\n\r%s" % pay_time,
                                     msg_channel=5)
    return jsonify({'ret': True})


@finance_client_order_agent_pay_bp.route('/<invoice_id>/pay_num', methods=['POST'])
def invoice_pay_num(invoice_id):
    if not g.user.is_finance():
        abort(404)
    invoice = AgentInvoice.get(invoice_id)
    if not invoice:
        abort(404)
    pay_money = request.form.get('pay_money', 0)
    invoice.pay_money = pay_money
    invoice.save()
    flash(u'保存成功!', 'success')
    invoice.client_order.add_comment(g.user,
                                     u"更新了打款金额:\n\r%s" % invoice.pay_money,
                                     msg_channel=5)
    return redirect(url_for("finance_client_order_agent_pay.info", order_id=invoice.client_order.id))


@finance_client_order_agent_pay_bp.route('/<invoice_id>/pass', methods=['POST'])
def invoice_pass(invoice_id):
    if not g.user.is_finance():
        abort(404)
    invoice = AgentInvoice.get(invoice_id)
    if not invoice:
        abort(404)
    invoices_ids = request.values.getlist('invoices')
    invoices_pay = AgentInvoicePay.gets(invoices_ids)
    if not invoices_pay:
        abort(403)
    emails = request.values.getlist('email')
    msg = request.values.get('msg', '')
    action = int(request.values.get('action', 0))

    to_users = invoice.client_order.direct_sales + invoice.client_order.agent_sales + \
        [invoice.client_order.creator, g.user]

    if action != 10:
        invoice_status = AGENT_INVOICE_STATUS_PASS
        action_msg = u'代理返点已打款'
        for invoice_pay in invoices_pay:
            invoice_pay.pay_status = invoice_status
            invoice_pay.save()
            flash(u'代理订单款已打,名称:%s, 打款金额%s' % (
                invoice_pay.agent_invoice.client_order.name +
                '-' + invoice_pay.agent_invoice.agent.name,
                str(invoice_pay.money)), 'success')
            invoice_pay.agent_invoice.client_order.add_comment(
                g.user, u'代理订单款已打款,名称%s, 打款金额%s ' % (
                    invoice_pay.agent_invoice.client_order.name +
                        '-' + invoice_pay.agent_invoice.agent.name,
                    str(invoice_pay.money)),
                msg_channel=5)
    else:
        action_msg = u'消息提醒'
    context = {"to_users": to_users,
               "action_msg": action_msg,
               "info": msg,
               "invoice": invoice,
               "order": invoice.client_order,
               "send_type": 'end',
               "invoice_pays": invoices_pay}
    agent_invoice_apply_signal.send(
        current_app._get_current_object(), context=context)
    return redirect(url_for("finance_client_order_agent_pay.pay_info", invoice_id=invoice_id))


@finance_client_order_agent_pay_bp.route('/<invoice_id>/<pid>/pay_delete', methods=['GET'])
def invoice_pay_delete(invoice_id, pid):
    invoice = AgentInvoice.get(invoice_id)
    invoice_pay = AgentInvoicePay.get(pid)
    flash(u'删除成功', 'success')
    invoice.client_order.add_comment(g.user, u"删除了付款信息  发票号：%s  付款金额：%s元  付款时间：%s" % (
        invoice.invoice_num, str(invoice_pay.money), invoice_pay.pay_time_cn), msg_channel=5)
    invoice_pay.delete()
    return redirect(url_for("finance_client_order_agent_pay.pay_info", invoice_id=invoice_id))


@finance_client_order_agent_pay_bp.route('/<order_id>/order/new', methods=['POST'])
def new_invoice(order_id, redirect_endpoint='finance_client_order_agent_pay.info'):
    return _new_invoice(order_id, redirect_endpoint)


@finance_client_order_agent_pay_bp.route('/<invoice_id>/update', methods=['POST'])
def update_invoice(invoice_id, redirect_endpoint='finance_client_order_agent_pay.info'):
    return _update_invoice(invoice_id, redirect_endpoint)


@finance_client_order_agent_pay_bp.route('/<invoice_id>/invoice/pay/new', methods=['POST'])
def new_invoice_pay(invoice_id):
    money = float(request.values.get('money', 0))
    pay_time = request.values.get('pay_time', '')
    detail = request.values.get('detail', '')
    mi = AgentInvoice.get(invoice_id)
    if mi.pay_invoice_money + money > mi.money:
        flash(u'付款金额大于发票金额，请重新填写!', 'danger')
        return redirect(url_for('saler_client_order_agent_invoice.invoice', invoice_id=invoice_id))
    pay = AgentInvoicePay.add(money=money,
                              agent_invoice=mi,
                              pay_time=pay_time,
                              pay_status=AGENT_INVOICE_STATUS_PASS,
                              detail=detail)
    pay.save()
    flash(u'付款成功!', 'success')
    pay.agent_invoice.client_order.add_comment(g.user, u'代理订单款已打款,名称%s, 打款金额%s ' % (
        pay.agent_invoice.client_order.name +
        '-' + pay.agent_invoice.agent.name,
        str(pay.money)),
        msg_channel=5)
    return redirect(url_for("finance_client_order_agent_pay.pay_info", invoice_id=invoice_id))
