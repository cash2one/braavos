#-*- coding: UTF-8 -*-
from flask import url_for, g, flash
from libs.mail import send_simple_mail, send_attach_mail, mail
from blinker import Namespace

from models.user import User

braavos_signals = Namespace()
password_changed_signal = braavos_signals.signal('password-changed')
add_comment_signal = braavos_signals.signal('add-comment')
order_apply_signal = braavos_signals.signal('order_apply')
reply_apply_signal = braavos_signals.signal('reply_apply')
contract_apply_signal = braavos_signals.signal('contract_apply')
douban_contract_apply_signal = braavos_signals.signal('douban_contract_apply')
framework_douban_contract_apply_signal = braavos_signals.signal(
    'framework_douban_contract_apply')
outsource_apply_signal = braavos_signals.signal('outsource_apply')
invoice_apply_signal = braavos_signals.signal('invoice_apply')
medium_rebate_invoice_apply_signal = braavos_signals.signal('medium_rebate_invoice_apply')
medium_invoice_apply_signal = braavos_signals.signal('medium_invoice_apply')
agent_invoice_apply_signal = braavos_signals.signal('agent_invoice_apply')
outsource_distribute_signal = braavos_signals.signal('outsource_distribute')
merger_outsource_apply_signal = braavos_signals.signal('merger_outsource_apply')
apply_leave_signal = braavos_signals.signal('apply_leave')
kpi_apply_signal = braavos_signals.signal('kpi_apply')
apply_out_signal = braavos_signals.signal('out_apply')
back_money_apply_signal = braavos_signals.signal('back_money_apply')
planning_bref_signal = braavos_signals.signal('planning_bref')


def password_changed(sender, user):
    send_simple_mail(u'InAd帐号密码重设通知',
                     recipients=[user.email],
                     body=u'您的InAd帐号密码已经被重新设置, 如果不是您的操作, 请联系广告平台管理员')


def add_comment(sender, comment):
    send_simple_mail(u'InAd留言提醒[%s]' % comment.target.name,
                     recipients=[
                         u.email for u in comment.target.get_mention_users(except_user=comment.creator)],
                     body=(u'%s的新留言:\n\n %s' % (comment.creator.name, comment.msg)))


def order_apply(sender, change_state_apply):
    url = mail.app.config['DOMAIN'] + url_for(
        'schedule.order_detail', order_id=change_state_apply.order.id, step=change_state_apply.next_step)
    send_simple_mail(u'【%s审批申请】%s-%s' % (change_state_apply.type_cn, change_state_apply.order.name, g.user.name),
                     recipients=[g.user.email],
                     body=(
                         u"""定单-%s\n
                         预订链接：%s\n
                         申请理由请查看排期下方留言\n
                         请于2个工作日内与申请审批的Leader联系，及时通过审核，超过时间没有审核的，系统会自动释放资源为未下单。\n
                         如不通过系统将自动将资源释放为申请前状态并提示理由。"""
                         % (change_state_apply.order.name, url)))
    send_simple_mail(u'【%s审批申请】%s-%s' % (change_state_apply.type_cn, change_state_apply.order.name, g.user.name),
                     recipients=change_state_apply.receiver,
                     body=(
                         u"""定单-%s\n
                         预订链接：%s\n
                         %s 申请下单，请求审批\n
                         申请理由请查看排期下方留言\n
                         请于2个工作日内核实通过审核，超过时间没有审核的，系统会自动释放资源为申请前状态。\n
                         如不通过请在留言框内注明理由，系统将自动将资源释放为申请前状态。"""
                         % (change_state_apply.order.name, url, g.user.name)))


