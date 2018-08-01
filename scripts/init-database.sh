#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

cd siteconfig
rm -f settings.py
ln -s settings.bootstrap.py settings.py
cd ..

# Clear database
rm -f db.sqlite3

# Create database
${PYTHON} manage.py makemigrations
${PYTHON} manage.py migrate

# Populate database
${PYTHON} manage.py shell -c "

from escapegame.models import EscapeGame, EscapeGameRoom, EscapeGameChallenge, VideoPlayer

VideoPlayer(video_player='/usr/bin/mplayer').save()
VideoPlayer(video_player='/usr/bin/omxplayer').save()

game = EscapeGame(name='1001 nuits', video_path='test.h264')
game.save()

room1 = EscapeGameRoom(name='Fontaine', game=game, door_pin=5)
room1.save()

room2 = EscapeGameRoom(name='Caverne', game=game, door_pin=7)
room2.save()

chall1 = EscapeGameChallenge(name='room1-chall1', room=room1, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(name='room1-chall2', room=room1, solved=False)
chall2.save()

chall1 = EscapeGameChallenge(name='room2-chall1', room=room2, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(name='room2-chall2', room=room2, solved=False)
chall2.save()

game = EscapeGame(name='Stranger Things', video_path='test.h264')
game.save()

room1 = EscapeGameRoom(name='In the past', game=game, door_pin=5)
room1.save()

room2 = EscapeGameRoom(name='In the future', game=game, door_pin=7)
room2.save()

chall1 = EscapeGameChallenge(name='room1-chall1', room=room1, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(name='room1-chall2', room=room1, solved=False)
chall2.save()

chall1 = EscapeGameChallenge(name='room2-chall1', room=room2, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(name='room2-chall2', room=room2, solved=False)
chall2.save()

"
${PYTHON} manage.py createsuperuser --user gamemaster --email none@mail.com

cd siteconfig
rm -f settings.py
ln -s settings.real.py settings.py
cd ..
