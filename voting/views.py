from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import Context
from django.shortcuts import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage

from voting.forms import *


def results(request):
    votes = Vote.objects.all()
    candidates = Candidate.objects.all()
    positions = Position.objects.all()
    user_voted_category = []
    for vote in votes:
        if vote.user_id.pk == request.user.id:
            candidate = Candidate.objects.get(pk=vote.candidate_id.pk)
            user_voted_category.append(candidate.position_id.pk)
    candidates_names = []
    candidates_votes = []
    vote_result = {}
    for position in positions:
        pos_votes = []
        for candidate in position.getCandidates():
            pos_votes.append(candidate.countVotes())
        vote_result[position.id] = {'candidates': position.getCandidatesNames(), 'votes': pos_votes}

    context = {'candidates': candidates, 'user_voted': user_voted_category, 'positions': positions, 'result': vote_result}
    return render(request, 'voting/results.html', context)


def check_admin(user):
    return user.is_superuser


@user_passes_test(check_admin)
def position(request):
    form = PositionForm()

    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/voting/positions')

    context = {'positions': Position.objects.all(), 'formAdd': form}

    return render(request, 'voting/admin/positions.html', context)


@user_passes_test(check_admin)
def positionDelete(request, id):
    position = Position.objects.get(pk=id)
    position.delete()
    return redirect('/voting/positions')


@login_required(login_url='/login')
def candidate(request):
    form = CandidateForm()
    form.fields['user_id'].widget = forms.HiddenInput()
    if request.method == 'POST':
        myfile = request.FILES['picture']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        data_dic = {
            'position_id': request.POST['position_id'],
            'user_id': request.user.id,
            'bio': request.POST['bio'],
            'picture': uploaded_file_url
        }
        form = CandidateForm(data_dic)
        if form.is_valid():
            form.save()
            return redirect('/voting/candidate')
        else:
            print(form.errors)

    context = {'candidates': Candidate.objects.all(), 'formAdd': form}

    return render(request, 'voting/candidate.html', context)


@login_required(login_url='/login')
def candidateDelete(request, id):
    candidate = Candidate.objects.get(pk=id)
    candidate.delete()
    return redirect('/voting/candidate')


@login_required(login_url='/login')
def vote(request):
    positions = Position.objects.all()
    votes = Vote.objects.all()
    user_voted_category = []
    for vote in votes:
        if vote.user_id.pk == request.user.id:
            candidate = Candidate.objects.get(pk=vote.candidate_id.pk)
            user_voted_category.append(candidate.position_id.pk)
    context = {'candidates': Candidate.objects.all(), 'positions': positions, 'user_voted': user_voted_category}

    return render(request, 'voting/vote.html', context)


@login_required(login_url='/login')
def addVote(request, id):
    data_dic = {
        'user_id': request.user.id,
        'candidate_id': id
    }
    form = VoteForm(data_dic)
    if form.is_valid():
        form.save()
    return redirect('/voting/')


def voteResult(request, id):
    position = Position.objects.get(pk=id)
    vote_result = []
    candidates = position.getCandidates()
    for candidate in candidates:
        vote_result.append({candidate.user_id.username: candidate.countVotes()})
    return JsonResponse(vote_result, safe=False)

def getPositionsId(request):
    positions = Position.objects.all()
    position_id = []
    for position in positions:
        position_id.append(position.id)
    return JsonResponse(position_id, safe=False)