def reply_apply(sender, change_state_apply):
    url = mail.app.config['DOMAIN'] + url_for(
        'order.order_detail', order_id=change_state_apply.order.id, step=change_state_apply.next_step)
    if change_state_apply.agree:
        send_simple_mail(u'【%s】%s-%s' % (change_state_apply.type_cn, change_state_apply.order.name, g.user.name),
                         recipients=change_state_apply.receiver,
                         body=(
                             u"""定单-%s\n
                             预订链接：%s\n
                             审核已通过。"""
                             % (change_state_apply.order.name, url)))
    else:
        send_simple_mail(u'【%s】%s-%s' % (change_state_apply.type_cn, change_state_apply.order.name, g.user.name),
                         recipients=change_state_apply.receiver,
                         body=(
                             u"""定单-%s\n
                             预订链接：%s\n
                             审核未通过，系统已将资源释放为申请前状态，请及时注意预订资源情况。
                             未通过理由请查看排期下方留言"""
                             % (change_state_apply.order.name, url)))


def contract_apply_douban(sender, apply_context):
    """豆瓣直签豆瓣、关联豆瓣订单 发送豆瓣合同管理员"""
    order = apply_context['order']
    file_paths = []
    if order.get_last_contract():
        file_paths.append(order.get_last_contract().real_path)
    if order.get_last_schedule():
        file_paths.append(order.get_last_schedule().real_path)

    send_attach_mail(u'【合同流程】%s-%s' % (order.name, apply_context['action_msg']),
                     recipients=apply_context['to'],
                     body=order.douban_contract_email_info(
                         title=u"请帮忙打印合同, 谢谢~"),
                     file_paths=file_paths)


def contract_apply(sender, apply_context, action=None):
    """合同流程 发送邮件"""
    order = apply_context['order']
    if order.__tablename__ == 'bra_douban_order' and order.contract_status == 4 and action == 5:
        contract_apply_douban(sender, apply_context)
    # elif order.__tablename__ == 'bra_client_order' and order.associated_douban_orders and order.contract_status == 4 and action == 5:
    #    apply_context['order'] = order.associated_douban_orders[0]
    #    contract_apply_douban(sender, apply_context)
    else:
        url = mail.app.config['DOMAIN'] + order.info_path()
        send_simple_mail(u'【合同流程】%s-%s' % (order.name, apply_context['action_msg']),
                         recipients=apply_context['to'],
                         body=(u"""%s

订单: %s
链接地址: %s
订单合同号: %s 
订单信息:
%s
留言如下:
    %s
\n
by %s
""" % (apply_context['action_msg'], order.name, url, order.contract, order.email_info, apply_context['msg'], g.user.name)))


def medium_invoice_apply(sender, apply_context):
    invoice = apply_context['invoice']
    order = invoice.client_order
    invoice_pays = apply_context['invoice_pays']
    invoice_info = u"发票信息: " + invoice.detail + u'; 发票金额: ' + \
        str(invoice.money) + u'; 发票号: ' + invoice.invoice_num + \
        u'; 未打款金额: ' + str(invoice.get_unpay_money)
    invoice_pay_info = "\n".join(
        [u'打款金额: ' + str(o.money) + u'; 打款时间: ' + o.pay_time_cn + u'; 留言信息: ' + o.detail for o in invoice_pays])
    if apply_context['send_type'] == "saler":
        url = mail.app.config[
            'DOMAIN'] + '/saler/client_order/medium_invoice/%s/invoice' % (invoice.id)
        name = u'黄亮'
    elif apply_context['send_type'] == "media":
        url = mail.app.config[
            'DOMAIN'] + '/saler/client_order/medium_invoice/%s/invoice' % (invoice.id)
        name = name = ', '.join(
            [k.name for k in User.medias() + User.media_leaders()])
    else:
        url = mail.app.config[
            'DOMAIN'] + '/finance/client_order/medium_pay/%s/info' % (invoice.client_order_id)
        name = ', '.join([k.name for k in User.finances()])
    text = u"""%s

Dear %s:

订单: %s
链接地址: %s
发票信息:
%s

打款信息:
%s

留言如下:
    %s
\n
by %s
""" % (apply_context['action_msg'], name, order.name, url, invoice_info, invoice_pay_info, apply_context['msg'], g.user.name)
    send_simple_mail(
        apply_context['title'], recipients=apply_context['to'], body=text)


