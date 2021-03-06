# -*- coding: UTF-8 -*-
import StringIO
import mimetypes
import datetime

from flask import Response, g
from werkzeug.datastructures import Headers
import xlsxwriter


def _write_money_in_excel(worksheet, align_center, pre_monthes, th, money):
    start = 2
    for k in range(len(money)):
        worksheet.write(th, start + k, float(money[k]), align_center)
    worksheet.write(
        th, len(pre_monthes) * 4 + 2, float(sum(money)), align_center)
    th += 1
    return th


# 导出媒体清单
def write_medium_money_excel(pre_monthes, douban_money,
                             youli_money, wuxian_money,
                             momo_money, zhihu_money,
                             xiachufang_money, xueqiu_money,
                             huxiu_money, kecheng_money,
                             weipiao_money, one_money,
                             midi_money, other_money,
                             searchAD_money, rebate_order_money,
                             total, up_money, year):
    response = Response()
    response.status_code = 200
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    align_center = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'border': 1})
    # 设置宽度为30
    for k in range(0, len(pre_monthes) * 4 + 1):
        worksheet.set_column(k + 2, 2, 10)
    worksheet.set_column(1, 1, 30)
    # 设置高度
    for k in range(0, 76 + len(up_money) * 6):
        worksheet.set_row(k, 30)

    worksheet.merge_range(0, 0, 0, 1, u'时间', align_center)
    worksheet.merge_range(1, 0, 1, 1, u'媒体项目', align_center)
    worksheet.merge_range(2, 0, 76 + len(up_money) *
                          6, 0, u'致趣收入', align_center)

    locations = [u'媒介', u'华北', u'华东', u'华南']
    month_start, month_end = 2, 5
    location_end = 2
    for k in range(len(pre_monthes)):
        worksheet.merge_range(0, month_start, 0, month_end, str(
            pre_monthes[k]['month'].month) + u'月', align_center)
        for i in range(len(locations)):
            worksheet.write(1, location_end, locations[i], align_center)
            location_end += 1
        month_start, month_end = month_end + 1, month_end + 4
    worksheet.write(0, len(pre_monthes) * 4 + 2, u'合计', align_center)
    worksheet.write(1, len(pre_monthes) * 4 + 2, '', align_center)
    if g.user.is_aduit() and str(year) == '2014':
        keys = []
    else:
        keys = [{'CCFF99': [u'豆瓣执行收入', u'豆瓣服务费收入计提', u'豆瓣返点成本', u'豆瓣毛利', '']}]
    keys += [{'33CCFF': [
        u'陌陌收入', u'陌陌媒体执行金额', u'陌陌媒体净成本', u'陌陌代理成本', u'陌陌毛利', '']},
        {'0066FF': [
            u'知乎收入', u'知乎媒体执行金额', u'知乎媒体净成本', u'知乎代理成本', u'知乎毛利', '']},
        {'AA7700': [
            u'下厨房收入', u'下厨房媒体执行金额', u'下厨房媒体净成本', u'下厨房代理成本', u'下厨房毛利', '']},
        {'007799': [
            u'雪球收入', u'雪球媒体执行金额', u'雪球媒体净成本', u'雪球代理成本', u'雪球毛利', '']},
        {'9F88FF': [
            u'虎嗅收入', u'虎嗅媒体执行金额', u'虎嗅媒体净成本', u'虎嗅代理成本', u'虎嗅毛利', '']},
        {'FF8888': [
            u'课程格子收入', u'课程格子媒体执行金额', u'课程格子媒体净成本', u'课程格子代理成本', u'课程格子毛利', '']},
        {'FFBB00': [
            u'迷笛收入', u'迷笛媒体执行金额', u'迷笛媒体净成本', u'迷笛代理成本', u'迷笛毛利', '']},
        {'FF3333': [
            u'微票收入', u'微票媒体执行金额', u'微票媒体净成本', u'微票代理成本', u'微票毛利', '']},
        {'E93EFF': [
            u'ONE收入', u'One媒体执行金额', u'One媒体净成本', u'One代理成本', u'One毛利', '']}]
    for k, v in up_money.items():
        keys.append({'FF7F50': [k + u'收入', k + u'媒体执行金额',
                                k + u'媒体净成本', k + u'代理成本', k + u'毛利', '']})
    keys += [{'AAAAAA': [u'其他收入', u'其他媒体执行金额', u'其他媒体净成本', u'其他代理成本', u'其他毛利', '']},
             {'FF0088': [u'效果业务收入', u'效果业务返点收入', u'效果业务执行金额', u'效果业务代理成本', u'效果业务毛利']}]
    th = 2
    for k in keys:
        for i in k[k.keys()[0]]:
            align_center_color = workbook.add_format(
                {'align': 'center', 'valign': 'vcenter', 'border': 1, 'fg_color': '#' + k.keys()[0]})
            if i:
                worksheet.write(th, 1, i, align_center_color)
            else:
                worksheet.merge_range(
                    th, 1, th, 2 + len(pre_monthes) * 4, '', align_center)
            th += 1

    # 重置th
    th = 2
    if g.user.is_aduit() and str(year) == '2014':
        pass
    else:
        # 直签豆瓣
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, douban_money['sale_money'])
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, douban_money['money2'])
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, douban_money['a_rebate'])
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, douban_money['profit'])
        th += 1
    # 陌陌
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, momo_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, momo_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, momo_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, momo_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, momo_money['profit'])
    th += 1
    # 知乎
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, zhihu_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, zhihu_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, zhihu_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, zhihu_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, zhihu_money['profit'])
    th += 1
    # 下厨房
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xiachufang_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xiachufang_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xiachufang_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xiachufang_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xiachufang_money['profit'])
    th += 1
    # 雪球
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xueqiu_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xueqiu_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xueqiu_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xueqiu_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, xueqiu_money['profit'])
    th += 1
    # 虎嗅
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, huxiu_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, huxiu_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, huxiu_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, huxiu_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, huxiu_money['profit'])
    th += 1
    # 课程格子
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, kecheng_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, kecheng_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, kecheng_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, kecheng_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, kecheng_money['profit'])
    th += 1
    # 迷笛
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, midi_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, midi_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, midi_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, midi_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, midi_money['profit'])
    th += 1
    # 微票
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, weipiao_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, weipiao_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, weipiao_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, weipiao_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, weipiao_money['profit'])
    th += 1
    # One
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, one_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, one_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, one_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, one_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, one_money['profit'])
    th += 1

    # 大于100W的媒体
    for k, v in up_money.items():
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, v['sale_money'])
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, v['money2'])
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, v['m_ex_money'])
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, v['a_rebate'])
        th = _write_money_in_excel(
            worksheet, align_center, pre_monthes, th, v['profit'])
        th += 1

    # 其他
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, other_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, other_money['money2'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, other_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, other_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, other_money['profit'])
    th += 1
    # 搜索部门
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, searchAD_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, rebate_order_money['sale_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, searchAD_money['money2'])
    # th = _write_money_in_excel(
    # worksheet, align_center, pre_monthes, th, searchAD_money['m_ex_money'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, searchAD_money['a_rebate'])
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, searchAD_money['profit'])
    # 合计
    worksheet.write(th, 1, u'合计', align_center)
    th = _write_money_in_excel(
        worksheet, align_center, pre_monthes, th, total)
    workbook.close()
    response.data = output.getvalue()
    filename = ("%s-%s.xls" %
                ("媒体清单", datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
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


COLUMN_LIST = ['A', 'B', 'C', 'D', 'E']


# 导出可视化报表折线图
def write_line_excel(obj):
    response = Response()
    response.status_code = 200
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': 1})

    # Add the worksheet data that the charts will refer to.
    headings = obj['headings']
    data = obj['data']

    worksheet.write_row('A1', headings, bold)
    '''
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])
    worksheet.write_column('D2', data[3])
    '''
    # Create a new chart object. In this case an embedded chart.
    chart = workbook.add_chart({'type': 'line'})

    # 循环插入每条线，并减去第一组数据（第一组数据为月份的显示）
    for k in range(len(obj['data'])):
        worksheet.write_column(COLUMN_LIST[k] + '2', data[k])
        if k >= 1:
            worksheet.set_column(k, k, 25)
            chart.add_series({
                'name': ['Sheet1', 0, k],
                'categories': ['Sheet1', 1, 0, len(data[0]), 0],
                'values': ['Sheet1', 1, k, len(data[k]), k],
            })
    # Add a chart title and some axis labels.
    chart.set_title({'name': obj['title']})
    # chart.set_x_axis({'name': 'Test number'})
    # chart.set_y_axis({'name': 'Sample length (mm)'})

    # Set an Excel chart style. Colors with white outline and shadow.
    chart.set_style(10)

    # Insert the chart into the worksheet (with an offset).
    chart.set_size({'width': 600, 'height': 400})
    worksheet.insert_chart('E2', chart, {'x_offset': 40, 'y_offset': 10})

    workbook.close()

    response.data = output.getvalue()
    filename = ("%s-%s.xls" %
                (str(obj['title']), datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
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


# 导出可视化报表饼图
def write_pie_excel(obj):
    response = Response()
    response.status_code = 200
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    worksheet.set_column(1, 1, 30)
    worksheet.set_column(2, 2, 15)
    worksheet.set_column(3, 3, 10)
    bold = workbook.add_format({'bold': 1})

    # Add the worksheet data that the charts will refer to.
    headings = obj['headings']
    data = obj['data']

    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])
    worksheet.write_column('D2', data[3])

    #######################################################################
    #
    # Create a new chart object.
    #
    chart = workbook.add_chart({'type': 'pie'})

    # Configure the series. Note the use of the list syntax to define ranges:
    chart.add_series({
        'name': u'占比',
        'categories': ['Sheet1', 1, 1, len(data[1]), 1],
        'values': ['Sheet1', 1, 2, len(data[3]), 2],
    })

    # Add a title.
    chart.set_title({'name': obj['title']})

    # Set an Excel chart style. Colors with white outline and shadow.
    chart.set_style(10)

    # Insert the chart into the worksheet (with an offset).
    chart.set_size({'width': 700, 'height': 500})
    worksheet.insert_chart('E2', chart, {'x_offset': 25, 'y_offset': 10})
    workbook.close()

    response.data = output.getvalue()
    filename = ("%s-%s.xls" %
                (str(obj['title']), datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
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


# 导出代理总表
def write_agent_total_excel(year, agent_obj, total_is_sale_money, total_is_medium_money):
    response = Response()
    response.status_code = 200
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    align_left = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'border': 1})
    money_align_left = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'border': 1, 'num_format': '#,##0.00'})
    align_center = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'border': 1})
    keys = [u'代理集团', u'代理', u'合同号', 'campaign', u'销售金额', u'媒介金额']
    for k in range(len(keys)):
        worksheet.set_column(k, 0, 30)
        worksheet.write(0, k, keys[k], align_center)
    th = 1
    for k in agent_obj:
        agents = k['agents']
        if k['excel_order_count'] == 1:
            worksheet.write(th, 0, k['name'], align_left)
        else:
            worksheet.merge_range(th, 0, th + k['excel_order_count'] - 1, 0, k['name'], align_left)
        for a in agents:
            if a['orders']:
                if len(a['orders']) == 1:
                    worksheet.write(th, 1, a['name'], align_left)
                else:
                    worksheet.merge_range(th, 1, th + a['html_order_count'] - 1, 1, a['name'], align_left)
                for o in a['orders']:
                    worksheet.write(th, 2, o['contract'] or u'无合同号', align_left)
                    worksheet.write(th, 3, o['campaign'], align_left)
                    worksheet.write(th, 4, o['is_sale_money'], money_align_left)
                    worksheet.write(th, 5, o['is_medium_money'], money_align_left)
                    th += 1
    worksheet.merge_range(th, 0, th, 3, u'总计', align_center)
    worksheet.write(th, 4, total_is_sale_money, money_align_left)
    worksheet.write(th, 5, total_is_medium_money, money_align_left)
    workbook.close()
    response.data = output.getvalue()
    filename = ("%s-%s.xls" % ('代理总表', str(year)))
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


