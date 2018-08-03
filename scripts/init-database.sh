#!/bin/bash

. $(dirname $0)/env.sh

cd "${ROOTDIR}"

# Clear database, migrations, etc.
./clean.sh

# Create database
${PYTHON} manage.py makemigrations
${PYTHON} manage.py migrate

# Create superuser
LOGIN='gamemaster'
MAIL='none@mail.com'
PASS='pbkdf2_sha256$100000$jdNRfA8s4xZc$QS9LDv1ntYYWSO445RL1aVeTFWwLcU2cLMLyuy1G0Lc='
DATE=$(date +"%Y-%m-%d %H:%M:%S.%6N")
sqlite3 ./db.sqlite3 "INSERT INTO 'auth_user' VALUES(1,'${PASS}',NULL,1,'${LOGIN}','','${MAIL}',1,1,'${DATE}','');"

# Populate database
${PYTHON} manage.py shell -c "

from escapegame.models import *

VideoPlayer(video_player='/usr/bin/mpv').save()
VideoPlayer(video_player='/usr/bin/omxplayer').save()

video_brief = Video(video_name='Video demo', video_path='test.h264')
video_brief.save()

game = EscapeGame(escape_game_name='1001 nuits', video_brief=video_brief)
game.save()

room1 = EscapeGameRoom(room_name='Fontaine', escape_game=game, door_pin=5)
room1.save()

room2 = EscapeGameRoom(room_name='Caverne', escape_game=game, door_pin=7)
room2.save()

chall1 = EscapeGameChallenge(challenge_name='room1-chall1', room=room1, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room1-chall2', room=room1, solved=False)
chall2.save()

chall1 = EscapeGameChallenge(challenge_name='room2-chall1', room=room2, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room2-chall2', room=room2, solved=False)
chall2.save()

game = EscapeGame(escape_game_name='Stranger Things', video_brief=video_brief)
game.save()

room1 = EscapeGameRoom(room_name='In the past', escape_game=game, door_pin=5)
room1.save()

room2 = EscapeGameRoom(room_name='In the future', escape_game=game, door_pin=7)
room2.save()

chall1 = EscapeGameChallenge(challenge_name='room1-chall1', room=room1, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room1-chall2', room=room1, solved=False)
chall2.save()

chall1 = EscapeGameChallenge(challenge_name='room2-chall1', room=room2, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room2-chall2', room=room2, solved=False)
chall2.save()"

