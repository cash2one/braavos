# -*- coding: UTF-8 -*-
import datetime
from flask import url_for

from . import db, BaseModelMixin
from models.mixin.comment import CommentMixin
from models.mixin.attachment import AttachmentMixin
from models.attachment import ATTACHMENT_STATUS_PASSED, ATTACHMENT_STATUS_REJECT
from .item import ITEM_STATUS_LEADER_ACTIONS
from .user import User, TEAM_LOCATION_CN
from consts import DATE_FORMAT
from invoice import Invoice, MediumInvoice


CONTRACT_TYPE_NORMAL = 0
CONTRACT_TYPE_SPECIAL = 1
CONTRACT_TYPE_CN = {
    CONTRACT_TYPE_NORMAL: u"标准",
    CONTRACT_TYPE_SPECIAL: u"非标"
}

SALE_TYPE_AGENT = 0
SALE_TYPE_DIRECT = 1
SALE_TYPE_CN = {
    SALE_TYPE_AGENT: u"代理",
    SALE_TYPE_DIRECT: u"直客",
}

RESOURCE_TYPE_AD = 0
RESOURCE_TYPE_CAMPAIGN = 1
RESOURCE_TYPE_FRAME = 2
RESOURCE_TYPE_OTHER = 4
RESOURCE_TYPE_CN = {
    RESOURCE_TYPE_AD: u"硬广",
    RESOURCE_TYPE_CAMPAIGN: u"互动",
    # RESOURCE_TYPE_FRAME: u"框架",
    RESOURCE_TYPE_OTHER: u"其他"
}

CONTRACT_STATUS_NEW = 0
CONTRACT_STATUS_APPLYCONTRACT = 1
CONTRACT_STATUS_APPLYPASS = 2
CONTRACT_STATUS_APPLYREJECT = 3
CONTRACT_STATUS_APPLYPRINT = 4
CONTRACT_STATUS_PRINTED = 5
CONTRACT_STATUS_MEDIA = 6
CONTRACT_STATUS_CN = {
    CONTRACT_STATUS_NEW: u"新建",
    CONTRACT_STATUS_APPLYCONTRACT: u"申请审批中...",
    CONTRACT_STATUS_APPLYPASS: u"审批通过",
    CONTRACT_STATUS_APPLYREJECT: u"审批未通过",
    CONTRACT_STATUS_MEDIA: u"利润分配中...",
    CONTRACT_STATUS_APPLYPRINT: u"申请打印中...",
    CONTRACT_STATUS_PRINTED: u"打印完毕"
}

STATUS_DEL = 0
STATUS_ON = 1
STATUS_CN = {
    STATUS_DEL: u'删除',
    STATUS_ON: u'正常',
}

ECPM_CONTRACT_STATUS_LIST = [2, 4, 5]

