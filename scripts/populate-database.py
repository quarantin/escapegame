from escapegame.models import *

VideoPlayer(video_player_name='Media Player', video_player_path='/usr/bin/mpv').save()
VideoPlayer(video_player_name='OMX Player', video_player_path='/usr/bin/omxplayer').save()

video_brief = Video(video_name='Video demo', video_path='test.h264')
video_brief.save()

raspi = RaspberryPi(name='Raspi 1001-nuits', hostname='1001-nuits.local', port=80)
raspi.save()

game = EscapeGame(escapegame_name='1001 nuits', video_brief=video_brief)
game.save()

room1 = EscapeGameRoom(room_name='Fontaine', escapegame=game, door_pin=7)
room1.raspberrypi = raspi
room1.save()

room2 = EscapeGameRoom(room_name='Caverne', escapegame=game, door_pin=9)
room2.save()

chall1 = EscapeGameChallenge(challenge_name='room1-chall1', room=room1, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room1-chall2', room=room1, solved=False)
chall2.save()

chall1 = EscapeGameChallenge(challenge_name='room2-chall1', room=room2, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room2-chall2', room=room2, solved=False)
chall2.save()

url_validate = 'http://escapegame.local/1001-nuits/fontaine/room1-chall1/validate/'
url_reset = 'http://escapegame.local/1001-nuits/fontaine/room1-chall1/reset/'
remote_pin = RemoteChallengePin(name='Pin 1001-nuits salle fontaine chall 1', raspberrypi=raspi, challenge=chall1, pin_number=11, url_callback_validate=url_validate, url_callback_reset=url_reset)
remote_pin.save()

url_lock = 'http://escapegame.local/1001-nuits/fontaine/lock/'
url_unlock = 'http://escapegame.local/1001-nuits/fontaine/unlock/'
remote_pin = RemoteDoorPin(name='Pin 1001-nuits porte fontaine', raspberrypi=raspi, room=room1, pin_number=7, url_callback_lock=url_lock, url_callback_unlock=url_unlock)
remote_pin.save()

pin_number = 13
url_on = 'http://1001-nuits.local/api/led/on/%d/' % pin_number
url_off = 'http://1001-nuits.local/api/led/off/%d/' % pin_number
remote_pin = RemoteLedPin(name='Pin 1001-nuits led salle fontaine chall 2', raspberrypi=raspi, pin_number=pin_number, url_on=url_on, url_off=url_off)
remote_pin.save()

# Stranger Things
game = EscapeGame(escapegame_name='Stranger Things', video_brief=video_brief)
game.save()

room1 = EscapeGameRoom(room_name='In the past', escapegame=game, door_pin=5)
room1.save()

room2 = EscapeGameRoom(room_name='In the future', escapegame=game, door_pin=7)
room2.save()

chall1 = EscapeGameChallenge(challenge_name='room1-chall1', room=room1, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room1-chall2', room=room1, solved=False)
chall2.save()

chall1 = EscapeGameChallenge(challenge_name='room2-chall1', room=room2, solved=False)
chall1.save()
chall2 = EscapeGameChallenge(challenge_name='room2-chall2', room=room2, solved=False)
chall2.save()

