# -*- coding: UTF-8 -*-
import datetime
from flask import url_for

from . import db, BaseModelMixin
from .user import User, TEAM_LOCATION_CN
from models.mixin.comment import CommentMixin
from models.mixin.attachment import AttachmentMixin
from models.attachment import ATTACHMENT_STATUS_PASSED, ATTACHMENT_STATUS_REJECT
from consts import DATE_FORMAT


CONTRACT_TYPE_NORMAL = 0
CONTRACT_TYPE_SPECIAL = 1
CONTRACT_TYPE_CN = {
    CONTRACT_TYPE_NORMAL: u"标准",
    CONTRACT_TYPE_SPECIAL: u"非标"
}

CONTRACT_STATUS_NEW = 0
CONTRACT_STATUS_APPLYCONTRACT = 1
CONTRACT_STATUS_APPLYPASS = 2
CONTRACT_STATUS_APPLYREJECT = 3
CONTRACT_STATUS_APPLYPRINT = 4
CONTRACT_STATUS_PRINTED = 5

CONTRACT_STATUS_DELETEAPPLY = 7
CONTRACT_STATUS_DELETEAGREE = 8
CONTRACT_STATUS_DELETEFINANCE = 81
CONTRACT_STATUS_DELETEPASS = 9
CONTRACT_STATUS_CHECKCONTRACT = 10
CONTRACT_STATUS_PRE_FINISH = 19
CONTRACT_STATUS_FINISH = 20
CONTRACT_STATUS_CN = {
    CONTRACT_STATUS_NEW: u"新建",
    CONTRACT_STATUS_APPLYCONTRACT: u"申请合同号中...",
    CONTRACT_STATUS_APPLYPASS: u"审批通过，等待合同审批结果",
    CONTRACT_STATUS_APPLYREJECT: u"审批未通过",
    CONTRACT_STATUS_APPLYPRINT: u"申请打印中...",
    CONTRACT_STATUS_PRINTED: u"打印完毕",
    CONTRACT_STATUS_DELETEAPPLY: u'撤单申请中...',
    CONTRACT_STATUS_DELETEAGREE: u'确认撤单',
    CONTRACT_STATUS_DELETEFINANCE: u'财务确认撤单',
    CONTRACT_STATUS_DELETEPASS: u'同意撤单',
    CONTRACT_STATUS_PRE_FINISH: u'项目归档（预）',
    CONTRACT_STATUS_FINISH: u'项目归档（确认）',
    CONTRACT_STATUS_CHECKCONTRACT: u'审批合同通过'
}

STATUS_DEL = 0
STATUS_ON = 1
STATUS_CN = {
    STATUS_DEL: u'删除',
    STATUS_ON: u'正常',
}


direct_sales = db.Table('framework_order_direct_sales',
                        db.Column(
                            'sale_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column(
                            'client_order_id', db.Integer, db.ForeignKey('bra_framework_order.id'))
                        )
agent_sales = db.Table('framework_order_agent_sales',
                       db.Column(
                           'agent_sale_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column(
                           'client_order_id', db.Integer, db.ForeignKey('bra_framework_order.id'))
                       )
assistant_sales = db.Table('framework_order_assistant_sales',
                           db.Column(
                               'assistant_sale_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column(
                               'client_order_id', db.Integer, db.ForeignKey('bra_framework_order.id'))
                           )
agents = db.Table('framework_order_agents',
                  db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
                  db.Column(
                      'framework_order_id', db.Integer, db.ForeignKey('bra_framework_order.id')),
                  )