direct_sales = db.Table('client_order_direct_sales',
                        db.Column('sale_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('client_order_id', db.Integer, db.ForeignKey('bra_client_order.id'))
                        )
agent_sales = db.Table('client_order_agent_sales',
                       db.Column('agent_sale_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('client_order_id', db.Integer, db.ForeignKey('bra_client_order.id'))
                       )
table_medium_orders = db.Table('client_order_medium_orders',
                               db.Column('order_id', db.Integer, db.ForeignKey('bra_order.id')),
                               db.Column('client_order_id', db.Integer, db.ForeignKey('bra_client_order.id'))
                               )


class ClientOrder(db.Model, BaseModelMixin, CommentMixin, AttachmentMixin):
    __tablename__ = 'bra_client_order'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))  # 客户合同甲方
    agent = db.relationship('Agent', backref=db.backref('client_orders', lazy='dynamic'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))  # 客户
    client = db.relationship('Client', backref=db.backref('client_orders', lazy='dynamic'))
    campaign = db.Column(db.String(100))  # 活动名称

    contract = db.Column(db.String(100))  # 客户合同号
    money = db.Column(db.Integer)  # 客户合同金额
    contract_type = db.Column(db.Integer)  # 合同类型： 标准，非标准
    client_start = db.Column(db.Date)
    client_end = db.Column(db.Date)
    reminde_date = db.Column(db.Date)  # 最迟回款日期
    resource_type = db.Column(db.Integer)  # 资源形式
    sale_type = db.Column(db.Integer)  # 资源形式

    direct_sales = db.relationship('User', secondary=direct_sales)
    agent_sales = db.relationship('User', secondary=agent_sales)

    medium_orders = db.relationship('Order', secondary=table_medium_orders)
    contract_status = db.Column(db.Integer)  # 合同审批状态
    status = db.Column(db.Integer)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref=db.backref('created_client_orders', lazy='dynamic'))
    create_time = db.Column(db.DateTime)

    contract_generate = True
    media_apply = True
    kind = "client-order"

    def __init__(self, agent, client, campaign, medium_orders=None, status=STATUS_ON,
                 contract="", money=0, contract_type=CONTRACT_TYPE_NORMAL, sale_type=SALE_TYPE_AGENT,
                 client_start=None, client_end=None, reminde_date=None, resource_type=RESOURCE_TYPE_AD,
                 direct_sales=None, agent_sales=None,
                 creator=None, create_time=None, contract_status=CONTRACT_STATUS_NEW):
        self.agent = agent
        self.client = client
        self.campaign = campaign
        self.medium_orders = medium_orders or []

        self.contract = contract
        self.money = money
        self.contract_type = contract_type
        self.sale_type = sale_type

        self.client_start = client_start or datetime.date.today()
        self.client_end = client_end or datetime.date.today()
        self.reminde_date = reminde_date or datetime.date.today()
        self.resource_type = resource_type

        self.direct_sales = direct_sales or []
        self.agent_sales = agent_sales or []

        self.creator = creator
        self.status = status
        self.create_time = create_time or datetime.datetime.now()
        self.contract_status = contract_status

    @classmethod
    def get_all(cls):
        """查看所有没删除订单"""
        return [o for o in cls.all() if o.status in [STATUS_ON, None]]

    @property
    def name(self):
        return u"%s-%s" % (self.client.name, self.campaign)

    @property
    def mediums(self):
        return [x.medium for x in self.medium_orders]

    @property
    def mediums_money2(self):
        return sum([x.medium_money2 for x in self.medium_orders])

    @property
    def mediums_invoice_pass_sum(self):
        return sum([k.pay_money for k in MediumInvoice.query.filter_by(client_order_id=self.id)
                   if k.invoice_status == 0])

    @property
    def mediums_invoice_apply_sum(self):
        return sum([k.pay_money for k in MediumInvoice.query.filter_by(client_order_id=self.id)
                   if k.invoice_status == 2])

    @property
    def medium_ids(self):
        return [x.medium.id for x in self.medium_orders]

    @property
    def outsources(self):
        return [o for mo in self.medium_orders for o in mo.outsources]

    def get_outsources_by_status(self, outsource_status):
        return [o for o in self.outsources if o.status == outsource_status]

    def get_outsource_status_cn(self, status):
        from models.outsource import OUTSOURCE_STATUS_CN
        return OUTSOURCE_STATUS_CN[status]

    @property
    def outsources_sum(self):
        return sum([o.pay_num if o.pay_num else o.num for o in self.outsources]) if self.outsources else 0

    @property
    def outsources_percent(self):
        return "%.1f" % (self.outsources_sum * 100 / float(self.money)) if self.money else "0"

    @property
    def invoice_apply_sum(self):
        return sum([k.money for k in Invoice.query.filter_by(client_order_id=self.id)
                   if k.invoice_status == 3])

    @property
    def invoice_pass_sum(self):
        return sum([k.money for k in Invoice.query.filter_by(client_order_id=self.id)
                   if k.invoice_status == 0])

    @property
    def invoice_percent(self):
        return "%.1f" % (self.invoice_pass_sum * 100 / float(self.money)) if self.money else "0"

    @property
    def locations(self):
        return list(set([u.location for u in self.direct_sales + self.agent_sales]))

    @property
    def locations_cn(self):
        return ",".join([TEAM_LOCATION_CN[l] for l in self.locations])

    @property
    def associated_douban_orders(self):
        return [ao for mo in self.medium_orders for ao in mo.associated_douban_orders]

    @property
    def contract_type_cn(self):
        return CONTRACT_TYPE_CN[self.contract_type]

    @property
    def resource_type_cn(self):
        return RESOURCE_TYPE_CN.get(self.resource_type)

    @property
    def sale_type_cn(self):
        return SALE_TYPE_CN.get(self.sale_type)

    @property
    def direct_sales_names(self):
        return ",".join([u.name for u in self.direct_sales])

    @property
    def agent_sales_names(self):
        return ",".join([u.name for u in self.agent_sales])

    @property
    def leaders(self):
        return list(set([l for u in self.direct_sales + self.agent_sales
                         for l in u.user_leaders] + User.super_leaders()))

    def can_admin(self, user):
        """是否可以修改该订单"""
        admin_users = self.direct_sales + self.agent_sales + [self.creator]
        return user.is_media() or user in admin_users

    def can_action(self, user, action):
        """是否拥有leader操作"""
        if action in ITEM_STATUS_LEADER_ACTIONS:
            return user.is_admin() or user.is_leader()
        else:
            return self.can_admin(user)

    def have_owner(self, user):
        """是否可以查看该订单"""
        owner = self.direct_sales + self.agent_sales + [self.creator]
        return user.is_admin() or user in owner

    @classmethod
    def get_order_by_user(cls, user):
        """一个用户可以查看的所有订单"""
        return [o for o in cls.all() if o.have_owner(user) and o.status in [STATUS_ON, None]]

    def get_invoice_by_status(self, type):
        return [invoice for invoice in self.invoices if invoice.invoice_status == type]

    def get_medium_invoice_by_status(self, type):
        return [invoice for invoice in self.mediuminvoices if invoice.invoice_status == type]

    def path(self):
        return self.info_path()

    @property
    def search_info(self):
        return (self.client.name + self.agent.name +
                self.campaign + self.contract +
                "".join([mo.medium.name + mo.medium_contract for mo in self.medium_orders]) +
                "".join([ado.contract for ado in self.associated_douban_orders]))

    @property
    def email_info(self):
        return u"""
    类型:新媒体订单
    客户订单:

        客户: %s
        代理/直客: %s
        Campaign: %s
        金额: %s
        直客销售: %s
        渠道销售: %s

    媒体订单:
%s
    豆瓣订单:
%s""" % (self.client.name, self.agent.name, self.campaign, self.money,
         self.direct_sales_names, self.agent_sales_names,
         "\n".join([o.email_info for o in self.medium_orders]),
         "\n".join([o.email_info for o in self.associated_douban_orders]))

    @property
    def outsource_info(self):
        return u"""
        客户订单总额:   %s 元
        外包应付总金额: %s 元
        外包占比:   %s %%""" % (self.money, self.outsources_sum, self.outsources_percent)

    @property
    def start_date(self):
        return self.client_start

    @property
    def end_date(self):
        return self.client_end

    @property
    def start_date_cn(self):
        return self.start_date.strftime(DATE_FORMAT)

    @property
    def end_date_cn(self):
        return self.end_date.strftime(DATE_FORMAT)

    @property
    def reminde_date_cn(self):
        return self.reminde_date.strftime(DATE_FORMAT)

    @property
    def contract_status_cn(self):
        return CONTRACT_STATUS_CN[self.contract_status]

    def attachment_path(self):
        return url_for('files.client_order_files', order_id=self.id)

    def info_path(self):
        return url_for("order.order_info", order_id=self.id, tab_id=1)

    def contract_path(self):
        return url_for("order.client_order_contract", order_id=self.id)

    def outsource_path(self):
        return url_for("outsource.client_outsources", order_id=self.id)

    def finance_outsource_path(self):
        return url_for("finance_pay.info", order_id=self.id)

    def saler_invoice_path(self):
        return url_for("saler_invoice.index", order_id=self.id)

    def finance_invoice_path(self):
        return url_for("finance_invoice.info", order_id=self.id)

    def attach_status_confirm_path(self, attachment):
        return url_for('order.client_attach_status',
                       order_id=self.id,
                       attachment_id=attachment.id,
                       status=ATTACHMENT_STATUS_PASSED)

    def attach_status_reject_path(self, attachment):
        return url_for('order.client_attach_status',
                       order_id=self.id,
                       attachment_id=attachment.id,
                       status=ATTACHMENT_STATUS_REJECT)

    @classmethod
    def contract_exist(cls, contract):
        is_exist = cls.query.filter_by(contract=contract).count() > 0
        return is_exist

    def get_default_contract(self):
        return contract_generator(self.agent.current_framework, self.id)

    def delete(self):
        self.delete_comments()
        self.delete_attachments()
        for mo in self.medium_orders:
            mo.delete()
        db.session.delete(self)
        db.session.commit()


def contract_generator(framework, num):
    code = "%s-%03x" % (framework, num % 1000)
    code = code.upper()
    return code
