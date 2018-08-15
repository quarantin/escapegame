from escapegame.models import *
from multimedia.models import *

#VideoPlayer(video_player_name='Media Player', video_player_path='/usr/bin/mpv').save()
#VideoPlayer(video_player_name='OMX Player', video_player_path='/usr/bin/omxplayer').save()

# Videos

video_brief = Video(video_name='Video demo', video_path='test.h264')
video_brief.save()

# Raspberry Pis Les 1001 nuits

raspi_1001_nuits = RaspberryPi(name='Raspi 1001-nuits', hostname='1001-nuits.local', port=80)
raspi_1001_nuits.save()

#
# Escape game: Les 1001 nuits
#
game_1001_nuits = EscapeGame(escapegame_name='Les 1001 nuits', video_brief=video_brief)
game_1001_nuits.save()

# Room La fontaine

room_fontaine = EscapeGameRoom(room_name='La fontaine', escapegame=game_1001_nuits, door_pin=7, raspberrypi=raspi_1001_nuits)
room_fontaine.save()

# Challenge: La fontaine

chall_fontaine = EscapeGameChallenge(challenge_name='La fontaine', room=room_fontaine)
chall_fontaine.save()

# Challenge: Les dalles

chall_dalles = EscapeGameChallenge(challenge_name='Les dalles', room=room_fontaine)
chall_dalles.save()

# Room La caverne

room_caverne = EscapeGameRoom(room_name='La caverne', escapegame=game_1001_nuits, door_pin=12)
room_caverne.save()

# Challenge: Le marchand

chall_marchand = EscapeGameChallenge(challenge_name='Le marchand', room=room_caverne)
chall_marchand.save()

# Challenge: Le lanceur de couteaux

chall_couteux = EscapeGameChallenge(challenge_name='Le lanceur de couteaux', room=room_caverne)
chall_couteux.save()

# Challenge: Le charmeur de serpents

chall_serpents = EscapeGameChallenge(challenge_name='Le charmeur de serpents', room=room_caverne)
chall_serpents.save()

# Challenge: Le fakir

chall_fakir = EscapeGameChallenge(challenge_name='Le fakir', room=room_caverne)
chall_fakir.save()

# Room: La lampe

room_lampe = EscapeGameRoom(room_name='La lampe', escapegame=game_1001_nuits, door_pin=13)
room_lampe.save()

# Challenge La lampe

chall_lampe = EscapeGameChallenge(challenge_name='La lampe', room=room_lampe)
chall_lampe.save()

# Raspberry Pis Stranger Things

raspi_stranger_things = RaspberryPi(name='Raspi Stranger Things', hostname='stranger-things.local', port=80)
raspi_stranger_things.save()

#
# Escape game: Stranger Things
#
game_stranger_things = EscapeGame(escapegame_name='Stranger Things', video_brief=video_brief)
game_stranger_things.save()

# Room: La salle claire

room = EscapeGameRoom(room_name='La salle claire', escapegame=game_stranger_things, door_pin=7)
room.save()

# Challenge: 1 (Stranger Things / La salle claire)

chall = EscapeGameChallenge(challenge_name='chall1', room=room)
chall.save()

# Challenge: 2 (Stranger Things / La salle claire)

chall = EscapeGameChallenge(challenge_name='chall2', room=room)
chall.save()

# Room: La salle obscure

room = EscapeGameRoom(room_name='La salle obscure', escapegame=game_stranger_things, door_pin=12)
room.save()

# Challenge: 1 (Stranger Things / La salle obscure)

chall = EscapeGameChallenge(challenge_name='chall1', room=room)
chall.save()

# Challenge: 2 (Stranger Things / La salle obscure)

chall = EscapeGameChallenge(challenge_name='chall2', room=room)
chall.save()

# Room: La forêt

room = EscapeGameRoom(room_name='La forêt', escapegame=game_stranger_things, door_pin=13)
room.save()

# Challenge: 1 (Stranger Things / La forêt)

chall = EscapeGameChallenge(challenge_name='chall1', room=room)
chall.save()

# Challenge: 2 (Stranger Things / La forêt)

chall = EscapeGameChallenge(challenge_name='chall2', room=room)
chall.save()

# Remote door pin Les 1001 nuits / La fontaine

#url_lock = 'http://escapegame.local/1001-nuits/fontaine/lock/'
#url_unlock = 'http://escapegame.local/1001-nuits/fontaine/unlock/'
#remote_pin = RemoteDoorPin(name='Pin 1001-nuits porte fontaine', raspberrypi=raspi_1001_nuits, room=room1, url_callback_lock=url_lock, url_callback_unlock=url_unlock)
remote_door_pin_fontaine = RemoteDoorPin(name='Remote Door Pin: 1001-nuits / fontaine', raspberrypi=raspi_1001_nuits, room=room_fontaine)
remote_door_pin_fontaine.save()

# Remote challenge pin Les 1001 nuits / La fontaine / La fontaine

#url_validate = 'http://escapegame.local/1001-nuits/fontaine/room1-chall1/validate/'
#url_reset = 'http://escapegame.local/1001-nuits/fontaine/room1-chall1/reset/'
#remote_pin = RemoteChallengePin(name='Pin 1001-nuits salle fontaine chall 1', raspberrypi=raspi_1001_nuits, challenge=chall1)
remote_challenge_pin_fontaine = RemoteChallengePin(name='Remote Challenge Pin: 1001-nuits / fontaine', raspberrypi=raspi_1001_nuits, challenge=chall_fontaine)
remote_challenge_pin_fontaine.save()

