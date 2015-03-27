# -*- coding: UTF-8 -*-
from flask import Blueprint, request, current_app as app, abort, g, render_template as tpl
from flask import jsonify, send_from_directory, redirect, flash

from models.order import Order
from models.client_order import ClientOrder, CONTRACT_STATUS_NEW, CONTRACT_STATUS_APPLYREJECT
from models.framework_order import FrameworkOrder
from models.douban_order import DoubanOrder
from models.associated_douban_order import AssociatedDoubanOrder
# from models.user import User
from libs.files import files_set, attachment_set
# from libs.signals import contract_apply_signal


files_bp = Blueprint('files', __name__, template_folder='../templates/files')

FILE_TYPE_CONTRACT = 0
FILE_TYPE_SCHEDULE = 1


@files_bp.route('/files/<filename>', methods=['GET'])
def files(filename):
    config = app.upload_set_config.get('files')
    if config is None:
        abort(404)
    return send_from_directory(config.destination, filename.encode('utf-8'))


@files_bp.route('/attachment/<filename>', methods=['GET'])
def attachment(filename):
    config = app.upload_set_config.get('attachment')
    if config is None:
        abort(404)
    return send_from_directory(config.destination, filename.encode('utf-8'))


@files_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        filename = files_set.save(request.files['file'])
        return jsonify({'status': 0, 'filename': filename})
    return jsonify({'status': 1, 'msg': 'file not exits or type not allowed'})


def attachment_upload(order, file_type=FILE_TYPE_CONTRACT):
    if order and 'file' in request.files:
        filename = attachment_set.save(request.files['file'])
        if file_type == FILE_TYPE_CONTRACT:
            attachment = order.add_contract_attachment(g.user, filename)
            flash(u'合同文件上传成功!', 'success')
        elif file_type == FILE_TYPE_SCHEDULE:
            attachment = order.add_schedule_attachment(g.user, filename)
            flash(u'排期文件上传成功!', 'success')
        if order.contract_status not in [CONTRACT_STATUS_NEW, CONTRACT_STATUS_APPLYREJECT]:
            contract_email(order, attachment)
    else:
        flash(u'订单不存在，或文件上传出错!', 'danger')
    return redirect("%s#attachment-%s-%s" % (order.info_path(), order.kind, order.id))


@files_bp.route('/client/contract/upload', methods=['POST'])
def client_contract_upload():
    order_id = request.values.get('order')
    order = ClientOrder.get(order_id)
    return attachment_upload(order, FILE_TYPE_CONTRACT)


@files_bp.route('/client/schedule/upload', methods=['POST'])
def client_schedule_upload():
    order_id = request.values.get('order')
    order = ClientOrder.get(order_id)
    return attachment_upload(order, FILE_TYPE_SCHEDULE)


@files_bp.route('/medium/contract/upload', methods=['POST'])
def medium_contract_upload():
    order_id = request.values.get('order')
    order = Order.get(order_id)
    return attachment_upload(order, FILE_TYPE_CONTRACT)


@files_bp.route('/medium/schedule/upload', methods=['POST'])
def medium_schedule_upload():
    order_id = request.values.get('order')
    order = Order.get(order_id)
    return attachment_upload(order, FILE_TYPE_SCHEDULE)


@files_bp.route('/framework/contract/upload', methods=['POST'])
def framework_contract_upload():
    order_id = request.values.get('order')
    order = FrameworkOrder.get(order_id)
    return attachment_upload(order, FILE_TYPE_CONTRACT)


@files_bp.route('/framework/schedule/upload', methods=['POST'])
def framework_schedule_upload():
    order_id = request.values.get('order')
    order = FrameworkOrder.get(order_id)
    return attachment_upload(order, FILE_TYPE_SCHEDULE)


@files_bp.route('/douban/contract/upload', methods=['POST'])
def douban_contract_upload():
    order_id = request.values.get('order')
    order = DoubanOrder.get(order_id)
    return attachment_upload(order, FILE_TYPE_CONTRACT)


@files_bp.route('/douban/schedule/upload', methods=['POST'])
def douban_schedule_upload():
    order_id = request.values.get('order')
    order = DoubanOrder.get(order_id)
    return attachment_upload(order, FILE_TYPE_SCHEDULE)


@files_bp.route('/associated_douban/contract/upload', methods=['POST'])
def associated_douban_contract_upload():
    order_id = request.values.get('order')
    order = AssociatedDoubanOrder.get(order_id)
    return attachment_upload(order, FILE_TYPE_CONTRACT)


@files_bp.route('/associated_douban/schedule/upload', methods=['POST'])
def associated_douban_schedule_upload():
    order_id = request.values.get('order')
    order = AssociatedDoubanOrder.get(order_id)
    return attachment_upload(order, FILE_TYPE_SCHEDULE)


@files_bp.route('/client_order/<order_id>/all_files', methods=['get'])
def client_order_files(order_id):
    co = ClientOrder.get(order_id)
    return tpl("order_files.html", order=co)


@files_bp.route('/medium_order/<order_id>/all_files', methods=['get'])
def medium_order_files(order_id):
    co = Order.get(order_id)
    return tpl("order_files.html", order=co)


@files_bp.route('/framework_order/<order_id>/all_files', methods=['get'])
def framework_order_files(order_id):
    fo = FrameworkOrder.get(order_id)
    return tpl("order_files.html", order=fo)


@files_bp.route('/douban_order/<order_id>/all_files', methods=['get'])
def douban_order_files(order_id):
    fo = DoubanOrder.get(order_id)
    return tpl("order_files.html", order=fo)


@files_bp.route('/associated_douban_order/<order_id>/all_files', methods=['get'])
def associated_douban_order_files(order_id):
    fo = AssociatedDoubanOrder.get(order_id)
    return tpl("order_files.html", order=fo)


def contract_email(order, attachment):
    '''
    contract_emails = [m.email for m in set(User.contracts() +
                                            order.direct_sales +
                                            order.agent_sales +
                                            [order.creator, g.user])]
    action_msg = u"新上传%s文件:%s" % (attachment.type_cn, attachment.filename)
    msg = u"""
    文件名:%s
    状态:%s
    上传者:%s""" % (attachment.filename, attachment.status_cn, g.user.name)
    apply_context = {"sender": g.user,
                     "to": contract_emails,
                     "action_msg": action_msg,
                     "msg": msg,
                     "order": order}
    contract_apply_signal.send(app._get_current_object(), apply_context=apply_context)
    flash(u'已发送提醒邮件给 %s' % ', '.join(contract_emails), "info")
    '''
