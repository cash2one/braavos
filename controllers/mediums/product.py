# -*- coding: utf-8 -*-
import datetime

from flask import request, redirect, url_for, Blueprint, flash, json, jsonify
from flask import render_template as tpl

from models.medium import Medium, MediumProductPC, MediumProductApp, MediumProductDown
from forms.medium import NewMediumProductPC, NewMediumProductApp, NewMediumProductDown
from libs.paginator import Paginator

mediums_product_bp = Blueprint(
    'mediums_product', __name__, template_folder='../../templates/mediums/product/')


@mediums_product_bp.route('/product/<mtype>/index', methods=['GET'])
def index(mtype):
    page = int(request.values.get('p', 1))
    if mtype == 'pc':
        products = MediumProductPC.all()
    elif mtype == 'app':
        products = MediumProductApp.all()
    elif mtype == 'down':
        products = MediumProductDown.all()
    paginator = Paginator(list(products), 50)
    try:
        products = paginator.page(page)
    except:
        products = paginator.page(paginator.num_pages)
    return tpl('/mediums/product/index.html', mtype=mtype, products=products)


@mediums_product_bp.route('/product/<mtype>/create', methods=['GET', 'POST'])
def create(mtype):
    if mtype == 'pc':
        form = NewMediumProductPC(request.form)
    elif mtype == 'app':
        form = NewMediumProductApp(request.form)
    elif mtype == 'down':
        form = NewMediumProductDown(request.form)
    if request.method == 'POST' and form.validate():
        body = []
        custom_ids = request.values.get('custom_ids', '')
        for x in custom_ids.split('|'):
            key = request.values.get('custom_key_' + str(x), '')
            value = request.values.get('custom_value_' + str(x), '')
            body.append({'c_key': key, 'c_value': value})

        if mtype == 'pc':
            if MediumProductPC.query.filter_by(name=form.name.data).count() > 0:
                flash(u'产品名称已存在', 'danger')
                return tpl('/mediums/product/create.html', form=form, mtype=mtype)
            MediumProductPC.add(medium=Medium.get(form.medium.data),
                                name=form.name.data,
                                create_time=datetime.datetime.now(),
                                update_time=datetime.datetime.now(),
                                register_count=form.register_count.data,
                                alone_count_by_day=form.alone_count_by_day.data,
                                active_count_by_day=form.active_count_by_day.data,
                                alone_count_by_month=form.alone_count_by_month.data,
                                active_count_by_month=form.active_count_by_month.data,
                                pv_by_day=form.pv_by_day.data,
                                pv_by_month=form.pv_by_month.data,
                                access_time=form.access_time.data,
                                ugc_count=form.ugc_count.data,
                                cooperation_type=form.cooperation_type.data,
                                divide_into=form.divide_into.data,
                                policies=form.policies.data,
                                delivery=form.delivery.data,
                                special=form.special.data,
                                sex_distributed=form.sex_distributed.data,
                                age_distributed=form.age_distributed.data,
                                area_distributed=form.area_distributed.data,
                                education_distributed=form.education_distributed.data,
                                income_distributed=form.income_distributed.data,
                                product_position=form.product_position.data,
                                body=json.dumps(body))
        elif mtype == 'app':
            if MediumProductApp.query.filter_by(name=form.name.data).count() > 0:
                flash(u'产品名称已存在', 'danger')
                return tpl('/mediums/product/create.html', form=form, mtype=mtype)
            MediumProductApp.add(medium=Medium.get(form.medium.data),
                                 name=form.name.data,
                                 create_time=datetime.datetime.now(),
                                 update_time=datetime.datetime.now(),
                                 install_count=form.install_count.data,
                                 activation_count=form.activation_count.data,
                                 register_count=form.register_count.data,
                                 active_count_by_day=form.active_count_by_day.data,
                                 active_count_by_month=form.active_count_by_month.data,
                                 pv_by_day=form.pv_by_day.data,
                                 pv_by_month=form.pv_by_month.data,
                                 open_rate_by_day=form.open_rate_by_day.data,
                                 access_time=form.access_time.data,
                                 ugc_count=form.ugc_count.data,
                                 cooperation_type=form.cooperation_type.data,
                                 divide_into=form.divide_into.data,
                                 policies=form.policies.data,
                                 delivery=form.delivery.data,
                                 special=form.special.data,
                                 sex_distributed=form.sex_distributed.data,
                                 age_distributed=form.age_distributed.data,
                                 area_distributed=form.area_distributed.data,
                                 education_distributed=form.education_distributed.data,
                                 income_distributed=form.income_distributed.data,
                                 product_position=form.product_position.data,
                                 body=json.dumps(body))
        elif mtype == 'down':
            if MediumProductDown.query.filter_by(name=form.name.data).count() > 0:
                flash(u'产品名称已存在', 'danger')
                return tpl('/mediums/product/create.html', form=form, mtype=mtype)
            MediumProductDown.add(medium=Medium.get(form.medium.data),
                                  name=form.name.data,
                                  create_time=datetime.datetime.now(),
                                  update_time=datetime.datetime.now(),
                                  start_time=request.values.get(
                                      'start_time', ''),
                                  end_time=request.values.get('end_time', ''),
                                  business_start_time=request.values.get(
                                      'business_start_time', ''),
                                  business_end_time=request.values.get(
                                      'business_end_time', ''),
                                  location=form.location.data,
                                  subject=form.subject.data,
                                  before_year_count=form.before_year_count.data,
                                  now_year_count=form.now_year_count.data,
                                  cooperation_type=form.cooperation_type.data,
                                  divide_into=form.divide_into.data,
                                  policies=form.policies.data,
                                  delivery=form.delivery.data,
                                  special=form.special.data,
                                  sex_distributed=form.sex_distributed.data,
                                  age_distributed=form.age_distributed.data,
                                  area_distributed=form.area_distributed.data,
                                  education_distributed=form.education_distributed.data,
                                  income_distributed=form.income_distributed.data,
                                  product_position=form.product_position.data,
                                  body=json.dumps(body))
        flash(u'添加成功', 'success')
        return redirect(url_for('mediums_product.index', mtype=mtype))
    return tpl('/mediums/product/create.html', form=form, mtype=mtype)


