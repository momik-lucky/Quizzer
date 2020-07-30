from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from .forms import *
from .models import *


class HomeView(View):
    template_name = 'core/home.html'

    def get(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            return render(request, self.template_name, context={'user': current_user})
        return HttpResponseRedirect('login')


class LoginView(View):
    template_name = 'core/login.html'

    def get(self, request):
        form = LoginForm(request.POST)
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(self.request, user)
            return HttpResponseRedirect('/')
        return render(self.request, self.template_name, context={'form': form})


class RegistrationView(View):
    template_name = 'core/registration.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        return render(self.request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            avatar = form.cleaned_data['avatar']
            email = form.cleaned_data['email']
            birthday = form.cleaned_data['birthday']
            info = form.cleaned_data['info']
            new_user.save()
            return HttpResponseRedirect('/')
        return render(self.request, self.template_name, context={'form': form})


class TestsListView(LoginRequiredMixin, View):
    template_name = "core/tests_list.html"

    def get(self, request):
        # Tests searching
        search_text = request.GET.get('search', '')
        if search_text:
            tests_filter = Test.objects.filter(Q(title__contains=search_text) | Q(description__contains=search_text))
        else:
            tests_filter = Test.objects.all()

        # Tests sorting
        form = TestSortForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['sort_by']:
                tests_filter = tests_filter.order_by(form.cleaned_data['sort_by'])

        # Non passed tests
        if request.GET.get('no_passed_exam'):
            tests_filter = Test.objects.filter(examination__result__exact='-1')
        context = {
            'tests': tests_filter,
            'form': form
        }
        return render(request, self.template_name, context=context)


@login_required
def profile_view(request):
    current_user = request.user
    user_profile = AdvUser.objects.get(username=current_user)
    context = {
        'current_user': current_user,
        'user_profile': user_profile
    }
    return render(request, "core/profile.html", context=context)


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'core/logout.html')


class TestCreateView(View):
    template_name = 'core/test_create.html'

    def get(self, request):
        form = TestForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = TestForm(request.POST)

        if form.is_valid():
            new_test = form.save()
            new_test.author = request.user.username
            new_test.save()
            return redirect('/test_create/add_questions/')
        return render(request, self.template_name, context={'form': form})


class QuestionsCreateView(View):
    template_name = 'core/questions_create.html'

    def get(self, request):
        form = QuestionForm()
        test = Test.objects.order_by('id').last()
        question_quantity = range(1, test.question_quantity+1)
        context = {
            'form': form,
            'question_quantity': question_quantity,
            'test': test,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = QuestionForm(request.POST)
        test_id = self.request.POST.get('test_id')
        test_obj = Test.objects.get(id=test_id)
        print('form:', form)
        if form.is_valid():
            new_question = form.save(commit=False)
            question = form.cleaned_data['question']
            choise_1 = form.cleaned_data['choise_1']
            choise_2 = form.cleaned_data['choise_2']
            choise_3 = form.cleaned_data['choise_3']
            choise_4 = form.cleaned_data['choise_4']
            answer = form.cleaned_data['answer']
            new_question.test = test_obj
            new_question.save()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, context={'form': form})


class TestDetailView(View):
    template_name = 'core/test_detail.html'

    def get(self, request, test_slug_name):
        test = get_object_or_404(Test, slug=test_slug_name)
        attempts_counter = test.attempts_counter
        comments = test.comment.all()[::-1]
        form = CommentForm()
        current_user = AdvUser.objects.get(username=request.user)
        exam, exam_created = Examination.objects.get_or_create(
            user=current_user, test=test,
        )
        context = {
            'test': test,
            'comments': comments,
            'form': form,
            'number': attempts_counter,
            'current_user': current_user,
            'exam': exam,
        }
        return render(request, self.template_name, context=context)


class TestQuestionsView(LoginRequiredMixin, View):
    template_name = 'core/questions.html'
    answers_results = 0

    def get(self, request, test_slug_name):
        test = get_object_or_404(Test, slug=test_slug_name)
        questions = Question.objects.filter(test=test)
        context = {
            'test': test,
            'questions': questions,
        }
        return render(request, self.template_name, context)

    def post(self, request, test_slug_name):
        test = get_object_or_404(Test, slug=test_slug_name)
        current_user = AdvUser.objects.get(username=request.user)
        exam = Examination.objects.get(user=current_user, test=test)
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        radiobutton = request.POST.get('radio_choices')
        if str(radiobutton).lower() == str(question.answer).lower():
            exam.correct_answer_counter += 1

        exam.save()
        return render(request, self.template_name)


class CommentCreateView(View):
    def post(self, request):
        test_id = self.request.POST.get('test_id')
        comment_text = self.request.POST.get('comment')
        test_obj = Test.objects.get(id=test_id)
        new_comment = test_obj.comment.create(author=request.user, text=comment_text)

        comment = [{
            'author': new_comment.author.username,
            'text': new_comment.text,
            'created': new_comment.created.strftime('%b. %d, %Y, %I:%M %p')
        }]
        return JsonResponse(comment, safe=False)


class TestResultsView(LoginRequiredMixin, View):
    def get(self, request, test_slug_name):
        test = get_object_or_404(Test, slug=test_slug_name)
        current_user = AdvUser.objects.get(username=request.user)
        exam = Examination.objects.get(user=current_user, test=test)
        exam.result = exam.correct_answer_counter / test.question_quantity * 100
        exam.save()
        test.attempts_counter += 1
        test.save()
        context = {
            'current_user': current_user,
            'test': test,
            'exam': exam,
        }
        return render(request, 'core/result.html', context=context)
