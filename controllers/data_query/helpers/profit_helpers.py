# -*- coding: UTF-8 -*-
import StringIO
import mimetypes
import datetime

from flask import Response, g
from werkzeug.datastructures import Headers
import xlsxwriter


def write_douban_order_excel(orders, year, month):
    response = Response()
    response.status_code = 200
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    align_left = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'border': 1})
    keys = [u'区域', u'合同号', u'客户名称', u'代理/直客', u'项目名称', u'客户合同总金额', u'回款总金额', u'客户' +
            str(month) + u'月执行额', str(month) + u'月支付代理返点', str(month) + u'月合同利润', u'合同开始', u'合同结束']
    for k in range(len(keys)):
        worksheet.write(0, 0 + k, keys[k], align_left)
    # 设置宽度为30
    for k in range(18):
        worksheet.set_column(k, 0, 15)
    # 设置高度
    for k in range(0, len(orders) + 2):
        worksheet.set_row(k, 20)

    th = 1
    for k in range(len(orders)):
        if orders[k]['__tablename__'] == 'bra_order':
            worksheet.write(th, 0, orders[k]['locations_cn'], align_left)
            worksheet.write(
                th, 1, orders[k]['associated_douban_contract'], align_left)
            worksheet.write(th, 2, orders[k]['client_name'], align_left)
            worksheet.write(th, 3, orders[k]['medium_name'], align_left)
            worksheet.write(th, 4, orders[k]['campaign'], align_left)
            worksheet.write(th, 5, orders[k]['medium_money2'], align_left)
            worksheet.write(th, 6, orders[k]['back_moneys'], align_left)
            worksheet.write(th, 7, orders[k]['now_month_money_zhixing'], align_left)
            worksheet.write(th, 8, orders[k]['now_month_agent_rebate_money'], align_left)
            worksheet.write(th, 9, orders[k]['profit_money'], align_left)
            worksheet.write(th, 10, orders[k]['start_date_cn'], align_left)
            worksheet.write(th, 11, orders[k]['end_date_cn'], align_left)
        else:
            worksheet.write(th, 0, orders[k]['locations_cn'], align_left)
            worksheet.write(th, 1, orders[k]['contract'], align_left)
            worksheet.write(th, 2, orders[k]['client_name'], align_left)
            worksheet.write(th, 3, orders[k]['agent_name'], align_left)
            worksheet.write(th, 4, orders[k]['campaign'], align_left)
            worksheet.write(th, 5, orders[k]['money'], align_left)
            worksheet.write(th, 6, orders[k]['back_moneys'], align_left)
            worksheet.write(th, 7, orders[k]['now_month_money_zhixing'], align_left)
            worksheet.write(
                th, 8, orders[k]['now_month_agent_rebate_money'], align_left)
            worksheet.write(th, 9, orders[k]['profit_money'], align_left)
            worksheet.write(th, 10, orders[k]['start_date_cn'], align_left)
            worksheet.write(th, 11, orders[k]['end_date_cn'], align_left)
        th += 1
    workbook.close()
    response.data = output.getvalue()
    filename = ("%s-%s.xls" %
                (u"Execution-douban", datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    mimetype_tuple = mimetypes.guess_type(filename)
    response_headers = Headers({
        'Pragma': "public",
        'Expires': '0',
        'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
        'Cache-Control': 'private',
        'Content-Type': mimetype_tuple[0],
        'Content-Disposition': 'attachment; filename=\"%s\";' % filename,
        'Content-Transfer-Encoding': 'binary',
        'Content-Length': len(response.data)
    })
    response.headers = response_headers
    response.set_cookie('fileDownload', 'true', path='/')
    return response


def write_order_excel(orders, year, month):
    response = Response()
    response.status_code = 200
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    align_left = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'border': 1})
    keys = [u'所属区域', u'合同号', u'客户名称', u'直客/代理', u'项目名称', u'合同总金额',
            u'已回款金额', str(month) + u'月执行额', str(month) +
            u'月代理返点', str(month) + u'月实际代理返点',
            u'投放媒体', str(month) + u'月客户金额', u'媒体合同号',
            u'媒体合同总金额', str(month) + u'月媒体执行金额', str(month) + u'月媒体返点',
            str(month) + u'月实际媒体返点', str(month) +
            u'月合同利润', str(month) + u'月实际合同利润',
            u'合同开始', u'合同结束']
    for k in range(len(keys)):
        worksheet.write(0, 0 + k, keys[k], align_left)

    # 设置宽度为30
    for k in range(18):
        worksheet.set_column(k, 0, 15)
    # 设置高度
    for k in range(0, len(orders) + 2):
        worksheet.set_row(k, 20)

    th = 1
    for k in range(len(orders)):
        mediums = orders[k]['medium_data']
        # 媒介导出报表时要拆分(多媒体合同时要拆分成一条一条，不需要合并)
        if g.user.is_media_leader():
            for i in range(len(mediums)):
                worksheet.write(th, 0, orders[k]['locations_cn'], align_left)
                worksheet.write(th, 1, orders[k]['contract'], align_left)
                worksheet.write(th, 2, orders[k]['client_name'], align_left)
                worksheet.write(th, 3, orders[k]['agent_name'], align_left)
                worksheet.write(th, 4, orders[k]['campaign'], align_left)
                if i == 0:
                    worksheet.write(th, 5, orders[k]['money'], align_left)
                    worksheet.write(th, 6, orders[k]['back_moneys'], align_left)
                    worksheet.write(th, 7, orders[k]['now_month_money_zhixing'], align_left)
                    worksheet.write(th, 8, orders[k]['now_month_agent_rebate_money'], align_left)
                    worksheet.write(th, 9, orders[k]['now_month_agent_real_rebate_money'], align_left)
                    worksheet.write(th, 16, orders[k]['now_month_medium_real_rebate_money'], align_left)
                    worksheet.write(th, 17, orders[k]['profit_money'], align_left)
                    worksheet.write(th, 18, orders[k]['real_profit_money'], align_left)
                else:
                    worksheet.write(th, 5, '', align_left)
                    worksheet.write(th, 6, '', align_left)
                    worksheet.write(th, 7, '', align_left)
                    worksheet.write(th, 8, '', align_left)
                    worksheet.write(th, 9, '', align_left)
                    worksheet.write(th, 16, '', align_left)
                    worksheet.write(th, 17, '', align_left)
                    worksheet.write(th, 18, '', align_left)

                worksheet.write(th, 10, mediums[i]['name'], align_left)
                worksheet.write(th, 11, mediums[i]['now_month_money_kehu'], align_left)
                worksheet.write(th, 12, mediums[i]['medium_contract'], align_left)
                worksheet.write(th, 13, mediums[i]['medium_money2'] or '', align_left)
                worksheet.write(th, 14, mediums[i]['now_month_money_zhixing'], align_left)
                worksheet.write(th, 15, mediums[i]['now_month_medium_rebate_money'], align_left)
                worksheet.write(th, 19, orders[k]['start_date_cn'], align_left)
                worksheet.write(th, 20, orders[k]['end_date_cn'], align_left)
                th += 1
        else:
            if len(mediums) > 1:
                worksheet.merge_range(
                    th, 0, th + len(mediums) - 1, 0, orders[k]['locations_cn'], align_left)
                worksheet.merge_range(
                    th, 1, th + len(mediums) - 1, 1, orders[k]['contract'], align_left)
                worksheet.merge_range(
                    th, 2, th + len(mediums) - 1, 2, orders[k]['client_name'], align_left)
                worksheet.merge_range(
                    th, 3, th + len(mediums) - 1, 3, orders[k]['agent_name'], align_left)
                worksheet.merge_range(
                    th, 4, th + len(mediums) - 1, 4, orders[k]['campaign'], align_left)
                worksheet.merge_range(
                    th, 5, th + len(mediums) - 1, 5, orders[k]['money'], align_left)
                worksheet.merge_range(
                    th, 6, th + len(mediums) - 1, 6, orders[k]['back_moneys'], align_left)
                worksheet.merge_range(th, 7, th + len(mediums) - 1, 7,
                                      orders[k]['now_month_money_zhixing'], align_left)
                worksheet.merge_range(th, 8, th + len(mediums) - 1, 8,
                                      orders[k]['now_month_agent_rebate_money'], align_left)
                worksheet.merge_range(th, 9, th + len(mediums) - 1, 9,
                                      orders[k]['now_month_agent_real_rebate_money'], align_left)
                worksheet.merge_range(th, 16, th + len(mediums) - 1, 16, orders[
                                      k]['now_month_medium_real_rebate_money'], align_left)
                worksheet.merge_range(
                    th, 17, th + len(mediums) - 1, 17, orders[k]['profit_money'], align_left)
                worksheet.merge_range(
                    th, 18, th + len(mediums) - 1, 18, orders[k]['real_profit_money'], align_left)
                worksheet.merge_range(
                    th, 19, th + len(mediums) - 1, 19, orders[k]['start_date_cn'], align_left)
                worksheet.merge_range(
                    th, 20, th + len(mediums) - 1, 20, orders[k]['end_date_cn'], align_left)
                for i in range(len(mediums)):
                    worksheet.write(th, 10, mediums[i]['name'], align_left)
                    worksheet.write(th, 11, mediums[i]['now_month_money_kehu'], align_left)
                    worksheet.write(th, 12, mediums[i]['medium_contract'], align_left)
                    worksheet.write(th, 13, mediums[i]['medium_money2'] or '', align_left)
                    worksheet.write(th, 14, mediums[i]['now_month_money_zhixing'], align_left)
                    worksheet.write(th, 15, mediums[i]['now_month_medium_rebate_money'], align_left)
                    th += 1

            else:
                worksheet.write(th, 0, orders[k]['locations_cn'], align_left)
                worksheet.write(th, 1, orders[k]['contract'], align_left)
                worksheet.write(th, 2, orders[k]['client_name'], align_left)
                worksheet.write(th, 3, orders[k]['agent_name'], align_left)
                worksheet.write(th, 4, orders[k]['campaign'], align_left)
                worksheet.write(th, 5, orders[k]['money'], align_left)
                worksheet.write(th, 6, orders[k]['back_moneys'], align_left)
                worksheet.write(th, 7, orders[k]['now_month_money_zhixing'], align_left)
                worksheet.write(th, 8, orders[k]['now_month_agent_rebate_money'], align_left)
                worksheet.write(th, 9, orders[k]['now_month_agent_real_rebate_money'], align_left)
                if orders[k]['medium_data']:
                    worksheet.write(th, 10, orders[k]['medium_data'][0]['name'], align_left)
                    worksheet.write(th, 11, orders[k]['medium_data'][0]['now_month_money_kehu'], align_left)
                    worksheet.write(th, 12, orders[k]['medium_data'][0]['medium_contract'], align_left)
                    worksheet.write(th, 13, orders[k]['medium_data'][0]['medium_money2'], align_left)
                    worksheet.write(th, 14, orders[k]['medium_data'][0]['now_month_money_zhixing'], align_left)
                    worksheet.write(th, 15, orders[k]['medium_data'][0]['now_month_medium_rebate_money'], align_left)
                worksheet.write(th, 16, orders[k]['now_month_medium_real_rebate_money'], align_left)
                worksheet.write(th, 17, orders[k]['profit_money'], align_left)
                worksheet.write(th, 18, orders[k]['real_profit_money'], align_left)
                worksheet.write(th, 19, orders[k]['start_date_cn'], align_left)
                worksheet.write(th, 20, orders[k]['end_date_cn'], align_left)
                th += 1
    workbook.close()
    response.data = output.getvalue()
    filename = ("%s-%s.xls" %
                (u"Execution", datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    mimetype_tuple = mimetypes.guess_type(filename)
    response_headers = Headers({
        'Pragma': "public",
        'Expires': '0',
        'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
        'Cache-Control': 'private',
        'Content-Type': mimetype_tuple[0],
        'Content-Disposition': 'attachment; filename=\"%s\";' % filename,
        'Content-Transfer-Encoding': 'binary',
        'Content-Length': len(response.data)
    })
    response.headers = response_headers
    response.set_cookie('fileDownload', 'true', path='/')
    return response