@mediums_product_bp.route('/product/<mtype>/<pid>/update', methods=['GET', 'POST'])
def update(mtype, pid):
    if mtype == 'pc':
        product = MediumProductPC.get(pid)
        form = NewMediumProductPC(request.form)
        form.name.data = product.name
        form.medium.data = product.medium.id
        form.register_count.data = product.register_count
        form.alone_count_by_day.data = product.alone_count_by_day
        form.active_count_by_day.data = product.active_count_by_day
        form.alone_count_by_month.data = product.alone_count_by_month
        form.active_count_by_month.data = product.active_count_by_month
        form.pv_by_day.data = product.pv_by_day
        form.pv_by_month.data = product.pv_by_month
        form.access_time.data = product.access_time
        form.ugc_count.data = product.ugc_count
        form.cooperation_type.data = product.cooperation_type
        form.divide_into.data = product.divide_into
        form.policies.data = product.policies
        form.delivery.data = product.delivery
        form.special.data = product.special
        form.sex_distributed.data = product.sex_distributed
        form.age_distributed.data = product.age_distributed
        form.area_distributed.data = product.area_distributed
        form.education_distributed.data = product.education_distributed
        form.income_distributed.data = product.income_distributed
        form.product_position.data = product.product_position
    elif mtype == 'app':
        product = MediumProductApp.get(pid)
        form = NewMediumProductApp(request.form)
        form.medium.data = product.medium.id
        form.name.data = product.name
        form.install_count.data = product.install_count
        form.activation_count.data = product.activation_count
        form.register_count.data = product.register_count
        form.active_count_by_day.data = product.active_count_by_day
        form.active_count_by_month.data = product.active_count_by_month
        form.pv_by_day.data = product.pv_by_day
        form.pv_by_month.data = product.pv_by_month
        form.open_rate_by_day.data = product.open_rate_by_day
        form.access_time.data = product.access_time
        form.ugc_count.data = product.ugc_count
        form.cooperation_type.data = product.cooperation_type
        form.divide_into.data = product.divide_into
        form.policies.data = product.policies
        form.delivery.data = product.delivery
        form.special.data = product.special
        form.sex_distributed.data = product.sex_distributed
        form.age_distributed.data = product.age_distributed
        form.area_distributed.data = product.area_distributed
        form.education_distributed.data = product.education_distributed
        form.income_distributed.data = product.income_distributed
        form.product_position.data = product.product_position
    elif mtype == 'down':
        product = MediumProductDown.get(pid)
        form = NewMediumProductDown(request.form)
        form.medium.data = product.medium.id
        form.name.data = product.name
        form.medium.data = product.medium.id
        form.name.data = product.name
        form.location.data = product.location
        form.subject.data = product.subject
        form.before_year_count.data = product.before_year_count
        form.now_year_count.data = product.now_year_count
        form.cooperation_type.data = product.cooperation_type
        form.divide_into.data = product.divide_into
        form.policies.data = product.policies
        form.delivery.data = product.delivery
        form.special.data = product.special
        form.sex_distributed.data = product.sex_distributed
        form.age_distributed.data = product.age_distributed
        form.area_distributed.data = product.area_distributed
        form.education_distributed.data = product.education_distributed
        form.income_distributed.data = product.income_distributed
        form.product_position.data = product.product_position
    product.c_body = json.loads(product.body)
    if request.method == 'POST' and form.validate():
        body = []
        custom_ids = request.values.get('custom_ids', '')
        print custom_ids
        for x in custom_ids.split('|'):
            key = request.values.get('custom_key_' + str(x), '')
            value = request.values.get('custom_value_' + str(x), '')
            body.append({'c_key': key, 'c_value': value})
        if mtype == 'pc':
            form = NewMediumProductPC(request.form)
            if product.name != form.name.data and MediumProductPC.query.filter_by(name=form.name.data).count() > 0:
                flash(u'产品名称已存在', 'danger')
                return tpl('/mediums/product/update.html', form=form, mtype=mtype)
            product.name = form.name.data
            product.medium = Medium.get(form.medium.data)
            product.register_count = form.register_count.data
            product.alone_count_by_day = form.alone_count_by_day.data
            product.active_count_by_day = form.active_count_by_day.data
            product.alone_count_by_month = form.alone_count_by_month.data
            product.active_count_by_month = form.active_count_by_month.data
            product.pv_by_day = form.pv_by_day.data
            product.pv_by_month = form.pv_by_month.data
            product.access_time = form.access_time.data
            product.ugc_count = form.ugc_count.data
            product.cooperation_type = form.cooperation_type.data
            product.divide_into = form.divide_into.data
            product.policies = form.policies.data
            product.delivery = form.delivery.data
            product.special = form.special.data
            product.sex_distributed = form.sex_distributed.data
            product.age_distributed = form.age_distributed.data
            product.area_distributed = form.area_distributed.data
            product.education_distributed = form.education_distributed.data
            product.income_distributed = form.income_distributed.data
            product.product_position = form.product_position.data
            product.body = json.dumps(body)
            product.save()
        elif mtype == 'app':
            form = NewMediumProductApp(request.form)
            if product.name != form.name.data and MediumProductApp.query.filter_by(name=form.name.data).count() > 0:
                flash(u'产品名称已存在', 'danger')
                return tpl('/mediums/product/update.html', form=form, mtype=mtype)
            product.medium = Medium.get(form.medium.data)
            product.name = form.name.data
            product.create_time = datetime.datetime.now()
            product.update_time = datetime.datetime.now()
            product.install_count = form.install_count.data
            product.activation_count = form.activation_count.data
            product.register_count = form.register_count.data
            product.active_count_by_day = form.active_count_by_day.data
            product.active_count_by_month = form.active_count_by_month.data
            product.pv_by_day = form.pv_by_day.data
            product.pv_by_month = form.pv_by_month.data
            product.open_rate_by_day = form.open_rate_by_day.data
            product.access_time = form.access_time.data
            product.ugc_count = form.ugc_count.data
            product.cooperation_type = form.cooperation_type.data
            product.divide_into = form.divide_into.data
            product.policies = form.policies.data
            product.delivery = form.delivery.data
            product.special = form.special.data
            product.sex_distributed = form.sex_distributed.data
            product.age_distributed = form.age_distributed.data
            product.area_distributed = form.area_distributed.data
            product.education_distributed = form.education_distributed.data
            product.income_distributed = form.income_distributed.data
            product.product_position = form.product_position.data
            product.body = json.dumps(body)
            product.save()
        elif mtype == 'down':
            form = NewMediumProductDown(request.form)
            if product.name != form.name.data and MediumProductDown.query.filter_by(name=form.name.data).count() > 0:
                flash(u'产品名称已存在', 'danger')
                return tpl('/mediums/product/update.html', form=form, mtype=mtype)
            product.medium = Medium.get(form.medium.data)
            product.name = form.name.data
            product.update_time = datetime.datetime.now()
            product.start_time = request.values.get('start_time', '')
            product.end_time = request.values.get('end_time', '')
            product.business_start_time = request.values.get(
                'business_start_time', '')
            product.business_end_time = request.values.get(
                'business_end_time', '')
            product.location = form.location.data
            product.subject = form.subject.data
            product.before_year_count = form.before_year_count.data
            product.now_year_count = form.now_year_count.data
            product.cooperation_type = form.cooperation_type.data
            product.divide_into = form.divide_into.data
            product.policies = form.policies.data
            product.delivery = form.delivery.data
            product.special = form.special.data
            product.sex_distributed = form.sex_distributed.data
            product.age_distributed = form.age_distributed.data
            product.area_distributed = form.area_distributed.data
            product.education_distributed = form.education_distributed.data
            product.income_distributed = form.income_distributed.data
            product.product_position = form.product_position.data
            product.body = json.dumps(body)
            product.save()
        flash(u'修改成功', 'success')
        return redirect(url_for('mediums_product.update', mtype=mtype, pid=product.id))
    return tpl('/mediums/product/update.html', form=form, mtype=mtype, product=product)


@mediums_product_bp.route('/product/<mtype>/<pid>/info', methods=['GET', 'POST'])
def info(mtype, pid):
    if mtype == 'pc':
        product = MediumProductPC.get(pid)
    elif mtype == 'app':
        product = MediumProductApp.get(pid)
    elif mtype == 'down':
        product = MediumProductDown.get(pid)
    product.c_body = json.loads(product.body)
    return tpl('/mediums/product/info.html', mtype=mtype, product=product)


@mediums_product_bp.route('/product/<mtype>/<pid>/delete', methods=['GET'])
def delete(mtype, pid):
    if mtype == 'pc':
        MediumProductPC.get(pid).delete()
    elif mtype == 'app':
        MediumProductApp.get(pid).delete()
    elif mtype == 'down':
        MediumProductDown.get(pid).delete()
    return jsonify({'id': pid})
