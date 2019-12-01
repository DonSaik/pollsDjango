from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('polls/', views.PollsView.as_view(), name='polls'),
    path('<int:question_id>/', views.detail_view, name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('userpolls/', views.user_polls_view, name='user-polls'),
    path('createpoll/', views.user_polls_create_view, name='user-create-poll'),
    path('<int:question_id>/edit/', views.user_polls_edit_view, name='user-edit-poll'),
]