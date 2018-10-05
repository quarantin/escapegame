# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from escapegame.models import *
from multimedia.models import *
from controllers.models import *

from datetime import timedelta


class Command(BaseCommand):

	def flush_database(self):

		all_models = [
			Image,
			MultimediaFile,
			RaspberryPi,   # RaspberryPi before Controller (parent model)
			Controller,
			ChallengeGPIO, # ChallengeGPIO before GPIO (parent model)
			DoorGPIO,      # DoorGPIO before GPIO (parent model)
			LiftGPIO,      # LiftGPIO before GPIO (parent model)
			GPIO,
			EscapeGameChallenge,
			EscapeGameRoom,
			EscapeGameCube,
			EscapeGame,
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
# Raspberry Pis
#
		self.stdout.write('  Populating model `RaspberryPi`', ending='')

		# Raspberry Pi: Master game controller
		raspi_master = RaspberryPi(name='Game Master', hostname='escapegame.local', media_type='video')
		raspi_master.save()

		# Raspberry Pi: Les 1001 nuits - Sons bruitages et lampes
		raspi_1001_nuits = RaspberryPi(name='Les 1001 nuits - Sons, bruitages et lampes', hostname='les-1001-nuits.local', media_type='audio')
		raspi_1001_nuits.save()

		# Raspberry Pi: Les 1001 nuits - Sons - La fontaine
		raspi_1001_nuits_sons_fontaine = RaspberryPi(name='Les 1001 nuits - Sons - La fontaine', hostname='les-1001-nuits-sons-fontaine.local', media_type='audio')
		raspi_1001_nuits_sons_fontaine.save()

		# Raspberry Pi: Les 1001 nuits - Sons - La caverne
		raspi_1001_nuits_sons_caverne = RaspberryPi(name='Les 1001 nuits - Sons - La caverne ', hostname='les-1001-nuits-sons-caverne.local', media_type='audio')
		raspi_1001_nuits_sons_caverne.save()

		# Raspberry Pi: Stranger Things - Sons et bruitages
		raspi_stranger_things = RaspberryPi(name='Stranger Things - Sons et bruitages', hostname='stranger-things.local', media_type='audio')
		raspi_stranger_things.save()

		# Raspberry Pi: Stranger Things - Sons - Salle claire/obscure
		raspi_stranger_things_sons_claire_obscure = RaspberryPi(name='Stranger Things - Sons - Salle claire/obscure', hostname='stranger-things-sons-claire-obscure.local', media_type='audio')
		raspi_stranger_things_sons_claire_obscure.save()

		# Raspberry Pi: Stranger Things - Sons - La forêt
		raspi_stranger_things_sons_foret = RaspberryPi(name='Stranger Things - Sons - La forêt', hostname='stranger-things-sons-la-foret.local', media_type='audio')
		raspi_stranger_things_sons_foret.save()

		# Raspberry Pi: Stranger Things - Le monstre
		raspi_stranger_things_le_monstre = RaspberryPi(name='Stranger Things - Le monstre', hostname='stranger-things-le-monstre.local', media_type='video')
		raspi_stranger_things_le_monstre.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Images
#

		self.stdout.write('  Populating model `Image`', ending='')

		# Full map image
		map_image = Image(name='Escape Game Map - Full Map', path='uploads/images/map-base.png')
		map_image.save()

		# Door briefing room image
		door_briefing_room_image = Image(name='Door briefing room', path='uploads/images/door-briefing-room.png')
		door_briefing_room_image.save()

		# Door corridor SAS 1
		door_corridor_sas_1_image = Image(name='Door corridor SAS 1', path='uploads/images/door-corridor-sas-1.png')
		door_corridor_sas_1_image.save()

		# Door corridor SAS 2
		door_corridor_sas_2_image = Image(name='Door corridor SAS 2', path='uploads/images/door-corridor-sas-2.png')
		door_corridor_sas_2_image.save()

		# Door corridor SAS 3
		door_corridor_sas_3_image = Image(name='Door corridor SAS 3', path='uploads/images/door-corridor-sas-3.png')
		door_corridor_sas_3_image.save()

		# SAS 1 door image
		door_sas_1_image = Image(name='Les 1001 nuits - SAS Door', path='uploads/images/door-sas-1.png')
		door_sas_1_image.save()

		# SAS 2 door image
		door_sas_2_image = Image(name='Stranger Things - SAS Door - Salle Claire', path='uploads/images/door-sas-2.png')
		door_sas_2_image.save()

		# SAS 3 door image
		door_sas_3_image = Image(name='Stranger Things - SAS Door - Salle Obscure', path='uploads/images/door-sas-3.png')
		door_sas_3_image.save()

		# Room "La Fontaine" door image
		door_fontain_room_image = Image(name='Les 1001 nuits - La Fontaine Door', path='uploads/images/door-fontain-room.png')
		door_fontain_room_image.save()

		# Room "Salle obscure" door image
		door_salle_obscure_image = Image(name='Stranger Things - Salle Obscure Door', path='uploads/images/door-salle-obscure.png')
		door_salle_obscure_image.save()

		# Room "Salle claire" door image
		door_salle_claire_image = Image(name='Stranger Things - Salle Claire Door', path='uploads/images/door-salle-claire.png')
		door_salle_claire_image.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Videos
#
		self.stdout.write('  Populating model `MultimediaFile`', ending='')

		# Demo audio
		audio_demo = MultimediaFile(name='Audio Demo', path='uploads/media/test.h264', media_type='audio')
		audio_demo.save()

		# Demo video
		video_demo = MultimediaFile(name='Video Demo', path='uploads/media/test.h264')
		video_demo.save()

		# Demo video 2
		video_demo_2 = MultimediaFile(name='Video Demo 2', path='uploads/media/small.mp4')
		video_demo_2.save()

		# Les 1001 nuits - Briefing Video
		video_les_1001_nuits_briefing = MultimediaFile(name='Les 1001 nuits - Briefing', path='uploads/media/test.h264')
		video_les_1001_nuits_briefing.save()

		# Les 1001 nuits - Winners Video
		video_les_1001_nuits_winners = MultimediaFile(name='Les 1001 nuits - Good End', path='uploads/media/test.h264')
		video_les_1001_nuits_winners.save()

		# Les 1001 nuits - Losers Video
		video_les_1001_nuits_losers = MultimediaFile(name='Les 1001 nuits - Bad End', path='uploads/media/test.h264')
		video_les_1001_nuits_losers.save()

		# Stranger Things - Salle obscure - Briefing Video
		video_stranger_things_briefing_salle_obscure = MultimediaFile(name='Stranger Things - Salle obscure - Briefing', path='uploads/media/test.h264')
		video_stranger_things_briefing_salle_obscure.save()

		# Stranger Things - Salle claire - Briefing Video
		video_stranger_things_briefing_salle_claire = MultimediaFile(name='Stranger Things - Salle claire - Briefing', path='uploads/media/test.h264')
		video_stranger_things_briefing_salle_claire.save()

		# Stranger Things - Winners Video
		video_stranger_things_winners = MultimediaFile(name='Stranger Things - Good End', path='uploads/media/test.h264')
		video_stranger_things_winners.save()

		# Stranger Things - Losers Video
		video_stranger_things_losers = MultimediaFile(name='Stranger Things - Bad End', path='uploads/media/test.h264')
		video_stranger_things_losers.save()

		# Stranger Things - Challenge Video - La forêt
		video_la_foret = MultimediaFile(name='Stranger Things - Challenge - La Forêt', path='uploads/media/test.h264')
		video_la_foret.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Escape games
#
		self.stdout.write('  Populating model `EscapeGame`', ending='')

		# Escape game: Les 1001 nuits
		time_limit_1001_nuits = timedelta(hours=1)
		game_1001_nuits = EscapeGame(
			name='Les 1001 nuits',
			time_limit=time_limit_1001_nuits,
			controller=raspi_1001_nuits,
			map_image=map_image)

		game_1001_nuits.save()

		raspi_1001_nuits.game = game_1001_nuits
		raspi_1001_nuits.save()


		raspi_1001_nuits_sons_fontaine.game = game_1001_nuits
		raspi_1001_nuits_sons_fontaine.save()

		raspi_1001_nuits_sons_caverne.game = game_1001_nuits
		raspi_1001_nuits_sons_caverne.save()

		# Escape game: Stranger Things
		time_limit_stranger_things = timedelta(hours=1)
		game_stranger_things = EscapeGame(
			name='Stranger Things',
			time_limit=time_limit_stranger_things,
			controller=raspi_stranger_things,
			map_image=map_image)

		game_stranger_things.save()

		raspi_stranger_things.game = game_stranger_things
		raspi_stranger_things.save()

		raspi_stranger_things_sons_claire_obscure.game = game_stranger_things
		raspi_stranger_things_sons_claire_obscure.save()


		raspi_stranger_things_sons_foret.game = game_stranger_things
		raspi_stranger_things_sons_foret.save()


		raspi_stranger_things_le_monstre.game = game_stranger_things
		raspi_stranger_things_le_monstre.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Cubes
#
		cube_1001_nuits = EscapeGameCube(
			name='Cube des 1001 nuits',
			tag_id='FF000001',
			game=game_1001_nuits,
			briefing_media=video_les_1001_nuits_briefing,
			winners_media=video_les_1001_nuits_winners,
			losers_media=video_les_1001_nuits_losers)
		cube_1001_nuits.save()

		cube_obscur = EscapeGameCube(
			name='Cube Stranger Things - Parcours obscur',
			tag_id='FF000002',
			game=game_stranger_things,
			briefing_media=video_stranger_things_briefing_salle_obscure,
			winners_media=video_stranger_things_winners,
			losers_media=video_stranger_things_losers)
		cube_obscur.save()

		cube_clair = EscapeGameCube(
			name='Cube Stranger Things - Parcours clair',
			tag_id='FF000003',
			game=game_stranger_things,
			briefing_media=video_stranger_things_briefing_salle_claire,
			winners_media=video_stranger_things_winners,
			losers_media=video_stranger_things_losers)
		cube_clair.save()
#
# Rooms
#
		self.stdout.write('  Populating model `EscapeGameRoom`', ending='')

		#
		# Les 1001 nuits
		#

		# Room: La salle de briefing des 1001 nuits
		room_briefing_1001_nuits = EscapeGameRoom(game=game_1001_nuits, controller=raspi_master, door_image=door_briefing_room_image, name='La salle de briefing des 1001 nuits')
		room_briefing_1001_nuits.save()

		# Room: Le couloir des 1001 nuits
		room_corridor_sas_1 = EscapeGameRoom(game=game_1001_nuits, controller=raspi_1001_nuits, door_image=door_corridor_sas_1_image, name='Le couloir des 1001 nuits', dependent_on=room_briefing_1001_nuits, has_no_challenge=True)
		room_corridor_sas_1.save()

		# Room: Le SAS des 1001 nuits (SAS 1)
		room_sas_1 = EscapeGameRoom(game=game_1001_nuits, door_image=door_sas_1_image, name='Le SAS des 1001 nuits', dependent_on=room_corridor_sas_1, starts_the_timer=True)
		room_sas_1.save()

		# Room: La fontaine
		room_fontaine = EscapeGameRoom(game=game_1001_nuits, door_image=door_fontain_room_image, name='La fontaine', dependent_on=room_sas_1)
		room_fontaine.save()

		# Room: La caverne
		room_caverne = EscapeGameRoom(game=game_1001_nuits, door_image=None, name='La caverne', dependent_on=room_fontaine)
		room_caverne.save()

		# Room: La lampe
		room_lampe = EscapeGameRoom(game=game_1001_nuits, door_image=None, name='La lampe', dependent_on=room_caverne)
		room_lampe.save()

		# Room: Retour au SAS des 1001 nuits (SAS 1)
		room_sas_1_retour = EscapeGameRoom(game=game_1001_nuits, door_image=door_corridor_sas_1_image, name='Retour au SAS des 1001 nuits', dependent_on=room_lampe, stops_the_timer=True)
		room_sas_1_retour.save()

		# Room: Le couloir des 1001 nuits (Retour)
		room_corridor_sas_1_retour = EscapeGameRoom(game=game_1001_nuits, controller=raspi_1001_nuits, door_image=door_briefing_room_image, name='Retour dans le couloir des 1001 nuits', dependent_on=room_sas_1_retour, has_no_challenge=True)
		room_corridor_sas_1_retour.save()

		# Room: Retour dans la salle de briefing des 1001 nuits
		room_briefing_1001_nuits_retour = EscapeGameRoom(game=game_1001_nuits, controller=raspi_master, door_image=None, name='Retour dans la salle de briefing des 1001 nuits', dependent_on=room_corridor_sas_1_retour)
		room_briefing_1001_nuits_retour.save()

		#
		# Stranger Things
		#

		# Room: La salle de briefing de Stranger Things - Parcours obscur
		room_briefing_stranger_things_obscur = EscapeGameRoom(game=game_stranger_things, controller=raspi_master, door_image=door_briefing_room_image, name='La salle de briefing de Stranger Things - Parcours obscur')
		room_briefing_stranger_things_obscur.save()

		# Room: La salle de briefing de Stranger Things - Parcours clair
		room_briefing_stranger_things_clair = EscapeGameRoom(game=game_stranger_things, controller=raspi_master, door_image=door_briefing_room_image, name='La salle de briefing de Stranger Things - Parcours clair')
		room_briefing_stranger_things_clair.save()

		# Room: Le couloir de Stranger Things - Parcours obscur
		room_corridor_sas_2 = EscapeGameRoom(game=game_stranger_things, controller=raspi_stranger_things, door_image=door_corridor_sas_2_image, name='Le couloir de Stranger Things - Parcours obscur', dependent_on=room_briefing_stranger_things_obscur, has_no_challenge=True)
		room_corridor_sas_2.save()

		# Room: Le couloir de Stranger Things - Parcours clair
		room_corridor_sas_3 = EscapeGameRoom(game=game_stranger_things, controller=raspi_stranger_things, door_image=door_corridor_sas_3_image, name='Le couloir de Stranger Things - Parcours clair', dependent_on=room_briefing_stranger_things_clair, has_no_challenge=True)
		room_corridor_sas_3.save()

		# Room: Le SAS obscur de Stranger Things (SAS 2)
		room_sas_2 = EscapeGameRoom(game=game_stranger_things, door_image=door_sas_2_image, name='Le SAS obscur', dependent_on=room_corridor_sas_2, starts_the_timer=True)
		room_sas_2.save()

		# Room: Le SAS clair de Stranger Things (SAS 3)
		room_sas_3 = EscapeGameRoom(game=game_stranger_things, door_image=door_sas_3_image, name='Le SAS clair', dependent_on=room_corridor_sas_3, starts_the_timer=True)
		room_sas_3.save()

		# Room: La salle obscure
		room_obscure = EscapeGameRoom(game=game_stranger_things, door_image=door_salle_obscure_image, name='La salle obscure', dependent_on=room_sas_2)
		room_obscure.save()

		# Room: La salle claire
		room_claire = EscapeGameRoom(game=game_stranger_things, door_image=door_salle_claire_image, name='La salle claire', dependent_on=room_sas_3)
		room_claire.save()

		# Room: La forêt
		room_foret = EscapeGameRoom(game=game_stranger_things, name='La forêt', dependent_on=room_obscure)
		room_foret.save()

		# Room: Retour au SAS obscur (SAS 2)
		room_sas_2_retour = EscapeGameRoom(game=game_stranger_things, door_image=door_corridor_sas_2_image, name='Retour au SAS obscur', dependent_on=room_foret, stops_the_timer=True)
		room_sas_2_retour.save()

		# Room: Retour au SAS clair (SAS 3)
		room_sas_3_retour = EscapeGameRoom(game=game_stranger_things, door_image=door_corridor_sas_3_image, name='Retour au SAS clair', dependent_on=room_foret, stops_the_timer=True)
		room_sas_3_retour.save()

		# Room: Le couloir de Stranger Things - Parcours obscur (Retour)
		room_corridor_sas_2_retour = EscapeGameRoom(game=game_stranger_things, controller=raspi_stranger_things, door_image=door_briefing_room_image, name='Retour dans le couloir de Stranger Things - Parcours obscur', dependent_on=room_sas_2_retour, has_no_challenge=True)
		room_corridor_sas_2_retour.save()

		# Room: Le couloir de Stranger Things - Parcours clair (Retour)
		room_corridor_sas_3_retour = EscapeGameRoom(game=game_stranger_things, controller=raspi_stranger_things, door_image=door_briefing_room_image, name='Retour dans le couloir de Stranger Things - Parcours clair', dependent_on=room_sas_3_retour, has_no_challenge=True)
		room_corridor_sas_3_retour.save()

		# Room: Salle de briefing - Stranger Things (Retour)
		room_briefing_stranger_things_retour = EscapeGameRoom(game=game_stranger_things, controller=raspi_master, door_image=None, name='Retour dans la salle de briefing de Stranger Things', dependent_on=room_corridor_sas_2_retour)
		room_briefing_stranger_things_retour.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Challenges
#
		self.stdout.write('  Populating model `EscapeGameChallenge`', ending='')

		# Cube Challenge: Salle de briefing des 1001 nuits - Prendre le cube
		chall_briefing_1001_nuits_take_cube = EscapeGameChallenge(room=room_briefing_1001_nuits, name='Salle de briefing des 1001 nuits - Prendre le cube')
		chall_briefing_1001_nuits_take_cube.save()
		gpio = chall_briefing_1001_nuits_take_cube.gpio
		gpio.cube = cube_1001_nuits
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Cube Challenge: SAS des 1001 nuits - Poser le cube
		chall_sas_1_put_cube = EscapeGameChallenge(room=room_sas_1, name='SAS des 1001 nuits - Poser le cube', dependent_on=chall_briefing_1001_nuits_take_cube)
		chall_sas_1_put_cube.save()
		gpio = chall_sas_1_put_cube.gpio
		gpio.cube = cube_1001_nuits
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		# Cube Challenge: SAS des 1001 nuits - Prendre le cube
		chall_sas_1_take_cube = EscapeGameChallenge(room=room_sas_1, name='SAS des 1001 nuits - Prendre le cube', dependent_on=chall_sas_1_put_cube)
		chall_sas_1_take_cube.save()
		gpio = chall_sas_1_take_cube.gpio
		gpio.cube = cube_1001_nuits
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Challenge: La fontaine
		chall_fontaine = EscapeGameChallenge(room=room_fontaine, name='La fontaine', dependent_on=chall_sas_1_take_cube)
		chall_fontaine.save()

		# Challenge: Les dalles
		chall_dalles = EscapeGameChallenge(room=room_fontaine, name='Les dalles', dependent_on=chall_fontaine)
		chall_dalles.save()

		# Challenge: Le marchand
		chall_marchand = EscapeGameChallenge(room=room_caverne, name='Le marchand', dependent_on=chall_dalles)
		chall_marchand.save()

		# Challenge: Le lanceur de couteaux
		chall_couteaux = EscapeGameChallenge(room=room_caverne, name='Le lanceur de couteaux', dependent_on=chall_marchand)
		chall_couteaux.save()

		# Challenge: Le charmeur de serpents
		chall_serpents = EscapeGameChallenge(room=room_caverne, name='Le charmeur de serpents', dependent_on=chall_couteaux)
		chall_serpents.save()

		# Challenge: Le fakir
		chall_fakir = EscapeGameChallenge(room=room_caverne, name='Le fakir', dependent_on=chall_serpents)
		chall_fakir.save()

		# Challenge La lampe
		chall_lampe = EscapeGameChallenge(room=room_lampe, name='La lampe', dependent_on=chall_fakir)
		chall_lampe.save()

		# Cube Challenge: Retour au SAS des 1001 nuits - Poser le cube
		chall_sas_1_put_cube_retour = EscapeGameChallenge(room=room_sas_1_retour, name='Retour au SAS des 1001 nuits - Poser le cube', dependent_on=chall_lampe)
		chall_sas_1_put_cube_retour.save()
		gpio = chall_sas_1_put_cube_retour.gpio
		gpio.cube = cube_1001_nuits
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		# Cube Challenge: Retour au SAS des 1001 nuits - Prendre le cube
		chall_sas_1_take_cube_retour = EscapeGameChallenge(room=room_sas_1_retour, name='Retour au SAS des 1001 nuits - Prendre le cube', dependent_on=chall_sas_1_put_cube_retour)
		chall_sas_1_take_cube_retour.save()
		gpio = chall_sas_1_take_cube_retour.gpio
		gpio.cube = cube_1001_nuits
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Cube Challenge: Retour dans la salle de briefing des 1001 nuits - Poser le cube
		chall_briefing_1001_nuits_put_cube = EscapeGameChallenge(room=room_briefing_1001_nuits_retour, name='Retour dans la salle de briefing des 1001 nuits - Poser le cube', dependent_on=chall_sas_1_take_cube_retour)
		chall_briefing_1001_nuits_put_cube.save()
		gpio = chall_briefing_1001_nuits_put_cube.gpio
		gpio.cube = cube_1001_nuits
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		#
		# Stranger Things
		#

		# Cube Challenge: Salle de briefing Stranger Things - Prendre le cube obscur
		chall_briefing_stranger_things_take_cube_obscur = EscapeGameChallenge(room=room_briefing_stranger_things_obscur, name='Salle de briefing Stranger Things - Prendre le cube obscur')
		chall_briefing_stranger_things_take_cube_obscur.save()
		gpio = chall_briefing_stranger_things_take_cube_obscur.gpio
		gpio.cube = cube_obscur
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Cube Challenge: Salle de briefing Stranger Things - Prendre le cube clair
		chall_briefing_stranger_things_take_cube_clair = EscapeGameChallenge(room=room_briefing_stranger_things_clair, name='Salle de briefing Stranger Things - Prendre le cube clair')
		chall_briefing_stranger_things_take_cube_clair.save()
		gpio = chall_briefing_stranger_things_take_cube_clair.gpio
		gpio.cube = cube_clair
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Cube Challenge: SAS obscur Stranger Things - Poser le cube obscur
		chall_sas_2_put_cube_obscur = EscapeGameChallenge(room=room_sas_2, name='SAS obscur Stranger Things - Poser le cube obscur', dependent_on=chall_briefing_stranger_things_take_cube_obscur)
		chall_sas_2_put_cube_obscur.save()
		gpio = chall_sas_2_put_cube_obscur.gpio
		gpio.cube = cube_obscur
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		# Cube Challenge: SAS obscur Stranger Things - Prendre le cube obscur
		chall_sas_2_take_cube_obscur = EscapeGameChallenge(room=room_sas_2, name='SAS obscur Stranger Things - Prendre le cube obscur', dependent_on=chall_sas_2_put_cube_obscur)
		chall_sas_2_take_cube_obscur.save()
		gpio = chall_sas_2_take_cube_obscur.gpio
		gpio.cube = cube_obscur
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Cube Challenge: SAS clair Stranger Things - Poser le cube clair
		chall_sas_3_put_cube_clair = EscapeGameChallenge(room=room_sas_3, name='SAS clair Stranger Things - Poser le cube clair', dependent_on=chall_briefing_stranger_things_take_cube_clair)
		chall_sas_3_put_cube_clair.save()
		gpio = chall_sas_3_put_cube_clair.gpio
		gpio.cube = cube_clair
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		# Cube Challenge: SAS clair Stranger Things - Prendre le cube clair
		chall_sas_3_take_cube_clair = EscapeGameChallenge(room=room_sas_3, name='SAS obscur Stranger Things - Prendre le cube clair', dependent_on=chall_sas_3_put_cube_clair)
		chall_sas_3_take_cube_clair.save()
		gpio = chall_sas_3_take_cube_clair.gpio
		gpio.cube = cube_clair
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Challenge: Stranger Things / La salle obscure / 1
		chall_salle_obscure_1 = EscapeGameChallenge(room=room_obscure, name='Salle obscure - chall1', dependent_on=chall_sas_2_take_cube_obscur)
		chall_salle_obscure_1.save()

		# Challenge: Stranger Things / La salle obscure / 2
		chall_salle_obscure_2 = EscapeGameChallenge(room=room_obscure, name='Salle obscure - chall2', dependent_on=chall_salle_obscure_1)
		chall_salle_obscure_2.save()

		# Challenge: Stranger Things / La salle claire / 1
		chall_salle_claire_1 = EscapeGameChallenge(room=room_claire, name='Salle claire - chall1', dependent_on=chall_sas_3_take_cube_clair)
		chall_salle_claire_1.save()

		# Challenge: Stranger Things / La salle claire / 2
		chall_salle_claire_2 = EscapeGameChallenge(room=room_claire, name='Salle claire - chall2', dependent_on=chall_salle_claire_1)
		chall_salle_claire_2.save()

		# Challenge: La radio (Stranger Things / La salle obscure)
		chall_radio = EscapeGameChallenge(room=room_obscure, name='La radio', solved_media=audio_demo, dependent_on=chall_salle_claire_2)
		chall_radio.save()

		# Challenge: Stranger Things / La forêt / 1
		chall_la_foret_1 = EscapeGameChallenge(room=room_foret, name='La forêt - chall1', solved_media=video_la_foret, dependent_on=chall_radio)
		chall_la_foret_1.save()

		# Challenge: Stranger Things / La forêt / 2
		chall_la_foret_2 = EscapeGameChallenge(room=room_foret, name='La forêt - chall2', dependent_on=chall_la_foret_1)
		chall_la_foret_2.save()

		# Cube Challenge: Retour au SAS obscur - Poser le cube obscur
		chall_sas_2_put_cube_obscur_retour = EscapeGameChallenge(room=room_sas_2_retour, name='Retour au SAS obscur - Poser le cube obscur', dependent_on=chall_la_foret_2)
		chall_sas_2_put_cube_obscur_retour.save()
		gpio = chall_sas_2_put_cube_obscur_retour.gpio
		gpio.cube = cube_obscur
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		# Cube Challenge: Retour au SAS obscur - Prendre le cube obscur
		chall_sas_2_take_cube_obscur_retour = EscapeGameChallenge(room=room_sas_2_retour, name='Retour au SAS obscur - Prendre le cube obscur', dependent_on=chall_sas_2_put_cube_obscur_retour)
		chall_sas_2_take_cube_obscur_retour.save()
		gpio = chall_sas_2_take_cube_obscur_retour.gpio
		gpio.cube = cube_obscur
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Cube Challenge: Retour au SAS clair - Poser le cube clair
		chall_sas_3_put_cube_clair_retour = EscapeGameChallenge(room=room_sas_3_retour, name='Retour au SAS clair - Poser le cube clair', dependent_on=chall_la_foret_2)
		chall_sas_3_put_cube_clair_retour.save()
		gpio = chall_sas_3_put_cube_clair_retour.gpio
		gpio.cube = cube_clair
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		# Cube Challenge: Retour au SAS clair - Prendre le cube clair
		chall_sas_3_take_cube_clair_retour = EscapeGameChallenge(room=room_sas_3_retour, name='Retour au SAS clair - Prendre le cube clair', dependent_on=chall_sas_3_put_cube_clair_retour)
		chall_sas_3_take_cube_clair_retour.save()
		gpio = chall_sas_3_take_cube_clair_retour.gpio
		gpio.cube = cube_clair
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Cube Challenge: Salle de briefing Stranger Things - Poser le cube obscur
		chall_briefing_stranger_things_put_cube_obscur = EscapeGameChallenge(room=room_briefing_stranger_things_retour, name='Retour dans la salle de briefing Stranger Things - Poser le cube obscur', dependent_on=chall_sas_2_take_cube_obscur_retour)
		chall_briefing_stranger_things_put_cube_obscur.save()
		gpio = chall_briefing_stranger_things_put_cube_obscur.gpio
		gpio.cube = cube_obscur
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		# Cube Challenge: Salle de briefing Stranger Things - Poser le cube clair
		chall_briefing_stranger_things_put_cube_clair = EscapeGameChallenge(room=room_briefing_stranger_things_retour, name='Retour dans la salle de briefing Stranger Things - Poser le cube clair', dependent_on=chall_sas_3_take_cube_clair_retour)
		chall_briefing_stranger_things_put_cube_clair.save()
		gpio = chall_briefing_stranger_things_put_cube_clair.gpio
		gpio.cube = cube_clair
		gpio.challenge_type = ChallengeGPIO.TYPE_PUT_CUBE
		gpio.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Lifts
#
		self.stdout.write('  Populating model `LiftGPIO`', ending='')

		# Lift: cube les 1001 nuits
		lift_1001_nuits = LiftGPIO(name='Les 1001 nuits', controller=raspi_master, cube=cube_1001_nuits, pin=31)
		lift_1001_nuits.save()

		# Lift: Stranger Things - Salle obscure
		lift_stranger_things_salle_obscure = LiftGPIO(name='Stranger Things - Salle obscure', controller=raspi_master, cube=cube_obscur, pin=32)
		lift_stranger_things_salle_obscure.save()

		# Lift: Stranger Things - Salle claire
		lift_stranger_things_salle_claire = LiftGPIO(name='Stranger Things - Salle claire', controller=raspi_master, cube=cube_clair, pin=33)
		lift_stranger_things_salle_claire.save()

		self.stdout.write(self.style.SUCCESS(' OK'))
