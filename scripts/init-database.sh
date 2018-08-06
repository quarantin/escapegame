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

room1 = EscapeGameRoom(room_name='Fontaine', escape_game=game, door_pin=7)
room1.save()

room2 = EscapeGameRoom(room_name='Caverne', escape_game=game, door_pin=9)
room2.save()

chall1 = EscapeGameChallenge(challenge_name='room1-chall1', room=room1, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room1-chall2', room=room1, solved=False)
chall2.save()

chall1 = EscapeGameChallenge(challenge_name='room2-chall1', room=room2, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room2-chall2', room=room2, solved=False)
chall2.save()

raspi = RaspberryPi(name='Raspi 1001-nuits', hostname='1001-nuits.local', port=80)
raspi.save()

url_validate = 'http://escapegame.local/1001-nuits/fontaine/room1-chall1/validate/'
url_reset = 'http://escapegame.local/1001-nuits/fontaine/room1-chall1/reset/'
remote_pin = RemoteChallengePin(name='Pin 1001-nuits salle fontaine chall 1', raspberrypi=raspi, challenge=chall1, pin_number=11, callback_url_validate=url_validate, callback_url_reset=url_reset)
remote_pin.save()

url_lock = 'http://escapegame.local/1001-nuits/fontaine/lock/'
url_unlock = 'http://escapegame.local/1001-nuits/fontaine/unlock/'
remote_pin = RemoteDoorPin(name='Pin 1001-nuits porte fontaine', raspberrypi=raspi, room=room1, pin_number=7, callback_url_lock=url_lock, callback_url_unlock=url_unlock)
remote_pin.save()

room1.room_controller = raspi
room1.save()

pin_number = 13
url_on = 'http://1001-nuits.local/api/led/on/%d/' % pin_number
url_off = 'http://1001-nuits.local/api/led/off/%d/' % pin_number
remote_pin = RemoteLedPin(name='Pin 1001-nuits led salle fontaine chall 2', raspberrypi=raspi, pin_number=pin_number, url_on=url_on, url_off=url_off)
remote_pin.save()

# Stranger Things
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

