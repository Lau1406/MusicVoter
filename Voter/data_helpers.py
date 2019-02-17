import spotipy
from spotipy import util
from Voter.models import *
import os

from Voter.serializers import SongSerializer


def get_update_data(user_pk):

    # Get current song
    # TODO: define this elsewhere?
    scope = 'user-modify-playback-state user-read-currently-playing'
    token = util.prompt_for_user_token(os.environ.get('SPOTIFY_USERNAME'), scope)

    if not token:
        return False

    sp = spotipy.Spotify(auth=token)

    track_data = sp.current_user_playing_track()['item']
    current_track, created = Song.objects.get_or_create(
        uri=track_data['uri'],
        defaults={
            'name': track_data['name'],
            'image': track_data['album']['images'][0]['url'],
            'length_ms': track_data['duration_ms'],
        },
    )

    if created:
        artists = track_data['artists']
        for artist in artists:
            artist, created = Artist.objects.get_or_create(
                uri=artist['uri'],
                defaults={
                    'name': artist['name'],
                }
            )
            current_track.artists.add(artist)

    # Get top X voted songs
    # For now all songs, jeee, what can possibly go wrong? All songs that have votes that is
    # Default order is by 'votes'
    # Get all songs that have at least one up or down vote
    songs = Song.objects.filter(Q(vote__upvote=Vote.UPVOTE) | Q(vote__upvote=Vote.DOWNVOTE))

    # Serialize the songs
    songs = SongSerializer(songs, many=True).data

    # Get all votes for each song for this user
    for song in songs:
        song['voted'] = Vote.objects.get(user=user_pk, song=song['uri']).upvote

    # Return data
    return {
        'current_song': SongSerializer(current_track).data,
        'voted_songs': songs
    }