def _write_client_data_by_location(th, data, t_money, title, worksheet, align_left, money_align_left, align_center):
    location_th = th
    for k in data:
        industry_th = th
        for c in k['clients']:
            client_th = th
            if c['agents']:
                for a_k, a_v in c['agents'].items():
                    worksheet.write(th, 3, a_k, align_left)
                    for i in range(len(a_v)):
                        if i in [6, 16]:
                            worksheet.write(th, 4 + i, str(a_v[i]) + '%', align_left)
                        else:
                            worksheet.write(th, 4 + i, a_v[i], money_align_left)
                    th += 1
                if len(c['agents']) > 1:
                    worksheet.merge_range(client_th, 2, th - 1, 2, c['name'], align_left)
                else:
                    worksheet.write(th - 1, 2, c['name'], align_left)
            else:
                worksheet.write(th, 3, '', align_left)
                for i in range(17):
                    if i in [6, 16]:
                        worksheet.write(th, 4 + i, '0.00%', align_left)
                    else:
                        worksheet.write(th, 4 + i, 0.00, money_align_left)
                th += 1
                worksheet.write(th - 1, 2, c['name'], align_left)
        worksheet.merge_range(industry_th, 1, th - 1, 1, k['industry_name'], align_left)
    worksheet.merge_range(location_th, 0, th - 1, 0, title, align_left)
    worksheet.merge_range(th, 0, th, 3, u'总计', align_center)
    for i in range(len(t_money)):
        if i in [6, 16]:
            worksheet.write(th, 4 + i, str(t_money[i]) + "%", align_left)
        else:
            worksheet.write(th, 4 + i, t_money[i], money_align_left)
    th += 1
    return th