def agent_invoice_apply(sender, apply_context):
    invoice = apply_context['invoice']
    order = invoice.client_order
    invoice_pays = apply_context['invoice_pays']
    invoice_info = u"发票信息: " + invoice.detail + u'; 发票金额: ' + \
        str(invoice.money) + u'; 发票号: ' + invoice.invoice_num + \
        u'; 未打款金额: ' + str(invoice.get_unpay_money)
    invoice_pay_info = "\n".join(
        [u'打款金额: ' + str(o.money) + u'; 打款时间: ' + o.pay_time_cn + u'; 留言信息: ' + o.detail for o in invoice_pays])
    if apply_context['send_type'] == "saler":
        if order.__tablename__ == 'searchAd_bra_client_order':
            url = mail.app.config[
                'DOMAIN'] + '/saler/searchAd_order/agent_invoice/%s/invoice' % (invoice.id)
            name = u'盖新'
        else:
            url = mail.app.config[
                'DOMAIN'] + '/saler/client_order/agent_invoice/%s/invoice' % (invoice.id)
            name = u'黄亮'
    else:
        if order.__tablename__ == 'searchAd_bra_client_order':
            url = mail.app.config[
                'DOMAIN'] + '/finance/searchAd_order/agent_pay/%s/info' % (invoice.client_order_id)
        else:
            url = mail.app.config[
                'DOMAIN'] + '/finance/client_order/agent_pay/%s/info' % (invoice.client_order_id)
        name = ', '.join([k.name for k in User.finances()])
    text = u"""%s

Dear %s:

订单: %s
链接地址: %s
发票信息:
%s

打款信息:
%s

留言如下:
    %s
\n
by %s
""" % (apply_context['action_msg'], name, order.name, url, invoice_info, invoice_pay_info, apply_context['msg'], g.user.name)
    send_simple_mail(
        apply_context['title'], recipients=apply_context['to'], body=text)


def invoice_apply(sender, apply_context):
    order = apply_context['order']
    invoices = apply_context['invoices']
    invoice_info = "\n".join(
        [u'发票信息: ' + o.detail + u'; 发票金额' + str(o.money) for o in invoices])
    url = mail.app.config['DOMAIN'] + apply_context['url']
    text = u"""%s
订单: %s
合同号: %s
合同金额: %s
链接地址: %s
发票信息:
%s
留言如下:
    %s
\n
by %s
""" % (apply_context['action_msg'], order.name, order.contract, order.money, url, invoice_info, apply_context['msg'], g.user.name)
    send_simple_mail(
        apply_context['title'], recipients=apply_context['to'], body=text)


def medium_rebate_invoice_apply(sender, apply_context):
    order = apply_context['order']
    invoices = apply_context['invoices']
    invoice_info = "\n".join(
        [u'发票信息: ' + o.detail + u'; 发票金额' + str(o.money) for o in invoices])
    url = mail.app.config['DOMAIN'] + apply_context['url']
    if apply_context['send_type'] == "saler":
        to_name = u'黄亮'
    else:
        to_name = u'财务'
    text = u"""
Dear: %s

    %s
订单: %s
合同号: %s
合同金额: %s
链接地址: %s
发票信息:
%s
留言如下:
    %s
\n
by %s
""" % (to_name, apply_context['action_msg'], order.name, order.contract, order.money, url, invoice_info, apply_context['msg'], g.user.name)
    send_simple_mail(
        apply_context['title'], recipients=apply_context['to'], body=text)


'''
def medium_invoice_apply(sender, apply_context):
    order = apply_context['order']
    invoices = apply_context['invoices']
    invoice_info = "\n".join(
        [u'发票信息: ' + o.detail + u'; 发票金额' + str(o.money) for o in invoices])
    if apply_context['send_type'] == "saler":
        url = mail.app.config['DOMAIN'] + order.saler_invoice_path()
    else:
        url = mail.app.config['DOMAIN'] + order.finance_invoice_path()
    text = u"""%s
订单: %s
链接地址: %s
发票信息:
%s
留言如下:
    %s
\n
by %s
""" % (apply_context['action_msg'], order.name, url, invoice_info, apply_context['msg'], g.user.name)
    send_simple_mail(apply_context['title'], recipients=apply_context['to'], body=text)
'''


