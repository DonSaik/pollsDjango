from django.shortcuts import get_object_or_404
from polls.models import Question
import io
from django.http import HttpResponse, FileResponse
from xlwt import Borders
from django.template.loader import get_template
from django.utils import timezone
import xhtml2pdf.pisa as pisa
import xlwt
import datetime
# Create your views here.


def pdf_view(request, question_id):
    datalist = get_object_or_404(Question, pk=question_id)
    today = timezone.now()
    params = {
        'today': today,
        'data': datalist,
    }
    template = get_template('generateinfo/generatepdf.html')
    html = template.render(params)
    buffer = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=str(datalist.id)+".pdf")


def excel_view(request,  question_id):
    datalist = get_object_or_404(Question, pk=question_id)
    today = datetime.datetime.now()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Question')
    # Sheet header, first row

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'Mmm dd, yyyy, h:mm AM/PM'
    row_num = 1
    ws.write(row_num, 0, today, date_format)
    row_num = 3
    columns = ['ID', 'Question text', 'Created at', 'Groups', ]
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    borders = Borders()
    borders.top = Borders.THIN
    borders.bottom = Borders.THIN
    font_style.borders = borders
    date_format.borders = borders
    data = Question.objects.all().values_list('id', 'question_text', 'created_at')
    row_num += 1
    ws.write (row_num, 0, datalist.id, font_style)
    ws.write(row_num, 1, datalist.question_text, font_style)
    ws.write(row_num , 2, datalist.created_at.replace(tzinfo=None), date_format)
    for row in datalist.groups.all():
        ws.write(row_num, 3, row.name, font_style)
        row_num += 1
    # xlwt.easyxf("borders: left thin, right thin, top thin, bottom thin;")
    row_num += 1
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Choices', 'Votes', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    borders = Borders()
    borders.top = Borders.THIN
    borders.bottom = Borders.THIN
    font_style.borders = borders
    for row in datalist.choice_set.all():
        row_num += 1
        ws.write(row_num, 0, row.choice_text, font_style)
        ws.write(row_num, 1, row.vote_set.count(), font_style)

    for colx in range(0, 5):
        width = 10000
        ws.col(colx).width = width
    wb.save(response)
    return response