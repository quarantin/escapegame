from django.core.management.base import BaseCommand

from escapegame.models import *
from multimedia.models import *
from controllers.models import *

class Command(BaseCommand):

	def flush_database(self):

		all_models = [
			Image,
			Video,
			EscapeGame,
			EscapeGameRoom,
			EscapeGameChallenge,
			RaspberryPi,
			RemoteDoorPin,
			RemoteChallengePin,
		]

		for model in all_models:
			self.stdout.write('  Flushing model `%s`' % model.__name__, ending='')
			model.objects.all().delete()
			self.stdout.write(self.style.SUCCESS(' OK'))

	def handle(self, *args, **options):

		# We want to clear the database before populating it to avoid duplicate entries.
		self.stdout.write(self.style.MIGRATE_HEADING('Flushing database:'))
		self.flush_database()

		self.stdout.write(self.style.MIGRATE_HEADING('Populating database:'))

		#
		# Videos
		#

		# Video demo
		self.stdout.write('  Populating model `Video`', ending='')
		video = Video(video_name='Video demo', video_path='uploads/videos/test.h264')
		video.save()
		self.stdout.write(self.style.SUCCESS(' OK'))

		#
		# Images
		#

		self.stdout.write('  Populating model `Image`', ending='')
		# Full map image
		map_image = Image(image_name='Full Map', image_path='uploads/images/map-base.png')
		map_image.save()
		# SAS door image
		sas_door_image = Image(image_name='SAS Door', image_path='uploads/images/map-sas-door.png')
		sas_door_image.save()
		# Corridor door 1 image
		corridor_door_1_image = Image(image_name='Corridor Door 1', image_path='uploads/images/map-corridor-door-1.png')
		corridor_door_1_image.save()
		# Corridor door 2 image
		corridor_door_2_image = Image(image_name='Corridor Door 2', image_path='uploads/images/map-corridor-door-2.png')
		corridor_door_2_image.save()
		# Corridor door 3 image
		corridor_door_3_image = Image(image_name='Corridor Door 3', image_path='uploads/images/map-corridor-door-3.png')
		corridor_door_3_image.save()
		# SAS 1 door image
		sas1_door_image = Image(image_name='SAS 1 Door', image_path='uploads/images/map-sas1-door.png')
		sas1_door_image.save()
		# SAS 2 door image
		sas2_door_image = Image(image_name='SAS 2 Door', image_path='uploads/images/map-sas2-door.png')
		sas2_door_image.save()
		# SAS 3 door image
		sas3_door_image = Image(image_name='SAS 3 Door', image_path='uploads/images/map-sas3-door.png')
		sas3_door_image.save()
		# Room "La fontaine" door image
		room_fontain_door_image = Image(image_name='Door Room Fontain', image_path='uploads/images/map-door-room-fontain.png')
		room_fontain_door_image.save()
		# Room "Salle claire" door image
		room_salle_claire_door_image = Image(image_name='Door Room Salle Claire', image_path='uploads/images/map-door-room-salle-claire.png')
		room_salle_claire_door_image.save()
		# Room "Salle obscure" door image
		room_salle_obscure_door_image = Image(image_name='Door Room Salle Obscure', image_path='uploads/images/map-door-room-salle-obscure.png')
		room_salle_obscure_door_image.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

		#
		# Raspberry Pis
		#

		self.stdout.write('  Populating model `RaspberryPi`', ending='')
		# Raspberry Pi: Les 1001 nuits
		raspi_1001_nuits = RaspberryPi(name='Raspi 1001-nuits', hostname='1001-nuits.local')
		raspi_1001_nuits.save()
		# Raspberry Pi: Stranger Things
		raspi_stranger_things = RaspberryPi(name='Raspi Stranger Things', hostname='stranger-things.local')
		raspi_stranger_things.save()
		self.stdout.write(self.style.SUCCESS(' OK'))

		#
		# Escape games
		#

		self.stdout.write('  Populating model `EscapeGame`', ending='')
		# Escape game: Les 1001 nuits
		game_1001_nuits = EscapeGame(escapegame_name='Les 1001 nuits', video=video, raspberrypi=raspi_1001_nuits, map_image=map_image, sas_door_image=sas_door_image, corridor_door_image=corridor_door_1_image)
		game_1001_nuits.save()
		# Escape game: Stranger Things
		game_stranger_things = EscapeGame(escapegame_name='Stranger Things', video=video, raspberrypi=raspi_stranger_things, map_image=map_image, sas_door_image=sas_door_image, corridor_door_image=corridor_door_2_image)
		game_stranger_things.save()
		self.stdout.write(self.style.SUCCESS(' OK'))

		#
		# Rooms
		#
		self.stdout.write('  Populating model `EscapeGameRoom`', ending='')

		#
		# Escape Game SAS (3)
		#
		# Room: SAS les 1001 nuits
		room_sas_1001_nuits = EscapeGameRoom(room_name='SAS - Les 1001 nuits', escapegame=game_1001_nuits, door_pin=7, door_image=sas1_door_image)
		room_sas_1001_nuits.save()
		# Room: SAS Stranger Things - Salle Claire
		room_sas_salle_claire = EscapeGameRoom(room_name='SAS - Stranger Things - Salle Claire ', escapegame=game_stranger_things, door_pin=7, door_image=sas2_door_image)
		room_sas_salle_claire.save()
		# Room: SAS Stranger Things - Salle Obscure
		room_sas_salle_obscure = EscapeGameRoom(room_name='SAS - Stranger Things - Salle Obscure', escapegame=game_stranger_things, door_pin=10, door_image=sas3_door_image)
		room_sas_salle_obscure.save()


		# Challenge: Premier challenge du SAS les 1001 nuits
		room_sas_1001_nuits_chall = EscapeGameChallenge(challenge_name='Début du jeu', room=room_sas_1001_nuits)
		room_sas_1001_nuits_chall.save()
		# Challenge: début du jeu Stranger Things - Salle Claire
		room_sas_salle_claire_chall = EscapeGameChallenge(challenge_name='Début du jeu', room=room_sas_salle_claire)
		room_sas_salle_claire_chall.save()
		# Challenge: début du jeu Stranger Things - Salle Obscure
		room_sas_salle_obscure_chall = EscapeGameChallenge(challenge_name='Début du jeu', room=room_sas_salle_obscure)
		room_sas_salle_obscure_chall.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

		self.stdout.write('  Populating model `EscapeGameChallenge`', ending='')

		# Room: La fontaine
		room_fontaine = EscapeGameRoom(room_name='La fontaine', escapegame=game_1001_nuits, door_pin=7, door_image=room_fontain_door_image)
		room_fontaine.save()
		# Challenge: La fontaine
		chall_fontaine = EscapeGameChallenge(challenge_name='La fontaine', room=room_fontaine)
		chall_fontaine.save()
		# Challenge: Les dalles
		chall_dalles = EscapeGameChallenge(challenge_name='Les dalles', room=room_fontaine)
		chall_dalles.save()

		# Room: La caverne
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

		# Room: La salle claire
		room = EscapeGameRoom(room_name='La salle claire', escapegame=game_stranger_things, door_pin=7, door_image=room_salle_claire_door_image)
		room.save()
		# Challenge: 1 (Stranger Things / La salle claire)
		chall = EscapeGameChallenge(challenge_name='chall1', room=room)
		chall.save()
		# Challenge: 2 (Stranger Things / La salle claire)
		chall = EscapeGameChallenge(challenge_name='chall2', room=room)
		chall.save()

		# Room: La salle obscure
		room = EscapeGameRoom(room_name='La salle obscure', escapegame=game_stranger_things, door_pin=12, door_image=room_salle_obscure_door_image)
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

		self.stdout.write(self.style.SUCCESS(' OK'))

		# Remote door pin Les 1001 nuits / La fontaine
		#remote_door_pin_fontaine = RemoteDoorPin(name='Remote Door Pin: 1001-nuits / fontaine', raspberrypi=raspi_1001_nuits, room=room_fontaine)
		#remote_door_pin_fontaine.save()

		# Remote challenge pin Les 1001 nuits / La fontaine / La fontaine
		#remote_challenge_pin_fontaine = RemoteChallengePin(name='Remote Challenge Pin: 1001-nuits / fontaine', raspberrypi=raspi_1001_nuits, challenge=chall_fontaine)
		#remote_challenge_pin_fontaine.save()
