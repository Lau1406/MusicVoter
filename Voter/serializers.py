from rest_framework import serializers
from Voter.models import *


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ('name',)


class SongSerializer(serializers.HyperlinkedModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ('name', 'image', 'length_ms', 'uri', 'artists')


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
