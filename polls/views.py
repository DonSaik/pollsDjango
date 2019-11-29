from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect

# Create your views here.
from .models import Question, Choice, Vote
from django.urls import reverse
from django.views import generic

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
    template_name = 'polls/polls.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Question.objects.all


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