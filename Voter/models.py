from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import ugettext


class Artist(models.Model):
    name = models.CharField(max_length=200)
    uri = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=1000)
    artists = models.ManyToManyField(Artist, blank=True)
    length_ms = models.PositiveIntegerField()
    uri = models.CharField(max_length=200, primary_key=True)
    votes = models.IntegerField(default=0)

    def has_votes(self):
        # Get all votes that are not NEUTRAL and check if the amount is not equal to 0
        return Vote.objects.filter(Q(song=self.pk) & ~Q(upvote=Vote.NEUTRAL)).count() != 0

    def __str__(self):
        return self.name

    # def vote(self, vote: Vote):
    #     # TODO: implement actual voting procedure
    #     self.votes += 1


class Vote(models.Model):
    UPVOTE = '1'
    NEUTRAL = '0'
    DOWNVOTE = '-1'

    VOTES = (
        (UPVOTE, ugettext('Upvote')),
        (NEUTRAL, ugettext('Neutral')),
        (DOWNVOTE, ugettext('Downvote')),
    )

    class Meta:
        unique_together = ('user', 'song')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvote = models.CharField(max_length=1, choices=VOTES, default=NEUTRAL)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return self.song.name + " - " + self.user.username