# 导出客户总表
def write_client_total_excel(year, data, money, location):
    response = Response()
    response.status_code = 200
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    align_left = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'border': 1})
    money_align_left = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'border': 1, 'num_format': '#,##0.00'})
    align_center = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'border': 1})
    worksheet.merge_range(0, 0, 1, 0, u'区域', align_center)
    worksheet.merge_range(0, 1, 1, 1, u'行业', align_center)
    worksheet.merge_range(0, 2, 1, 2, u'客户', align_center)
    worksheet.merge_range(0, 3, 1, 3, u'代理', align_center)
    worksheet.merge_range(0, 4, 0, 6, str(year - 2), align_center)
    worksheet.write(1, 4, u'新媒体', align_center)
    worksheet.write(1, 5, u'豆瓣', align_center)
    worksheet.write(1, 6, u'TOTAL', align_center)
    worksheet.merge_range(0, 7, 0, 10, str(year - 1), align_center)
    worksheet.write(1, 7, u'新媒体', align_center)
    worksheet.write(1, 8, u'豆瓣', align_center)
    worksheet.write(1, 9, u'TOTAL', align_center)
    worksheet.write(1, 10, u'增长率', align_center)
    worksheet.merge_range(0, 11, 0, 12, str(year) + u' Q1', align_center)
    worksheet.write(1, 11, u'新媒体', align_center)
    worksheet.write(1, 12, u'豆瓣', align_center)
    worksheet.merge_range(0, 13, 0, 14, str(year) + u' Q2', align_center)
    worksheet.write(1, 13, u'新媒体', align_center)
    worksheet.write(1, 14, u'豆瓣', align_center)
    worksheet.merge_range(0, 15, 0, 16, str(year) + u' Q3', align_center)
    worksheet.write(1, 15, u'新媒体', align_center)
    worksheet.write(1, 16, u'豆瓣', align_center)
    worksheet.merge_range(0, 17, 0, 18, str(year) + u' Q4', align_center)
    worksheet.write(1, 17, u'新媒体', align_center)
    worksheet.write(1, 18, u'豆瓣', align_center)
    worksheet.merge_range(0, 19, 0, 20, '', align_center)
    worksheet.write(1, 19, u'新媒体', align_center)
    worksheet.write(1, 20, u'豆瓣', align_center)
    # 设置宽度
    worksheet.set_column(1, 1, 15)
    worksheet.set_column(2, 2, 20)
    worksheet.set_column(3, 3, 40)
    worksheet.set_column(4, 20, 20)
    th = 2
    if location == 1:
        th = _write_client_data_by_location(th, data, money, u'华北', worksheet,
                                            align_left, money_align_left, align_center)
    elif location == 2:
        th = _write_client_data_by_location(th, data, money, u'华东', worksheet,
                                            align_left, money_align_left, align_center)
    elif location == 3:
        th = _write_client_data_by_location(th, data, money, u'华南', worksheet,
                                            align_left, money_align_left, align_center)

    worksheet = workbook.add_worksheet(u'统计图')
    bold = workbook.add_format({'bold': 1})
    headings = ['#', str(year - 2) + u'年新媒体', str(year - 2) + u'年豆瓣', str(year - 1) +
                u'年新媒体', str(year - 1) + u'年豆瓣', str(year) + u'年新媒体', str(year) + u'年豆瓣']
    categories = []
    series_b_y_client = []
    series_b_y_douban = []
    series_l_y_client = []
    series_l_y_douban = []
    series_n_y_client = []
    series_n_y_douban = []
    for k in data:
        for c in k['clients']:
            categories.append(c['name'])
            series_b_y_client.append(c['client_money'][0])
            series_b_y_douban.append(c['client_money'][1])
            series_l_y_client.append(c['client_money'][3])
            series_l_y_douban.append(c['client_money'][4])
            series_n_y_client.append(c['client_money'][7] + c['client_money'][9] +
                                     c['client_money'][11] + c['client_money'][13])
            series_n_y_douban.append(c['client_money'][8] + c['client_money'][10] +
                                     c['client_money'][12] + c['client_money'][14])
    data = [
        categories,
        series_b_y_client,
        series_b_y_douban,
        series_l_y_client,
        series_l_y_douban,
        series_n_y_client,
        series_n_y_douban,
    ]
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])
    worksheet.write_column('D2', data[3])
    worksheet.write_column('E2', data[4])
    worksheet.write_column('F2', data[5])
    worksheet.write_column('G2', data[6])
    chart1 = workbook.add_chart({'type': 'column'})
    # Configure a second series. Note use of alternative syntax to define ranges.
    chart1.add_series({
        'name': [u'统计图', 0, 1],
        'categories': [u'统计图', 1, 0, len(categories) / 2, 0],
        'values': [u'统计图', 1, 1, len(categories) / 2, 1],
    })
    chart1.add_series({
        'name': [u'统计图', 0, 2],
        'categories': [u'统计图', 1, 0, len(categories) / 2, 0],
        'values': [u'统计图', 1, 2, len(categories) / 2, 2],
    })
    chart1.add_series({
        'name': [u'统计图', 0, 3],
        'categories': [u'统计图', 1, 0, len(categories) / 2, 0],
        'values': [u'统计图', 1, 3, len(categories) / 2, 3],
    })
    chart1.add_series({
        'name': [u'统计图', 0, 4],
        'categories': [u'统计图', 1, 0, len(categories) / 2, 0],
        'values': [u'统计图', 1, 4, len(categories) / 2, 4],
    })
    chart1.add_series({
        'name': [u'统计图', 0, 5],
        'categories': [u'统计图', 1, 0, len(categories) / 2, 0],
        'values': [u'统计图', 1, 5, len(categories) / 2, 5],
    })
    chart1.add_series({
        'name': [u'统计图', 0, 6],
        'categories': [u'统计图', 1, 0, len(categories) / 2, 0],
        'values': [u'统计图', 1, 6, len(categories) / 2, 6],
    })
    # Add a chart title and some axis labels.
    chart1.set_title({'name': '区域客户分析'})
    chart1.set_x_axis({'name': '客户'})
    chart1.set_y_axis({'name': '执行额 (元)'})
    chart1.set_size({'width': 1720, 'height': 300})
    # Set an Excel chart style.
    chart1.set_style(110)

    chart2 = workbook.add_chart({'type': 'column'})
    chart2.add_series({
        'name': [u'统计图', 0, 1],
        'categories': [u'统计图', len(categories) / 2, 0, len(categories), 0],
        'values': [u'统计图', len(categories) / 2, 1, len(categories), 1],
    })
    chart2.add_series({
        'name': [u'统计图', 0, 2],
        'categories': [u'统计图', len(categories) / 2, 0, len(categories), 0],
        'values': [u'统计图', len(categories) / 2, 2, len(categories), 2],
    })
    chart2.add_series({
        'name': [u'统计图', 0, 3],
        'categories': [u'统计图', len(categories) / 2, 0, len(categories), 0],
        'values': [u'统计图', len(categories) / 2, 3, len(categories), 3],
    })
    chart2.add_series({
        'name': [u'统计图', 0, 4],
        'categories': [u'统计图', len(categories) / 2, 0, len(categories), 0],
        'values': [u'统计图', len(categories) / 2, 4, len(categories), 4],
    })
    chart2.add_series({
        'name': [u'统计图', 0, 5],
        'categories': [u'统计图', len(categories) / 2, 0, len(categories), 0],
        'values': [u'统计图', len(categories) / 2, 5, len(categories), 5],
    })
    chart2.add_series({
        'name': [u'统计图', 0, 6],
        'categories': [u'统计图', len(categories) / 2, 0, len(categories), 0],
        'values': [u'统计图', len(categories) / 2, 6, len(categories), 6],
    })
    # Add a chart title and some axis labels.
    chart2.set_title({'name': '区域客户分析'})
    chart2.set_x_axis({'name': '客户'})
    chart2.set_y_axis({'name': '执行额 (元)'})
    chart2.set_size({'width': 1720, 'height': 300})
    # Set an Excel chart style.
    chart2.set_style(110)
    # Insert the chart into the worksheet (with an offset).
    worksheet.insert_chart('I2', chart1, {'x_offset': 25, 'y_offset': 10})
    worksheet.insert_chart('I30', chart2, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
    response.data = output.getvalue()
    if location == 1:
        filename = ("%s-%s-%s.xls" % ('新媒体客户总表', str(year), '华北'))
    elif location == 2:
        filename = ("%s-%s-%s.xls" % ('新媒体客户总表', str(year), '华东'))
    elif location == 3:
        filename = ("%s-%s-%s.xls" % ('新媒体客户总表', str(year), '华南'))
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