def framework_douban_contract_apply(sender, apply_context):
    """框架订单豆瓣合同号申请"""
    order = apply_context['order']
    url = mail.app.config['DOMAIN'] + order.info_path()
    douban_users = User.douban_contracts()
    body = u"""
Dear %s:

请帮忙递交法务审核合同 + 分配合同号, 谢谢~

项目: 框架
代理集团: %s
直客销售: %s
渠道销售: %s
时间: %s : %s
金额: %s

附注:
    致趣订单管理系统链接地址: %s

by %s\n
""" % (','.join([x.name for x in douban_users]), order.group.name,
       order.direct_sales_names, order.agent_sales_names,
       order.start_date_cn, order.end_date_cn,
       order.money, url, g.user.name)
    file_paths = []
    # if order.get_last_contract():
    #    file_paths.append(order.get_last_contract().real_path)
    if order.get_last_schedule():
        file_paths.append(order.get_last_schedule().real_path)
    send_attach_mail(u'【合同流程】%s-%s' % (order.name, u'豆瓣合同号申请'),
                     recipients=apply_context['to'],
                     body=body,
                     file_paths=file_paths)


def douban_contract_apply(sender, apply_context):
    """豆瓣合同号申请"""
    order = apply_context['order']
    url = mail.app.config['DOMAIN'] + order.info_path()
    douban_users = User.douban_contracts()
    body = u"""
Dear %s:

请帮忙递交法务审核合同 + 分配合同号, 谢谢~

项目: %s
客户: %s
代理: %s
直客销售: %s
渠道销售: %s
时间: %s : %s
金额: %s

附注:
    致趣订单管理系统链接地址: %s

by %s\n
""" % (','.join([x.name for x in douban_users]), order.campaign,
       order.client.name, order.jiafang_name,
       order.direct_sales_names, order.agent_sales_names,
       order.start_date_cn, order.end_date_cn,
       order.money, url, g.user.name)
    file_paths = []
    if order.get_last_contract():
        file_paths.append(order.get_last_contract().real_path)
    if order.get_last_schedule():
        file_paths.append(order.get_last_schedule().real_path)
    send_attach_mail(u'【合同流程】%s-%s' % (order.name, u'豆瓣合同号申请'),
                     recipients=apply_context['to'],
                     body=body,
                     file_paths=file_paths)


def outsource_distribute(sender, apply_context):
    order = apply_context['order']
    title = u'【费用报备】%s-%s-订单分配提醒' % (order.contract or u'无合同号',
                                     order.jiafang_name)
    send_simple_mail(title, recipients=apply_context[
                     'to'], body=order.outsource_distribute_email_info(title))


def outsource_apply(sender, apply_context):
    """外包服务流程 发送邮件"""
    order = apply_context['order']
    outsources = apply_context['outsources']
    outsources_info = "\n".join([o.outsource_info for o in outsources])

    url = mail.app.config['DOMAIN'] + order.outsource_path()

    send_simple_mail(apply_context['title'], recipients=apply_context['to'],
                     body=order.outsource_email_info(apply_context['to_users'],
                                                     apply_context[
                                                         'title'], outsources_info,
                                                     url, apply_context['msg']))


