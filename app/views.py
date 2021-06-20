from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F
from django.forms.utils import ErrorList
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import *
from app.forms import *


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '%s' % ''.join(['<div class="error">%s</div>' % e for e in self])


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


@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            tags = form.clean()['tag']

            tags = tags.replace(' ', '')
            parsed_tag = []
            while tags.find(',') != -1:
                tag = tags[:tags.find(',')]
                parsed_tag.append(tag)
                tags = tags[tags.find(',') + 1:]

            if tags:
                parsed_tag.append(tags)

            new_tags = []
            for tag in parsed_tag:
                check_tag = Tag.objects.get_tag(tag)
                if check_tag is None:
                    check_tag = Tag.objects.create(text=tag)
                new_tags.append(check_tag.id)
            question.tag.set(new_tags)
            return redirect(reverse('question', kwargs={"pk": question.pk}))
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {"form": form})


def login(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                url = request.GET.get('next', '/')
                return redirect(url)
            else:
                error = 'Sorry, wrong login or password!'
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'error': error,
        'form': form
    }
                  )


def logout(request):
    auth.logout(request)
    url = request.GET.get('next', '/')
    return redirect(url)


def question(request):
    return render(request, 'question.html', {})


def register(request):
    error = []
    if request.method == 'POST':
        form = RegisterForm(data=request.POST, auto_id=False, error_class=DivErrorList)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['login']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            new_user.profile.nickname = form.cleaned_data['nickname']
            auth.login(request, new_user)
            return redirect(reverse('new'))
        else:
            for err in form.errors['__all__']:
                error.append(err)

    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'error': error,
        'form': form
    }
                  )


@login_required
def settings(request, pk):
    error = []
    if request.method == 'POST':
        user = User.objects.get(id=Profile.objects.get(nickname=pk).user.id)
        form = SettingsForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            new_settings = form.save(commit=False)
            if form.cleaned_data['login']:
                new_settings.username = form.cleaned_data['login']
            if form.cleaned_data['email']:
                new_settings.email = form.cleaned_data['email']
            new_settings.save()
            new_profile = Profile.objects.get(user=request.user)
            if form.cleaned_data['nickname']:
                new_profile.nickname = form.cleaned_data['nickname']
            if form.cleaned_data['avatar']:
                new_profile.avatar = form.cleaned_data['avatar']
            new_profile.save()
            return redirect(reverse('settings', kwargs={"pk": new_profile.nickname}))
        else:
            for err in form.errors['__all__']:
                error.append(err)
    else:
        form = SettingsForm()
    return render(request, 'settings.html', {
        'login': pk,
        'form': form,
        'error': error
    }
                  )


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

    if request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.author = request.user
            new_answer.question = selected_question
            new_answer.save()
            return redirect(reverse('question', kwargs={"pk": pk}) + '#' + str(new_answer.id))
    else:
        form = AnswerForm()

    return render(request, 'question.html', {
        'q': selected_question,
        'answers_count': answers_count,
        'answers': answer,
        'form': form
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


@login_required
@require_POST
def vote(request):
    data = request.POST
    qid = data['qid']
    action = data['action']
    q = Question.objects.get(pk=qid)
    inc = Like.ACTION[action]
    grade = Like.objects.get_like_by_content(ContentType.objects.get_for_model(q), qid, request.user)

    if grade:
        if inc == grade.rating:
            return JsonResponse({'status': 'already voted', 'rating': q.rating})
        else:
            q.rating = F('rating') + 2 * inc
            grade.rating = inc
            q.save()
            grade.save()
            q.refresh_from_db()
            return JsonResponse({'status': 'changed', 'rating': q.rating})
    like = Like.objects.create(user=request.user,
                               content_type=ContentType.objects.get_for_model(q),
                               rating=inc, object_id=qid)
    like.save()
    q.rating = F('rating') + inc
    q.save()
    q.refresh_from_db()

    return JsonResponse({'status': 'ok', 'rating': q.rating})


@login_required
@require_POST
def vote_answer(request):
    data = request.POST
    aid = data['aid']
    action = data['action']
    a = Answer.objects.get(pk=aid)
    inc = Like.ACTION[action]
    grade = Like.objects.get_like_by_content(ContentType.objects.get_for_model(a), aid, request.user)

    if grade:
        if inc == grade.rating:
            return JsonResponse({'status': 'already voted', 'rating': a.rating})
        else:
            a.rating = F('rating') + 2 * inc
            grade.rating = inc
            a.save()
            grade.save()
            a.refresh_from_db()
            return JsonResponse({'status': 'changed', 'rating': a.rating})
    like = Like.objects.create(user=request.user,
                               content_type=ContentType.objects.get_for_model(a),
                               rating=inc, object_id=aid)
    like.save()
    a.rating = F('rating') + inc
    a.save()
    a.refresh_from_db()

    return JsonResponse({'status': 'ok', 'rating': a.rating})


@login_required
@require_POST
def vote_correct(request):
    data = request.POST
    aid = data['aid']
    qid = data['qid']
    incorrect = ''
    for e in Answer.objects.get_answer(qid):
        if e.correct and e.id != aid:
            e.correct = False
            e.save()
            incorrect = e.id
            break
    a = Answer.objects.get(pk=aid)
    if a.correct:
        a.correct = False
    else:
        a.correct = True
    a.save()
    a.refresh_from_db()

    return JsonResponse({'status': 'ok', 'correct': a.correct, 'incorrect': incorrect})
