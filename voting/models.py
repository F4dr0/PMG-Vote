from django.contrib.auth.models import User
from django.db import models
from django.contrib import auth


# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def getCandidates(self):
        candidates = Candidate.objects.all()
        candidates_in_position = []
        for candidate in candidates:
            if candidate.position_id.pk == self.id:
                candidates_in_position.append(candidate)
        return candidates_in_position

    def getCandidatesNames(self):
        candidates = Candidate.objects.all()
        candidates_in_position = []
        for candidate in candidates:
            if candidate.position_id.pk == self.id:
                candidates_in_position.append(candidate.user_id.username)
        return candidates_in_position

class Candidate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    picture = models.CharField(max_length=250, default=None, blank=True, null=True)
    bio = models.CharField(max_length=250, default=None, blank=True, null=True)

    def __str__(self):
        return self.user_id

    def countVotes(self):
        votes = Vote.objects.all()
        count = 0
        for vote in votes:
            if vote.candidate_id.pk == self.id:
                count += 1
        return count


class Vote(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)


def isCandidate(self):
    candidates = Candidate.objects.all()
    for candidate in candidates:
        if candidate.user_id.pk == self.id:
            return True
    return False


def voted(self, position_id):
    positions = Position.objects.get(position_id)
    votes = Position.objects.all()
    for vote in votes:
        vote_for = Candidate.objects.get(vote.candidate_id)
        if vote_for.id == position_id:
            return True
    return False;


auth.models.User.add_to_class('isCandidate', isCandidate)
auth.models.User.add_to_class('voted', voted)