def merger_outsource_apply(sender, apply_context):
    merger_outsource = apply_context['merger_outsource']
    outsources = merger_outsource.outsources
    outsources_info = "\n".join([o.outsource_info for o in outsources])
    pay_nums = merger_outsource.pay_num
    action = apply_context['action']
    if apply_context.has_key('url'):
        url = apply_context['url']
    else:
        url = mail.app.config['DOMAIN'] + outsources[0].finance_pay_path()
    if merger_outsource.invoice:
        invoice_type = u'有'
    else:
        invoice_type = u'无'
    to_user = apply_context['to']
    to_user_name = ''

    if action == 1:
        to_user_name = ','.join(
            [k.name for k in User.all() if k.email.find('huangliang') >= 0])
        to_user += [k.email for k in User.all() if k.email.find('huangliang')
                    >= 0 or k.email.find('fenghaiyan') >= 0] + [k.email for k in User.finances()]
        if merger_outsource.__tablename__ == 'merger_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_client_target_info', target_id=merger_outsource.target.id)
        elif merger_outsource.__tablename__ == 'merger_personal_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_client_target_personal_info')
        elif merger_outsource.__tablename__ == 'merger_douban_personal_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_douban_target_personal_info')
        else:
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_douban_target_info', target_id=merger_outsource.target.id)
        flash(u'已发送邮件给 %s ' % (', '.join(to_user)), 'info')
    elif action == -1:
        to_user_name = ','.join(
            [k.name for k in User.all() if k.email.find('fenghaiyan') >= 0])
        to_user += [k.email for k in User.all() if k.email.find('huangliang')
                    >= 0 or k.email.find('fenghaiyan') >= 0] + [k.email for k in User.finances()]
        if merger_outsource.__tablename__ == 'merger_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_client_target_info', target_id=merger_outsource.target.id)
        elif merger_outsource.__tablename__ == 'merger_personal_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_client_target_personal_info')
        elif merger_outsource.__tablename__ == 'merger_douban_personal_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_douban_target_personal_info')
        else:
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_douban_target_info', target_id=merger_outsource.target.id)
        flash(u'已发送邮件给 %s ' % (', '.join(to_user)), 'info')
    elif action == 2:
        to_user_name = ','.join([k.name for k in User.finances()])
        to_user += [k.email for k in User.all() if k.email.find('huangliang')
                    >= 0 or k.email.find('fenghaiyan') >= 0] + [k.email for k in User.finances()]
        if merger_outsource.__tablename__ == 'merger_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('finance_outsource_pay.info', target_id=merger_outsource.target.id)
        elif merger_outsource.__tablename__ == 'merger_personal_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('finance_outsource_pay.info', target_id=0)
        elif merger_outsource.__tablename__ == 'merger_douban_personal_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('finance_outsource_pay.douban_info', target_id=0)
        else:
            url = mail.app.config[
                'DOMAIN'] + url_for('finance_outsource_pay.douban_info', target_id=merger_outsource.target.id)
        flash(u'已发送邮件给 %s ' % (', '.join(to_user)), 'info')
    elif action == 0:
        to_user_name = ','.join(
            [k.name for k in User.all() if k.email.find('fenghaiyan') >= 0])
        to_user += [k.email for k in User.all() if k.email.find('huangliang')
                    >= 0 or k.email.find('fenghaiyan') >= 0] + [k.email for k in User.finances()]
        if merger_outsource.__tablename__ == 'merger_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_client_target_info', target_id=merger_outsource.target.id)
        elif merger_outsource.__tablename__ == 'merger_personal_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_client_target_personal_info')
        elif merger_outsource.__tablename__ == 'merger_douban_personal_out_source':
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_douban_target_personal_info')
        else:
            url = mail.app.config[
                'DOMAIN'] + url_for('outsource.merget_douban_target_info', target_id=merger_outsource.target.id)
        flash(u'已发送邮件给 %s ' % (', '.join(to_user)), 'info')

    body = u"""
Dear %s:

%s

【外包组成】
%s

申请付款总金额: %s
是否有发票:%s
发票信息:%s

留言:
%s


附注:
    致趣订单管理系统链接地址: %s

by %s\n
""" % (to_user_name, apply_context['title'], outsources_info, pay_nums, invoice_type, merger_outsource.remark, apply_context['msg'], url, g.user.name)
    send_simple_mail(apply_context['title'], recipients=list(set(to_user)),
                     body=body)


