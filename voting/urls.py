from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.results, name="index"),
    path('positions/', views.position, name="position"),
    path('positions/delete/<int:id>', views.positionDelete, name="position_delete"),
    path('candidate', views.candidate, name="candidate"),
    path('candidate/delete/<int:id>', views.candidateDelete, name="candidate_delete"),
    path('vote', views.vote, name="vote"),
    path('vote/<int:id>', views.addVote, name="vote_add"),
    path('results/<int:id>/', views.voteResult, name="vote_results"),
]