class FrameworkOrder(db.Model, BaseModelMixin, CommentMixin, AttachmentMixin):
    __tablename__ = 'bra_framework_order'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('bra_group.id'))  # 甲方集团
    group = db.relationship(
        'Group', backref=db.backref('framework_orders', lazy='dynamic'))
    agents = db.relationship('Agent', secondary=agents)
    description = db.Column(db.String(500))  # 描述

    contract = db.Column(db.String(100))  # 客户合同号
    douban_contract = db.Column(db.String(100))  # 豆瓣合同号
    money = db.Column(db.Float())  # 客户合同金额
    contract_type = db.Column(db.Integer)  # 合同类型： 标准，非标准
    client_start = db.Column(db.Date)
    client_end = db.Column(db.Date)
    client_start_year = db.Column(db.Integer, index=True)
    client_end_year = db.Column(db.Integer, index=True)
    reminde_date = db.Column(db.Date)  # 最迟回款日期

    direct_sales = db.relationship('User', secondary=direct_sales)
    agent_sales = db.relationship('User', secondary=agent_sales)
    assistant_sales = db.relationship('User', secondary=assistant_sales)
    contract_status = db.Column(db.Integer)  # 合同审批状态
    status = db.Column(db.Integer)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship(
        'User', backref=db.backref('created_framework_orders', lazy='dynamic'))
    create_time = db.Column(db.DateTime)
    finish_time = db.Column(db.DateTime)   # 合同归档时间
    inad_rebate = db.Column(db.Float)
    douban_rebate = db.Column(db.Float)
    contract_generate = True
    media_apply = False
    kind = "framework-order"
    __mapper_args__ = {'order_by': contract.desc()}

    def __init__(self, group, agents=None, description=None, status=STATUS_ON,
                 contract="", money=0, contract_type=CONTRACT_TYPE_NORMAL,
                 client_start=None, client_end=None, reminde_date=None,
                 direct_sales=None, agent_sales=None, assistant_sales=[], finish_time=None,
                 creator=None, create_time=None, contract_status=CONTRACT_STATUS_NEW,
                 inad_rebate=0.0, douban_rebate=0.0):
        self.group = group
        self.agents = agents or []
        self.description = description or ""

        self.contract = contract
        self.money = money
        self.contract_type = contract_type

        self.client_start = client_start or datetime.date.today()
        self.client_end = client_end or datetime.date.today()
        self.client_start_year = int(self.client_start.year)
        self.client_end_year = int(self.client_end.year)
        self.reminde_date = reminde_date or datetime.date.today()

        self.direct_sales = direct_sales or []
        self.agent_sales = agent_sales or []
        self.assistant_sales = assistant_sales or []

        self.creator = creator
        self.create_time = create_time or datetime.datetime.now()
        self.finish_time = finish_time or datetime.datetime.now()
        self.contract_status = contract_status
        self.status = status
        self.inad_rebate = inad_rebate
        self.douban_rebate = douban_rebate

    @classmethod
    def get_all(cls):
        """查看所有没删除订单"""
        return [o for o in cls.query.all() if o.status in [STATUS_ON, None] and o.contract_status not in [9]]

    @classmethod
    def all(cls):
        return cls.get_all()

    @classmethod
    def delete_all(cls):
        return [o for o in cls.query.all() if o.status == STATUS_DEL]

    @property
    def name(self):
        if self.agents:
            return u"框架-%s-%s" % (self.group.name, self.agents[0].name)
        return u"框架-%s" % (self.group.name)

    @property
    def direct_sales_names(self):
        return ",".join([u.name for u in self.direct_sales])

    @property
    def agent_sales_names(self):
        return ",".join([u.name for u in self.agent_sales])

    @property
    def assistant_sales_names(self):
        return ",".join([u.name for u in self.assistant_sales])

    @property
    def leaders(self):
        return list(set([l for u in self.direct_sales + self.agent_sales + self.assistant_sales
                         for l in u.user_leaders] + User.super_leaders()))

    @property
    def email_info(self):
        return u"""
        类型:框架订单
        代理集团: %s
        金额: %s
        直客销售: %s
        渠道销售: %s
        执行开始时间: %s
        执行结束时间: %s
        框架合同号: %s
        备注: %s
        """ % (self.group.name, self.money, self.direct_sales_names,
               self.agent_sales_names, self.start_date_cn, self.end_date_cn,
               self.contract, self.description,)

    def can_admin(self, user):
        """是否可以修改该订单"""
        salers = self.direct_sales + self.agent_sales + self.assistant_sales
        leaders = []
        for k in salers:
            leaders += k.team_leaders
        admin_users = salers + [self.creator] + list(set(leaders))
        return user.is_admin() or user.is_contract() or user in admin_users

    def can_media_leader_action(self, user):
        return False

    def have_owner(self, user):
        """是否可以查看该订单"""
        salers = self.direct_sales + self.agent_sales + self.assistant_sales
        leaders = []
        for k in salers:
            leaders += k.team_leaders
        owner = salers + [self.creator] + list(set(leaders))
        return user.is_admin() or user in owner

    @classmethod
    def get_order_by_user(cls, user):
        """一个用户可以查看的所有订单"""
        return [o for o in cls.all() if o.have_owner(user) and o.status in [STATUS_ON, None]]

    def path(self):
        return self.info_path()

    @property
    def locations(self):
        return list(set([u.location for u in self.direct_sales + self.agent_sales]))

    @property
    def locations_cn(self):
        return ",".join([TEAM_LOCATION_CN[l] for l in self.locations])

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
        return url_for('files.framework_order_files', order_id=self.id)

    def info_path(self):
        return url_for("order.framework_order_info", order_id=self.id)

    def contract_path(self):
        return url_for("order.framework_order_contract", order_id=self.id)

    def attach_status_confirm_path(self, attachment):
        return url_for('order.framework_attach_status',
                       order_id=self.id,
                       attachment_id=attachment.id,
                       status=ATTACHMENT_STATUS_PASSED)

    def attach_status_reject_path(self, attachment):
        return url_for('order.framework_attach_status',
                       order_id=self.id,
                       attachment_id=attachment.id,
                       status=ATTACHMENT_STATUS_REJECT)

    @classmethod
    def contract_exist(cls, contract):
        is_exist = cls.query.filter_by(contract=contract).count() > 0
        return is_exist

    def get_default_contract(self):
        return contract_generator(self.group, self.id)

    def douban_contract_apply_path(self):
        return url_for("contract.framework_douban_apply", order_id=self.id)

    def can_edit_contract_time(self, now_date=None):
        if not now_date:
            now_date = datetime.date.today()
        if self.client_start.month > now_date.month:
            return True
        else:
            return False

    @property
    def finish_time_cn(self):
        try:
            return self.finish_time.date()
        except:
            return ''


def contract_generator(group, num):
    code = "ZQF%s%03x-%03x" % (datetime.datetime.now().strftime('%Y%m'),
                               group.id % 1000, num % 1000)
    code = code.upper()
    return code