def apply_leave(sender, leave):
    status = leave.status
    if status in [0, 2]:
        if leave.is_long_leave():
            to_name = u'黄亮'
        else:
            to_name = ','.join([k.name for k in leave.creator.team_leaders])
        url = mail.app.config['DOMAIN'] + \
            url_for('account_leave.info', lid=leave.id)
    elif status in [3, 4]:
        to_name = leave.creator.name
        url = mail.app.config['DOMAIN'] + \
            url_for('account_leave.index', user_id=leave.creator.id)
    to_users = leave.senders + leave.creator.team_leaders + \
        [leave.creator] + [g.user]
    to_emails = list(set([k.email for k in to_users])) + ['admin@inad.com']
    if leave.is_long_leave():
        to_emails += ['huangliang@inad.com']
    body = u"""
Dear %s:

申请状态: %s

请假人: %s
请假日期: %s - %s，共%s
请假类型: %s
请假原因: 
%s

请批准，谢谢

by %s

附注: 
    请假申请链接地址: %s

""" % (to_name, leave.status_cn, leave.creator.name, leave.start_time_cn, leave.end_time_cn,
       leave.rate_day_cn, leave.type_cn, leave.reason, g.user.name, url)

    send_simple_mail(u'【请假申请】- %s' %
                     (leave.creator.name), recipients=to_emails, body=body)


def kpi_apply(sender, apply_context):
    report = apply_context['report']
    if report.status == 2:
        url = mail.app.config['DOMAIN'] + \
            url_for('account_kpi.check_apply', r_id=report.id)
        to_names = ','.join([k.name for k in report.creator.team_leaders])
        user_name = report.creator.name
        to_users = [k.email for k in report.creator.team_leaders] + \
            [report.creator.email]
        title = u'绩效考核申请审批'
        body = u"""
Dear %s:

请您为 %s 的绩效考核打分。

附注: 
    KPI链接地址: %s

    """ % (to_names, user_name, url)
    elif report.status == 1:
        url = mail.app.config['DOMAIN'] + \
            url_for('account_kpi.update', r_id=report.id)
        to_names = report.creator.name
        user_name = report.creator.name
        to_users = [k.email for k in report.creator.team_leaders] + \
            [report.creator.email]
        title = u'绩效考核被打回'
        body = u"""
Dear %s:

您的绩效考核被打回请重新修改后提交领导审批。

附注: 
    KPI链接地址: %s

    """ % (to_names, url)
    elif report.status == 4:
        url = mail.app.config['DOMAIN'] + \
            url_for('account_kpi.info', r_id=report.id)
        to_names = ','.join([k.name for k in User.HR_leaders()])
        user_name = report.creator.name
        to_users = [k.email for k in User.HR_leaders(
        )] + [report.creator.email] + [k.email for k in report.creator.team_leaders]
        title = u'绩效考核申请归档'
        body = u"""
Dear %s:

%s 的绩效已提交给您，请查看并归档。

附注: 
    KPI链接地址: %s

    """ % (to_names, user_name, url)
    elif report.status == 5:
        url = mail.app.config['DOMAIN'] + \
            url_for('account_kpi.info', r_id=report.id)
        to_names = report.creator.name
        user_name = report.creator.name
        to_users = [k.email for k in User.HR_leaders(
        )] + [report.creator.email] + [k.email for k in report.creator.team_leaders]
        title = u'绩效考核已归档'
        body = u"""
Dear %s:

您的绩效已归档，请通过下边链接查看评分。

附注: 
    KPI链接地址: %s

    """ % (to_names, url)

    send_simple_mail(title, list(set(to_users)), body=body)


def back_money_apply(sender, apply_context):
    order = apply_context['order']
    num = apply_context['num']
    type = apply_context['type']
    if type == 'invoice':
        s_title = u'返点发票信息'
    elif type == 'end':
        s_title = u'回款完成'
    elif type == 'no_end':
        s_title = u'回款状态变为未完成'
    else:
        s_title = u'回款信息'
    if order.__tablename__ in ['searchAd_bra_client_order', 'searchAd_bra_rebate_order']:
        to_users = order.direct_sales + order.agent_sales +\
            [order.creator, g.user] + order.leaders
        title = u'【搜索部门-项目回款】%s-%s' % (order.name, s_title)
    else:
        to_users = order.direct_sales + order.agent_sales + User.contracts() +\
            [order.creator, g.user] + order.leaders + User.medias()
        if 3 in order.locations:
            to_users += [k for k in User.all() if k.email.find('chenjingjing') >= 0]
        title = u'【项目回款】%s-%s' % (order.name, s_title)
    to_emails = list(set([x.email for x in to_users]))
    flash(u'已发送邮件给 %s ' %
          (', '.join([k.name for k in list(set(to_users))])), 'info')
    
    url = mail.app.config['DOMAIN'] + order.info_path()
    
    body = u"""
订单: %s
链接地址: %s
订单合同号: %s 

回款详情:
   本次回款金额: %s
   已回款完成比例: %s %%

订单信息:
%s

\n
by %s
""" % (order.name, url, order.contract, str(num), order.back_money_percent, order.email_info, g.user.name)
    send_simple_mail(title, to_emails, body=body)


