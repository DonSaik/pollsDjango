from django.urls import path

from . import views

app_name = 'generateinfo'
urlpatterns = [
    path('<int:question_id>/downloadpdf', views.pdf_view, name='genpdf'),
    path('<int:question_id>/downloadexcel', views.excel_view, name='genexcel'),
]