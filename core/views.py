from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Question, Answer
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class QueListView(ListView):
    model = Question
    template_name = 'core/home.html'
    context_object_name = 'questions'
    ordering = ['-asked_at']
    paginate_by = 3


class UserQueListView(ListView):
    model = Answer
    template_name = 'core/user-que.html'
    context_object_name = 'answers'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Answer.objects.filter(answered_by=user).order_by('-answering_time')


class AnswerDetailView(DetailView):
    model = Question


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer']
    context_object_name = 'answer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.filter(id=self.kwargs.get('pk')).first()
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['answer'].widget = forms.Textarea(attrs={'autocomplete': 'off'})
        return form

    def max_no_answers(self, form):
        que = Question.objects.filter(id=self.kwargs.get('pk')).first()
        if que.answer_set.filter(answered_by=self.request.user).count() >= 1:
            messages.warning(self.request, f'You have already answered this question. Try updating it.')
            return redirect('../')
        else:
            super().form_valid(form)

    def form_valid(self, form):
        form.instance.question_id = self.kwargs.get('pk')
        self.max_no_answers(form)
        return redirect('answers', form.instance.question_id)


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    fields = ['answer']
    success_url = '../'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['answer'].widget = forms.TextInput(attrs={'autocomplete': 'off'})
        return form

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.answered_by:
            return True
        else:
            return False


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    fields = ['answer']
    success_url = 'qna-home'

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.answered_by:
            return True
        else:
            return False


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['question'].widget = forms.TextInput(attrs={'autocomplete': 'off'})
        return form


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['question']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['question'].widget = forms.TextInput(attrs={'autocomplete': 'off'})
        return form

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.asked_by:
            return True
        else:
            return False


class QuestionDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    fields = ['question']
    success_url = "../../"
    success_message = 'successfully deleted.'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.asked_by:

            return True
        else:
            return False


def about(request):
    return render(request, 'core/about.html', {'title': 'home'})
