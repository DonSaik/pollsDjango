from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect

# Create your views here.
from .models import Question, Choice, Vote
from django.urls import reverse
from django.views import generic
from polls.forms import PollForm, ChoiceFormset
from django.contrib.auth.models import User, Group
from django.http import Http404


# def index(request):
#     latest_poll_list = Question.objects.order_by('-created_at')[:5]
#     output = ','.join([q.question_text for q in latest_poll_list])
#     return  render(request, 'polls/index.html', {'latest_poll_list': latest_poll_list})
#
#
# def detail(request, question_id):
#     question= get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     response = "Yourre looking %s"
#     return HttpResponse(response % question_id)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-created_at')[:5]


class PollsView(generic.ListView):
    model = Question
    template_name = 'polls/polls.html'
    context_object_name = 'latest_poll_list'
    paginate_by = 7

    def get_queryset(self):
        return Question.objects.filter()


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    checked_choice = None

    if request.user.is_authenticated:
        if Vote.objects.filter(user=request.user, question=question).exists():
            checked_choice = Vote.objects.get(user=request.user, question=question).choice

    return render(request, 'polls/detail.html', {
        'question': question,
        'checked_choice': checked_choice,
    })


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if not Vote.objects.filter(user=request.user, question=question).exists():
            new_vote = Vote()
            new_vote.question = question
            new_vote.choice = selected_choice
            new_vote.user = request.user
            new_vote.save()
            question.vote = new_vote
            question.save()
            print(question.vote.question)
            print(question.vote.user)
            print(question.vote.choice)
            selected_choice.votes += 1
            selected_choice.save()
        else:
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You have already voted.",
            })
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@login_required
def user_polls_view(request):

    question_list = Question.objects.filter(user=request.user)

    print(question_list[0])
    return render(request, 'polls/user/userpolls.html', {
        'questions': question_list,
    })


@login_required
def user_polls_create_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PollForm(request.POST)
        formset = ChoiceFormset(request.POST)
        # check whether it's valid:
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            for form in formset:
                # so that `book` instance can be attached.
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
            return render(request, 'polls/detail.html', {
                'question': question})

        # if a GET (or any other method) we'll create a blank form
    else:
        form = PollForm()

    return render(request, 'polls/user/createpoll.html',
                  {'formPoll': form, 'formset': ChoiceFormset(queryset=Choice.objects.none()),
                   })


@login_required
def user_polls_edit_view(request, question_id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        current_question = Question.objects.get(id=question_id)
        form = PollForm(request.POST, instance=current_question)
        current_choices = Choice.objects.filter(question=current_question)
        formset = ChoiceFormset(request.POST, instance=current_question)
        # check whether it's valid:
        if form.is_valid() and formset.is_valid:
            question = form.save(commit=False)
            question.save()
            for form in formset:
                # so that `book` instance can be attached.
                choice = form.save(commit=False)
                choice.save()
            return render(request, 'polls/detail.html', {
                'question': question})

        # if a GET (or any other method) we'll create a blank form

    try:
        my_record = Question.objects.get(id=question_id)
        form = PollForm(instance=my_record)
        formset = ChoiceFormset(instance=my_record)
    except KeyError:
        HttpResponse("Something went wrong!")

    return render(request, 'polls/user/editpoll.html',
                  {'formPoll': form, 'formset': formset,
                   'question': my_record,
                   })