def out_apply(sender, out, status):
    if status == 1:
        msg = u'外出报备申请'
        to_name = ','.join([k.name for k in out.creator.team_leaders])
    elif status == 10:
        msg = u'外出报备撤销'
        to_name = ','.join([k.name for k in out.creator.team_leaders])
    elif status == 11:
        msg = u'外出报备被驳回'
        to_name = out.creator.name
    elif status == 2:
        msg = u'外出报备申请通过'
        to_name = out.creator.name
    elif status in [3, 4]:
        msg = u'会议纪要填写完成'
        to_name = ','.join([k.name for k in out.creator.team_leaders])
    elif status == 13:
        msg = u'外出报备未审批-会议纪要填写完成'
        to_name = ','.join([k.name for k in out.creator.team_leaders])
    elif status == 14:
        msg = u'外出报备申请通过-并完成会议纪要'
        to_name = out.creator.name
    title = u'【外出报备】' + '-' + out.m_persion_cn +'-' +out.creator.name
    url = mail.app.config['DOMAIN'] + url_for('account_out.info', oid=out.id)
    body = u"""
Dear %s: 

%s

报备人：%s
开始时间：%s
结束时间：%s
公司名称：%s
会见人：  %s
地址：   %s
参会人（公司内部）：%s
外出原因：
%s
会议纪要：
%s

附注: 
    外出报备链接地址: %s

    """ % (to_name, msg, out.creator.name, out.start_time_cn, out.end_time_cn, out.m_persion_cn,
           out.persions, out.address, ','.join([k.name for k in out.joiners]),
           out.reason, out.meeting_s, url)
    to_users = out.creator.team_leaders + [g.user] + out.joiners
    joiners_leaders = []
    for k in out.joiners:
        joiners_leaders += k.team_leaders
    to_users += joiners_leaders
    if out.creator_type == 1:
        to_user_emails = [k.email for k in to_users] + ['admin@inad.com']
        if out.status in [3, 4]:
            title = u'【外出报备】-会议纪要'
            to_user_emails = [k.email for k in to_users] + ['sales@inad.com']
    else:
        to_user_emails = [k.email for k in to_users] + ['admin@inad.com']
        if out.status == 3:
            to_user_emails = [k.email for k in to_users]
    if out.creator.team.location == 2:
        to_user_emails += ['salessh@inad.com']
    if out.creator.team.location == 1 and out.creator.team.type in [3, 4, 9]:
        to_user_emails += ['huawei@inad.com']

    # 会议纪要申请通过只抄送相关人+admin,不抄送leader
    if out.status == 2:
        to_users = [g.user] + out.joiners
        to_user_emails = [k.email for k in to_users] + ['admin@inad.com']
    # 会议纪要发送邮件标题改为"【外出报备】-会议纪要"
    if out.status in [3, 4]:
        title = u'【外出报备】-会议纪要' + '-' + out.m_persion_cn +'-' +out.creator.name
    flash(u'已发送邮件给 %s ' % (', '.join([k.name for k in to_users])), 'info')
    send_simple_mail(title, list(set(to_user_emails)), body=body)


