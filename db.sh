#!/bin/bash

# Clear database
rm -f db.sqlite3

# Create database
python3 manage.py makemigrations
python3 manage.py migrate

# Populate database
python3 manage.py shell -c "
from video.models import VideoPlayer
from escapegame.models import EscapeGame, EscapeGameRoom, EscapeGameChallenge

VideoPlayer(video_player='mplayer').save()
VideoPlayer(video_player='omxplayer').save()

eg1 = EscapeGame(name='Mille et une nuits', video='test.h264')
eg1.save()

eg2 = EscapeGame(name='Mille et une nuits', video='test.h264')
eg2.save()

room1 = EscapeGameRoom(name='Fontaine', game=eg1, door_pin=3)
room1.save()

chall1 = EscapeGameChallenge(name='chall1', room=room1, solved=False)
chall1.save()"

python3 manage.py createsuperuser --user gamemaster --email none@mail.com
