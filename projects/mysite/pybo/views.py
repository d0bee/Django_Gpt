from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
#from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .gpt import new_question_id, get_response
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

def index(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
        #return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            # 항시 대기보다 요청시 처리로 변경
            write_gpt(request, question.content)
            
            # ~ GPT
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

def write_gpt(request, new_content):
    new_question = get_object_or_404(Question, pk=new_question_id())
    form = AnswerForm()
    answer = form.save(commit=False)
    answer.content = get_response("아래 코드 최적화 해줘"+new_content)
    answer.author = request.user
    answer.create_date = timezone.now()
    answer.question = new_question
    answer.save()