def planning_bref(sender, apply_context):
    bref = apply_context['bref']
    action = apply_context['status']
    # 获取某区域策划负责人
    c_loction = bref.creator.location
    planning_team_admins = [k for k in User.all_active(
    ) if k.location == c_loction and k.team.type == 6][0].team.admins
    # 获取某区域销售负责人
    sale_admins = bref.creator.team.admins
    # 获取某区域执行负责人
    operater_admins = [k for k in User.all_active(
    ) if k.location == c_loction and k.team.type == 15]
    if action == 2:
        title = u'【策划单】-%s' % (bref.title)
        to_name = ','.join([k.name for k in planning_team_admins])
        status_cn = u'下单申请'
    elif action == 10:
        title = u'【策划单】-%s' % (bref.title)
        status_cn = u'已取消'
        to_name = bref.creator.name
    elif action == 1:
        title = u'【策划单】-%s' % (bref.title)
        status_cn = u'已打回'
        to_name = bref.creator.name
    elif action == 3:
        title = u'【策划单】-%s' % (bref.title)
        status_cn = u'已分配'
        to_name = bref.creator.name + ',' + bref.toer.name
    elif action == 0:
        title = u'【策划单】-%s' % (bref.title)
        status_cn = u'已完成'
        to_name = bref.creator.name
    url = mail.app.config['DOMAIN'] + \
        url_for('planning_bref.info', bid=bref.id)
    # 邮件发送人
    to_emails = apply_context['to']
    to_emails += [u.email for u in operater_admins +
                  planning_team_admins + [bref.creator] + bref.creator.team_leaders]
    flash(u'已发送邮件给:' + ','.join(to_emails), 'info')
    if action in [0, 3]:
        finish_text = u"""
完成情况
分配给 %s
分配人 %s
策划单地址   %s
        """ % (bref.toer.name, bref.follower.name, bref.url)
    else:
        finish_text = ''

    body = u"""
Dear %s: 

%s-%s
%s
基本信息:
名称  %s
代理/直客   %s
品牌  %s
产品  %s
目标受众    %s
背景  %s
推广目的    %s
推广主题    %s
推广周期    %s
推广预算    %s
是否有模板   %s

项目说明:
下单需求方   %s
应用场景    %s
应用等级    %s
完成时间    %s

补充说明:
品牌意向媒体  %s
建议  %s
备注  
%s


留言信息:
%s

附注: 
    策划单链接地址: %s

    """ % (to_name, title, status_cn, finish_text, bref.title, bref.agent, bref.brand, bref.product, bref.target, bref.background,
           bref.push_target, bref.push_theme, bref.push_time, bref.budget_cn, bref.is_temp_cn, bref.agent_type_cn,
           bref.use_type_cn, bref.level_cn, bref.get_time_cn, bref.intent_medium, bref.suggest, bref.desc,
           apply_context['msg'], url)
    send_simple_mail(title, list(set(to_emails)), body=body)


def init_signal(app):
    """注册信号的接收器"""
    password_changed_signal.connect_via(app)(password_changed)
    add_comment_signal.connect_via(app)(add_comment)
    order_apply_signal.connect_via(app)(order_apply)
    reply_apply_signal.connect_via(app)(reply_apply_signal)
    contract_apply_signal.connect_via(app)(contract_apply)
    douban_contract_apply_signal.connect_via(app)(douban_contract_apply)
    framework_douban_contract_apply_signal.connect_via(
        app)(framework_douban_contract_apply)
    outsource_apply_signal.connect_via(app)(outsource_apply)
    invoice_apply_signal.connect_via(app)(invoice_apply)
    medium_rebate_invoice_apply_signal.connect_via(app)(medium_rebate_invoice_apply)
    medium_invoice_apply_signal.connect_via(app)(medium_invoice_apply)
    agent_invoice_apply_signal.connect_via(app)(agent_invoice_apply)
    outsource_distribute_signal.connect_via(app)(outsource_distribute)
    merger_outsource_apply_signal.connect_via(app)(merger_outsource_apply)
    apply_leave_signal.connect_via(app)(apply_leave)
    kpi_apply_signal.connect_via(app)(kpi_apply)
    apply_out_signal.connect_via(app)(out_apply)
    back_money_apply_signal.connect_via(app)(back_money_apply)
    planning_bref_signal.connect_via(app)(planning_bref)
