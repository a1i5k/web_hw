from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render
from .models import Question, Tag, Answer


def paginate(objects, request, per_page=5):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page')
    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        result_page = paginator.page(1)
    except EmptyPage:
        result_page = paginator.page(paginator.num_pages)
    return result_page


def index(request):
    question = paginate(Question.objects.get_new(), request)
    if question is None:
        raise Http404
    return render(request, 'index.html', {
        'questions': question
    }
                  )


def ask(request):
    return render(request, 'ask.html', {})


def login(request):
    return render(request, 'login.html', {})


def question(request):
    return render(request, 'question.html', {})


def register(request):
    return render(request, 'register.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, pk):
    received_tag = Tag.objects.get_by_tag(pk)
    if received_tag is None:
        return render(request, 'tag.html', {
            'tag': pk
        }
                      )
    question_tag = paginate(received_tag, request)
    if question_tag is None:
        raise Http404
    return render(request, 'tag.html', {
        'tag': pk,
        'questions': question_tag
    }
                  )


def one_question(request, pk):
    selected_question = Question.objects.get_by_id(pk).first()
    if selected_question is None:
        raise Http404
    answer = paginate(Answer.objects.get_answer(pk), request)
    answers_count = Answer.objects.get_count_answer(pk)
    return render(request, 'question.html', {
        'q': selected_question,
        'answers_count':  answers_count,
        'answers': answer
    }
                  )


def hot(request):
    hot_questions = paginate(Question.objects.get_hot(), request)
    if hot_questions is None:
        raise Http404

    return render(request, 'hot.html', {
        'questions': hot_questions
    }
                  )
