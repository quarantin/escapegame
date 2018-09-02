# -*- coding: utf-8 -*-

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
		]

		self.stdout.write(self.style.MIGRATE_HEADING('Flushing database:'))

		for model in all_models:

			self.stdout.write('  Flushing model `%s`' % model.__name__, ending='')

			try:
				model.objects.all().delete()
				self.stdout.write(self.style.SUCCESS(' OK'))
			except:
				self.stdout.write(self.style.SUCCESS(' MISSING'))

	def handle(self, *args, **options):

		EscapeGame.from_shell = True

		# We want to clear the database before populating it to avoid duplicate entries.
		self.flush_database()

		self.stdout.write(self.style.MIGRATE_HEADING('Populating database:'))

#
# Videos
#
		self.stdout.write('  Populating model `Video`', ending='')

		# Demo video
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

		# SAS 1 door image
		door_sas1_image = Image(image_name='SAS 1 Door', image_path='uploads/images/map-sas1-door.png')
		door_sas1_image.save()

		# SAS 2 door image
		door_sas2_image = Image(image_name='SAS 2 Door', image_path='uploads/images/map-sas2-door.png')
		door_sas2_image.save()

		# SAS 3 door image
		door_sas3_image = Image(image_name='SAS 3 Door', image_path='uploads/images/map-sas3-door.png')
		door_sas3_image.save()

		# Room "La fontaine" door image
		door_room_fontain_image = Image(image_name='Door Room Fontain', image_path='uploads/images/map-door-room-fontain.png')
		door_room_fontain_image.save()

		# Room "Salle claire" door image
		door_room_claire_image = Image(image_name='Door Room Salle Claire', image_path='uploads/images/map-door-room-salle-claire.png')
		door_room_claire_image.save()

		# Room "Salle obscure" door image
		door_room_obscure_image = Image(image_name='Door Room Salle Obscure', image_path='uploads/images/map-door-room-salle-obscure.png')
		door_room_obscure_image.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Raspberry Pis
#
		self.stdout.write('  Populating model `RaspberryPi`', ending='')

		# Raspberry Pi: Master game controller
		raspi_master = RaspberryPi(name='Raspi Master', hostname='escapegame.local')
		raspi_master.save()

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
		game_1001_nuits = EscapeGame(escapegame_name='Les 1001 nuits', video=video, raspberrypi=raspi_1001_nuits, map_image=map_image)
		game_1001_nuits.save()

		# Escape game: Stranger Things
		game_stranger_things = EscapeGame(escapegame_name='Stranger Things', video=video, raspberrypi=raspi_stranger_things, map_image=map_image)
		game_stranger_things.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Rooms
#
		self.stdout.write('  Populating model `EscapeGameRoom`', ending='')

		# Room: SAS 1 - Les 1001 nuits
		room_sas_1 = EscapeGameRoom(escapegame=game_1001_nuits, door_pin=7, door_image=door_sas1_image, room_name='SAS 1 - Les 1001 nuits')
		room_sas_1.has_cube = True
		room_sas_1.save()

		# Room: La fontaine
		room_fontaine = EscapeGameRoom(escapegame=game_1001_nuits, door_pin=11, door_image=door_room_fontain_image, room_name='La fontaine')
		room_fontaine.save()

		# Room: La caverne
		room_caverne = EscapeGameRoom(escapegame=game_1001_nuits, door_pin=12, door_image=None, room_name='La caverne')
		room_caverne.save()

		# Room: La lampe
		room_lampe = EscapeGameRoom(escapegame=game_1001_nuits, door_pin=13, door_image=None, room_name='La lampe')
		room_lampe.save()

		# Room: SAS 2 - Stranger Things - Salle Claire
		room_sas_2 = EscapeGameRoom(escapegame=game_stranger_things, door_pin=7, door_image=door_sas2_image, room_name='SAS 2 - Stranger Things - Salle Claire ')
		room_sas_2.has_cube = True
		room_sas_2.save()

		# Room: SAS 3 - Stranger Things - Salle Obscure
		room_sas_3 = EscapeGameRoom(escapegame=game_stranger_things, door_pin=11, door_image=door_sas3_image, room_name='SAS 3 - Stranger Things - Salle Obscure')
		room_sas_3.has_cube = True
		room_sas_3.save()

		# Room: La salle claire
		room_claire = EscapeGameRoom(escapegame=game_stranger_things, door_pin=12, door_image=door_room_claire_image, room_name='La salle claire')
		room_claire.save()

		# Room: La salle obscure
		room_obscure = EscapeGameRoom(escapegame=game_stranger_things, door_pin=13, door_image=door_room_obscure_image, room_name='La salle obscure')
		room_obscure.save()

		# Room: La forêt
		room_foret = EscapeGameRoom(escapegame=game_stranger_things, door_pin=15, room_name='La forêt')
		room_foret.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Timers
