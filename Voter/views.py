from django.http import HttpResponse
from django.template import loader
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from spotipy.oauth2 import SpotifyClientCredentials
from Voter.serializers import *
import spotipy


def index(request):
    template = loader.get_template('voter/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def spotify_search(request):
    # TODO: make robust

    query = request.data['query']
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = sp.search(query)
    songs = []

    for result in results['tracks']['items']:
        song, created = Song.objects.get_or_create(
            uri=result['uri'],
            defaults={
                'name': result['name'],
                'image': result['album']['images'][0]['url'],
                'length_ms': result['duration_ms'],
            },
        )
        songs.append(song)

        artists = result['artists']
        for artist in artists:
            artist, created = Artist.objects.get_or_create(
                uri=artist['uri'],
                defaults={
                    'name': artist['name'],
                }
            )
            song.artists.add(artist)

    serializer = SongSerializer(songs, context={'request': request}, many=True)
    return Response(serializer.data)
