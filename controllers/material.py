# -*- coding: UTF-8 -*-
from flask import Blueprint, request, redirect, abort, g, url_for
from flask import render_template as tpl, flash, Response

from models.item import AdItem
from models.material import Material, ImageMaterial
from forms.material import RawMaterialForm, ImageMaterialForm

material_bp = Blueprint('material', __name__, template_folder='../templates/material')


@material_bp.route('/', methods=['GET'])
def index():
    return redirect('/')


@material_bp.route('/new_material/item/<item_id>', methods=['GET', 'POST'])
def new_material(item_id):
    item = AdItem.get(item_id)
    if not item:
        abort(404)
    form = RawMaterialForm(request.form)
    if request.method == 'POST' and form.validate():
        material = Material.add(name=form.name.data, item=item, creator=g.user)
        material.code = form.code.data
        material.status = form.status.data
        material.save()
        flash(u'新建素材(%s)成功!' % material.name, 'success')
        return redirect(url_for('order.item_materials', item_id=item.id))
    return tpl('material_raw.html', form=form)


@material_bp.route('/material/<material_id>/', methods=['GET', 'POST'])
def raw_material(material_id):
    material = Material.get(material_id)
    if not material:
        abort(404)
    form = RawMaterialForm(request.form)
    if request.method == 'POST':
        if form.validate():
            material.name = form.name.data
            material.code = form.code.data
            material.status = form.status.data
            material.save()
            flash(u'素材(%s)保存成功!' % material.name, 'success')
    else:
        form.name.data = material.name
        form.code.data = material.code
        form.status.data = material.status
    return tpl('material_raw.html', form=form, material=material)


def material_preview_response(material):
    if not material or not material.processed_html:
        abort(404)
    response = Response()
    response.set_data(material.processed_html)
    return response


@material_bp.route('/material/<material_id>/preview/')
def raw_preview(material_id):
    material = Material.get(material_id)
    return material_preview_response(material)


@material_bp.route('/new_image_material/item/<item_id>', methods=['GET', 'POST'])
def new_image_material(item_id):
    item = AdItem.get(item_id)
    if not item:
        abort(404)
    form = ImageMaterialForm(request.form)
    form.code.hidden = True
    if request.method == 'POST' and form.validate():
        material = ImageMaterial.add(name=form.name.data, item=item, creator=g.user)
        material.status = form.status.data
        material.image_file = form.image_file.data
        material.click_link = form.click_link.data
        material.monitor_link = form.monitor_link.data
        material.code = form.code.data
        material.save()
        flash(u'新建素材(%s)成功!' % material.name, 'success')
        return redirect(url_for('order.item_materials', item_id=item.id))
    return tpl('material_image.html', form=form, item=item)


@material_bp.route('/image_material/<material_id>/', methods=['GET', 'POST'])
def image_material(material_id):
    material = ImageMaterial.get(material_id)
    if not material:
        abort(404)
    form = ImageMaterialForm(request.form)
    form.code.hidden = True
    if request.method == 'POST':
        if form.validate():
            material.name = form.name.data
            material.status = form.status.data
            material.image_file = form.image_file.data
            material.click_link = form.click_link.data
            material.monitor_link = form.monitor_link.data
            material.code = form.code.data
            material.save()
            flash(u'素材(%s)保存成功!' % material.name, 'success')
    else:
        form.name.data = material.name
        form.status.data = material.status
        form.image_file.data = material.image_file
        form.click_link.data = material.click_link
        form.monitor_link.data = material.monitor_link
        form.code.data = material.code
    return tpl('material_image.html', form=form, material=material, item=material.item)


@material_bp.route('/image_material/<material_id>/preview/')
def image_preview(material_id):
    material = ImageMaterial.get(material_id)
    return material_preview_response(material)


@material_bp.route('/copy_material/<item_id>', methods=['POST'])
def copy_material(item_id):
    item_ids = request.form.getlist('item_id')
    material_ids = request.form.getlist('material_id')
    if not material_ids:
        flash(u"请选择素材")
    elif not item_ids:
        flash(u"请选择订单项")
    else:
        items = [AdItem.get(i_id) for i_id in item_ids]
        for m_id in material_ids:
            material = Material.get(m_id)
            for i in items:
                new_material = Material.add(
                    name="%s_copy" % material.name,
                    item=i,
                    creator=g.user,
                    type=material.type)
                new_material.code = material.code
                new_material.status = material.status
                new_material.props = material.props
                new_material.save()
        flash(u'拷贝%s素材到个%s订单项成功!' % (len(material_ids), len(item_ids)), 'success')
    return redirect(url_for('order.item_detail', item_id=item_id))
