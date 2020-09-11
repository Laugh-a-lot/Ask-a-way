from django.urls import path
from . import views
from .views import (QueListView,
                    AnswerDetailView,
                    AnswerCreateView,
                    QuestionCreateView,
                    QuestionUpdateView,
                    AnswerUpdateView,
                    QuestionDeleteView,
                    AnswerDeleteView,
                    UserQueListView)

urlpatterns = [
    path('', QueListView.as_view(), name='qna-home'),
    path('question/<int:pk>/update', QuestionUpdateView.as_view(), name='q-update'),
    path('question/new/', QuestionCreateView.as_view(), name='ask_question'),
    path('question/<int:pk>/', AnswerDetailView.as_view(), name='answers'),
    path('question/<str:username>/', UserQueListView.as_view(), name='user-answers'),
    path('question/<int:pk>/a_update', AnswerUpdateView.as_view(), name='a-update'),
    path('question/<int:pk>/delete', QuestionDeleteView.as_view(), name='q-delete'),
    path('question/<int:pk>/a_delete', AnswerDeleteView.as_view(), name='a-delete'),

    path('question/<int:pk>/add_answer/', AnswerCreateView.as_view(), name='add_answer'),

    path('about/', views.about, name='qna-about'),
]