#
		self.stdout.write('  Populating model `EscapeGameChallenge` (timers)', ending='')

		# Challenge: Timer, premier challenge du SAS Les 1001 nuits
		chall_sas_1_timer = EscapeGameChallenge(room=room_sas_1, challenge_name='Début du jeu \'Les 1001 nuits\'')
		chall_sas_1_timer.save()

		# Challenge: Timer, premier challenge du SAS Stranger Things - Salle claire
		chall_sas_2_timer = EscapeGameChallenge(room=room_sas_2, challenge_name='Début du jeu \'Stanger Things - Salle claire\'')
		chall_sas_2_timer.save()

		# Challenge: Timer, premier challenge du SAS Stranger Things - Salle obscure
		chall_sas_3_timer = EscapeGameChallenge(room=room_sas_3, challenge_name='Début du jeu \'Stranger Things - Salle obscure\'')
		chall_sas_3_timer.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Challenges
#
		self.stdout.write('  Populating model `EscapeGameChallenge`', ending='')

		# Challenge: La fontaine
		chall_fontaine = EscapeGameChallenge(room=room_fontaine, challenge_name='La fontaine')
		chall_fontaine.save()

		# Challenge: Les dalles
		chall_dalles = EscapeGameChallenge(room=room_fontaine, challenge_name='Les dalles')
		chall_dalles.save()

		# Challenge: Le marchand
		chall_marchand = EscapeGameChallenge(room=room_caverne, challenge_name='Le marchand')
		chall_marchand.save()

		# Challenge: Le lanceur de couteaux
		chall_couteux = EscapeGameChallenge(room=room_caverne, challenge_name='Le lanceur de couteaux')
		chall_couteux.save()

		# Challenge: Le charmeur de serpents
		chall_serpents = EscapeGameChallenge(room=room_caverne, challenge_name='Le charmeur de serpents')
		chall_serpents.save()

		# Challenge: Le fakir
		chall_fakir = EscapeGameChallenge(room=room_caverne, challenge_name='Le fakir')
		chall_fakir.save()

		# Challenge La lampe
		chall_lampe = EscapeGameChallenge(room=room_lampe, challenge_name='La lampe')
		chall_lampe.save()

		# Challenge: 1 (Stranger Things / La salle claire)
		chall = EscapeGameChallenge(room=room_claire, challenge_name='chall1 (salle claire)')
		chall.save()

		# Challenge: 2 (Stranger Things / La salle claire)
		chall = EscapeGameChallenge(room=room_claire, challenge_name='chall2 (salle claire)')
		chall.save()

		# Challenge: 1 (Stranger Things / La salle obscure)
		chall = EscapeGameChallenge(room=room_obscure, challenge_name='chall1 (salle obscure)')
		chall.save()

		# Challenge: 2 (Stranger Things / La salle obscure)
		chall = EscapeGameChallenge(room=room_obscure, challenge_name='chall2 (salle obscure)')
		chall.save()

		# Challenge: 1 (Stranger Things / La forêt)
		chall = EscapeGameChallenge(room=room_foret, challenge_name='chall1 (la forêt)')
		chall.save()

		# Challenge: 2 (Stranger Things / La forêt)
		chall = EscapeGameChallenge(room=room_foret, challenge_name='chall2 (la forêt)')
		chall.save()

		self.stdout.write(self.style.SUCCESS(' OK'))
