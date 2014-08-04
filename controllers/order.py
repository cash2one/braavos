#-*- coding: UTF-8 -*-
from datetime import datetime, timedelta

from flask import Blueprint, request, redirect, abort, url_for, g
from flask import render_template as tpl, json

from models.order import Order
from models.client import Client, Agent
from models.medium import Medium, AdPosition
from models.item import AdItem, AdSchedule, SALE_TYPE_CN
from models.user import User
from forms.order import OrderForm
from forms.item import ItemForm

order_bp = Blueprint('order', __name__, template_folder='../templates/order')


@order_bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('order.orders'))


@order_bp.route('/new_order', methods=['GET', 'POST'])
def new_order():
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        order = Order(client=Client.get(form.client.data), campaign=form.campaign.data,
                      medium=Medium.get(form.medium.data), order_type=form.order_type.data,
                      contract=form.contract.data, money=form.money.data,
                      agent=Agent.get(form.agent.data), direct_sales=User.gets(form.direct_sales.data),
                      agent_sales=User.gets(form.agent_sales.data), operaters=User.gets(form.operaters.data),
                      planers=User.gets(form.planers.data), designers=User.gets(form.designers.data), creator=g.user,
                      create_time=datetime.now())
        order.add()
        return redirect(url_for("order.orders"))
    else:
        form.creator.data = g.user.name
    return tpl('new_order.html', form=form)


@order_bp.route('/order_detail/<order_id>', methods=['GET', 'POST'])
def order_detail(order_id):
    order = Order.get(order_id)
    if not order:
        abort(404)
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        order.client = Client.get(form.client.data)
        order.campaign = form.campaign.data
        order.medium = Medium.get(form.medium.data)
        order.order_type = form.order_type.data
        order.contract = form.contract.data
        order.money = form.money.data
        order.agent = Agent.get(form.agent.data)
        order.direct_sales = User.gets(form.direct_sales.data)
        order.agent_sales = User.gets(form.agent_sales.data)
        order.operaters = User.gets(form.operaters.data)
        order.designers = User.gets(form.designers.data)
        order.planers = User.gets(form.planers.data)
        order.save()
        return redirect(url_for("order.orders"))
    else:
        form.client.data = order.client.id
        form.campaign.data = order.campaign
        form.medium.choices = [(order.medium.id, order.medium.name)]
        form.medium.data = order.medium.id
        form.order_type.data = order.order_type
        form.contract.data = order.contract
        form.money.data = order.money
        form.agent.data = order.agent.id
        form.direct_sales.data = [u.id for u in order.direct_sales]
        form.agent_sales.data = [u.id for u in order.agent_sales]
        form.operaters.data = [u.id for u in order.operaters]
        form.designers.data = [u.id for u in order.designers]
        form.planers.data = [u.id for u in order.planers]
        form.creator.data = order.creator.name
    return tpl('order.html', form=form, order=order)


@order_bp.route('/orders', methods=['GET'])
def orders():
    orders = Order.all()
    return tpl('orders.html', orders=orders)


@order_bp.route('/order_detail/<order_id>/new_item')
def new_item(order_id):
    order = Order.get(order_id)
    if not order:
        abort(404)
    start_date = datetime.today()
    end_date = start_date + timedelta(days=30)
    positions = [(x.id, x.display_name) for x in AdPosition.all()]
    return tpl('new_item.html', order=order, positions=positions,
               start_date=start_date, end_date=end_date,
               SALE_TYPE_CN=SALE_TYPE_CN, SPECIAL_SALE_CN={0: u"否", 1: u"是"})


def check_schedules_post(data):
    """检查排期数据是否合法"""
    try:
        status = 0
        msg = ''
        items = json.loads(data)
        for item in items:
            position = AdPosition.get(item['position'])
            for (date_str, num_str) in item['schedule'].items():
                date = datetime.strptime(date_str, '%Y-%m-%d')
                num = int(num_str)
                if position.can_order_num(date) < num:
                    status = 1
                    msg += u'%s 最多只能预订 %s \n' % (position.display_name, position.can_order_num(date))
    except:
        return '1', "数据解析出错啦"
    return status, msg


def add_schedules(order, data):
    """新增订单项, 排期项"""
    items = json.loads(data)
    for item in items:
        position = AdPosition.get(item['position'])
        adItem = AdItem(order=order, sale_type=item['sale_type'], special_sale=item['special_sale'],
                        position=position, creator=g.user, create_time=datetime.now())
        adItem.add()
        for (date_str, num_str) in item['schedule'].items():
            start_time = datetime.strptime(date_str, '%Y-%m-%d')
            end_time = start_time + timedelta(days=1, seconds=-1)
            num = int(num_str)
            schedule = AdSchedule(item=adItem, num=num, start_time=start_time, end_time=end_time)
            schedule.add()


@order_bp.route('/order_detail/<order_id>/schedules_post/', methods=["POST"])
def schedules_post(order_id):
    """AJAX 提交排期数据"""
    order = Order.get(order_id)
    if not order:
        abort(404)
    data = request.values.get('data')
    status, msg = check_schedules_post(data)
    if not status:
        add_schedules(order, data)
    return json.dumps({'status': status, 'msg': msg})


def schdule_info(date, num):
    return (date.strftime("%Y-%m-%d"), num, date.isoweekday())


def get_schedule(position, start_date, end_date):
    ret = {"position": position.id,
           "name": position.display_name,
           "start": start_date.strftime("%Y-%m-%d"),
           "end": end_date.strftime("%Y-%m-%d")}
    ret['schedules'] = [schdule_info(date, num) for date, num in position.can_order_schedule(start_date, end_date)]
    return ret


@order_bp.route('/schedule_info', methods=['GET'])
def schedule_info():
    """ajax 获取排期数据"""
    start_date = datetime.strptime(request.values.get('start'), '%Y-%m-%d')
    end_date = datetime.strptime(request.values.get('end'), '%Y-%m-%d')
    position = AdPosition.get(request.values.get('position'))
    return json.dumps(get_schedule(position, start_date, end_date))


@order_bp.route('/position_list', methods=['GET'])
def position_list():
    order = Order.get(request.values.get('order'))
    sale_type = request.values.get('sale_type')
    special_sale = request.values.get('special_sale')
    return json.dumps([(p.id, p.display_name) for p in AdPosition.all()])


@order_bp.route('/item_detail/<item_id>', methods=["GET", "POST"])
def item_detail(item_id):
    item = AdItem.get(item_id)
    if not item:
        abort(404)
    form = ItemForm(request.form)
    if request.method == 'POST' and form.validate():
        item.sale_type = form.sale_type.data
        item.special_sale = form.special_sale.data
        item.description = form.description.data
        item.ad_type = form.ad_type.data
        item.price = form.price.data
        item.priority = form.priority.data
        item.speed = form.speed.data
        item.item_status = form.item_status.data
        item.status = form.status.data
        item.save()
    else:
        form.order.data = item.order.name
        form.sale_type.data = item.sale_type
        form.special_sale.data = item.special_sale
        form.position.data = item.position.name
        form.description.data = item.description
        form.ad_type.data = item.ad_type
        form.price.data = item.price
        form.priority.data = item.priority
        form.speed.data = item.speed
        form.item_status.data = item.item_status
        form.status.data = item.status
        form.creator.data = item.creator.name

        form.order.readonly = True
        form.position.readonly = True
        form.creator.readonly = True

    return tpl('item.html', form=form, item=item)
