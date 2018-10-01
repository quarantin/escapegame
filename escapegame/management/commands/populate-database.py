# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from escapegame.models import *
from multimedia.models import *
from controllers.models import *

from datetime import timedelta


class Command(BaseCommand):

	def flush_database(self):

		all_models = [
			Audio,
			Image,
			Video,
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
# Audio
#
		self.stdout.write('  Populating model `Audio`', ending='')
		demo_audio = Audio(name='Audio Demo', audio_path='uploads/audios/test.h264')
		demo_audio.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Images
#

		self.stdout.write('  Populating model `Image`', ending='')

		# Full map image
		map_image = Image(image_name='Escape Game Map - Full Map', image_path='uploads/images/map-base.png')
		map_image.save()

		# Door briefing room image
		door_briefing_room_image = Image(image_name='Door briefing room', image_path='uploads/images/door-briefing-room.png')
		door_briefing_room_image.save()

		# Door corridor SAS 1
		door_corridor_sas_1_image = Image(image_name='Door corridor SAS 1', image_path='uploads/images/door-corridor-sas-1.png')
		door_corridor_sas_1_image.save()

		# Door corridor SAS 2
		door_corridor_sas_2_image = Image(image_name='Door corridor SAS 2', image_path='uploads/images/door-corridor-sas-2.png')
		door_corridor_sas_2_image.save()

		# Door corridor SAS 3
		door_corridor_sas_3_image = Image(image_name='Door corridor SAS 3', image_path='uploads/images/door-corridor-sas-3.png')
		door_corridor_sas_3_image.save()

		# SAS 1 door image
		door_sas_1_image = Image(image_name='Les 1001 nuits - SAS Door', image_path='uploads/images/door-sas-1.png')
		door_sas_1_image.save()

		# SAS 2 door image
		door_sas_2_image = Image(image_name='Stranger Things - SAS Door - Salle Claire', image_path='uploads/images/door-sas-2.png')
		door_sas_2_image.save()

		# SAS 3 door image
		door_sas_3_image = Image(image_name='Stranger Things - SAS Door - Salle Obscure', image_path='uploads/images/door-sas-3.png')
		door_sas_3_image.save()

		# Room "La Fontaine" door image
		door_fontain_room_image = Image(image_name='Les 1001 nuits - La Fontaine Door', image_path='uploads/images/door-fontain-room.png')
		door_fontain_room_image.save()

		# Room "Salle obscure" door image
		door_salle_obscure_image = Image(image_name='Stranger Things - Salle Obscure Door', image_path='uploads/images/door-salle-obscure.png')
		door_salle_obscure_image.save()

		# Room "Salle claire" door image
		door_salle_claire_image = Image(image_name='Stranger Things - Salle Claire Door', image_path='uploads/images/door-salle-claire.png')
		door_salle_claire_image.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Videos
#
		self.stdout.write('  Populating model `Video`', ending='')

		# Demo Video
		demo_video = Video(name='Video Demo', path='uploads/videos/test.h264')
		demo_video.save()

		# Demo Video 2
		demo_video_2 = Video(name='Video Demo 2', path='uploads/videos/small.mp4')
		demo_video_2.save()

		# Les 1001 nuits - Briefing Video
		briefing_video_1001_nuits = Video(name='Les 1001 nuits - Briefing', path='uploads/videos/test.h264')
		briefing_video_1001_nuits.save()

		# Les 1001 nuits - Winners Video
		winners_video_1001_nuits = Video(name='Les 1001 nuits - Good End', path='uploads/videos/test.h264')
		winners_video_1001_nuits.save()

		# Les 1001 nuits - Losers Video
		losers_video_1001_nuits = Video(name='Les 1001 nuits - Bad End', path='uploads/videos/test.h264')
		losers_video_1001_nuits.save()

		# Stranger Things - Salle obscure - Briefing Video
		briefing_video_stranger_things_salle_obscure = Video(name='Stranger Things - Salle obscure - Briefing', path='uploads/videos/test.h264')
		briefing_video_stranger_things_salle_obscure.save()

		# Stranger Things - Salle claire - Briefing Video
		briefing_video_stranger_things_salle_claire = Video(name='Stranger Things - Salle claire - Briefing', path='uploads/videos/test.h264')
		briefing_video_stranger_things_salle_claire.save()

		# Stranger Things - Winners Video
		winners_video_stranger_things = Video(name='Stranger Things - Good End', path='uploads/videos/test.h264')
		winners_video_stranger_things.save()

		# Stranger Things - Losers Video
		losers_video_stranger_things = Video(name='Stranger Things - Bad End', path='uploads/videos/test.h264')
		losers_video_stranger_things.save()

		# Stranger Things - Challenge Video - La Forêt
		video_la_foret = Video(name='Stranger Things - Challenge - La Forêt', path='uploads/videos/test.h264')
		video_la_foret.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Raspberry Pis
#
		self.stdout.write('  Populating model `RaspberryPi`', ending='')

		# Raspberry Pi: Master game controller
		raspi_master = RaspberryPi(name='Game Master', hostname='escapegame.local')
		raspi_master.save()

		# Raspberry Pi: Les 1001 nuits
		raspi_1001_nuits = RaspberryPi(name='Les 1001 nuits', hostname='les-1001-nuits.local')
		raspi_1001_nuits.save()

		# Raspberry Pi: Sons Les 1001 nuits
		raspi_sons_1001_nuits = RaspberryPi(name='Sons Les 1001 nuits', hostname='sons-les-1001-nuits.local', media_type= "audio")
		raspi_sons_1001_nuits.save()

		# Raspberry Pi: Stranger Things
		raspi_stranger_things = RaspberryPi(name='Stranger Things', hostname='stranger-things.local')
		raspi_stranger_things.save()

		# Raspberry Pi: Son Stranger Things
		raspi_son_stranger_things = RaspberryPi(name='Sons Stranger Things', hostname='sons-stranger-things.local', media_type= "audio")
		raspi_son_stranger_things.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Escape games
#
		self.stdout.write('  Populating model `EscapeGame`', ending='')

		# Escape game: Les 1001 nuits
		time_limit_1001_nuits = timedelta(minutes=30)
		game_1001_nuits = EscapeGame(
			name='Les 1001 nuits',
			time_limit=time_limit_1001_nuits,
			winners_video=winners_video_1001_nuits,
			losers_video=losers_video_1001_nuits,
			controller=raspi_1001_nuits,
			map_image=map_image)

		game_1001_nuits.save()

		# Escape game: Stranger Things
		time_limit_stranger_things = timedelta(hours=1)
		game_stranger_things = EscapeGame(
			name='Stranger Things',
			time_limit=time_limit_stranger_things,
			winners_video=winners_video_stranger_things,
			losers_video=losers_video_stranger_things,
			controller=raspi_stranger_things,
			map_image=map_image)

		game_stranger_things.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Cubes
#
		cube_1001_nuits = EscapeGameCube(tag_id='FF000001', game=game_1001_nuits)
		cube_1001_nuits.save()

		cube_obscur = EscapeGameCube(tag_id='FF000002', game=game_stranger_things)
		cube_obscur.save()

		cube_clair = EscapeGameCube(tag_id='FF000003', game=game_stranger_things)
		cube_clair.save()
#
# Rooms
#
		self.stdout.write('  Populating model `EscapeGameRoom`', ending='')

		#
		# Les 1001 nuits
		#

		# Room: La salle de briefing des 1001 nuits
		room_briefing_1001_nuits = EscapeGameRoom(game=game_1001_nuits, controller=raspi_master, door_image=door_briefing_room_image, name='Salle de briefing des 1001 nuits')
		room_briefing_1001_nuits.save()

		# Room: Le SAS des 1001 nuits (SAS 1)
		room_sas_1 = EscapeGameRoom(game=game_1001_nuits, door_image=door_sas_1_image, name='Le SAS des 1001 nuits', is_sas=True)
		room_sas_1.save()

		# Room: La fontaine
		room_fontaine = EscapeGameRoom(game=game_1001_nuits, door_image=door_fontain_room_image, name='La fontaine')
		room_fontaine.save()

		# Room: La caverne
		room_caverne = EscapeGameRoom(game=game_1001_nuits, door_image=None, name='La caverne')
		room_caverne.save()

		# Room: La lampe
		room_lampe = EscapeGameRoom(game=game_1001_nuits, door_image=None, name='La lampe')
		room_lampe.save()

		# Room: Retour au SAS des 1001 nuits (SAS 1)
		room_sas_1_retour = EscapeGameRoom(game=game_1001_nuits, door_image=door_sas_1_image, name='Retour au SAS des 1001 nuits')
		room_sas_1_retour.save()

		# Room: Retour dans la salle de briefing des 1001 nuits
		room_briefing_1001_nuits_retour = EscapeGameRoom(game=game_1001_nuits, controller=raspi_master, door_image=door_briefing_room_image, name='Retour dans la salle de briefing des 1001 nuits')
		room_briefing_1001_nuits_retour.save()

		#
		# Stranger Things
		#

		# Room: La salle de briefing de Stranger Things
		room_briefing_stranger_things = EscapeGameRoom(game=game_stranger_things, controller=raspi_master, door_image=door_briefing_room_image, name='La salle de briefing de Stranger Things')
		room_briefing_stranger_things.save()

		# Room: Le SAS obscur de Stranger Things (SAS 2)
		room_sas_2 = EscapeGameRoom(game=game_stranger_things, door_image=door_sas_2_image, name='Le SAS obscur', is_sas=True)
		room_sas_2.save()

		# Room: Le SAS clair de Stranger Things (SAS 3)
		room_sas_3 = EscapeGameRoom(game=game_stranger_things, door_image=door_sas_3_image, name='Le SAS clair', is_sas=True)
		room_sas_3.save()

		# Room: La salle claire
		room_claire = EscapeGameRoom(game=game_stranger_things, door_image=door_salle_claire_image, name='La salle claire')
		room_claire.save()

		# Room: La salle obscure
		room_obscure = EscapeGameRoom(game=game_stranger_things, door_image=door_salle_obscure_image, name='La salle obscure')
		room_obscure.save()

		# Room: La forêt
		room_foret = EscapeGameRoom(game=game_stranger_things, name='La forêt')
		room_foret.save()

		# Room: Retour au SAS obscur (SAS 2)
		room_sas_2_retour = EscapeGameRoom(game=game_stranger_things, door_image=door_sas_2_image, name='Retour au SAS obscur')
		room_sas_2_retour.save()

		# Room: Rettour au SAS clair (SAS 3)
		room_sas_3_retour = EscapeGameRoom(game=game_stranger_things, door_image=door_sas_3_image, name='Retour au SAS clair')
		room_sas_3_retour.save()

		# Room: Salle de briefing - Stranger Things (Retour)
		room_briefing_stranger_things_retour = EscapeGameRoom(game=game_stranger_things, controller=raspi_master, door_image=door_briefing_room_image, name='Retour dans la salle de briefing de Stranger Things')
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
		chall_briefing_stranger_things_take_cube_obscur = EscapeGameChallenge(room=room_briefing_stranger_things, name='Salle de briefing Stranger Things - Prendre le cube obscur')
		chall_briefing_stranger_things_take_cube_obscur.save()
		gpio = chall_briefing_stranger_things_take_cube_obscur.gpio
		gpio.cube = cube_obscur
		gpio.challenge_type = ChallengeGPIO.TYPE_TAKE_CUBE
		gpio.save()

		# Cube Challenge: Salle de briefing Stranger Things - Prendre le cube clair
		chall_briefing_stranger_things_take_cube_clair = EscapeGameChallenge(room=room_briefing_stranger_things, name='Salle de briefing Stranger Things - Prendre le cube clair')
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
		chall_radio = EscapeGameChallenge(room=room_obscure, name='La radio', dependent_on=chall_salle_claire_2)
		chall_radio.save()

		# Challenge: Stranger Things / La forêt / 1
		chall_la_foret_1 = EscapeGameChallenge(room=room_foret, name='La forêt - chall1', solved_video=video_la_foret, dependent_on=chall_radio)
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
# Extra doors
#
		self.stdout.write('  Populating model `DoorGPIO` (extra)', ending='')

		# SAS 1 is for Les 1001 nuits
		door_corridor_sas_1 = DoorGPIO(name='La porte couloir du SAS 1001 Nuits', dependent_on=chall_briefing_1001_nuits_take_cube, controller=raspi_master, image=door_corridor_sas_1_image, action_pin=11)
		door_corridor_sas_1.save()

		# SAS 2 is for Stranger Things - Salle Claire
		door_corridor_sas_2 = DoorGPIO(name='La porte couloir du SAS obscur', dependent_on=chall_briefing_stranger_things_take_cube_obscur, controller=raspi_master, image=door_corridor_sas_2_image, action_pin=11)
		door_corridor_sas_2.save()

		# SAS 3 is for Stranger Things - Salle Obscure
		door_corridor_sas_3 = DoorGPIO(name='La porte couloir du SAS clair', dependent_on=chall_briefing_stranger_things_take_cube_clair, controller=raspi_master, image=door_corridor_sas_3_image, action_pin=11)
		door_corridor_sas_3.save()

		self.stdout.write(self.style.SUCCESS(' OK'))

#
# Lifts
#
		self.stdout.write('  Populating model `LiftGPIO`', ending='')

		# Lift: cube les 1001 nuits
		lift_1001_nuits = LiftGPIO(name='Les 1001 nuits', controller=raspi_master, game=game_1001_nuits, briefing_video=briefing_video_1001_nuits, pin=31)
		lift_1001_nuits.save()

		# Lift: Stranger Things - Salle obscure
		lift_stranger_things_salle_obscure = LiftGPIO(name='Stranger Things - Salle obscure', controller=raspi_master, game=game_stranger_things, briefing_video=briefing_video_stranger_things_salle_obscure, pin=32)
		lift_stranger_things_salle_obscure.save()

		# Lift: Stranger Things - Salle claire
		lift_stranger_things_salle_claire = LiftGPIO(name='Stranger Things - Salle claire', controller=raspi_master, game=game_stranger_things, briefing_video=briefing_video_stranger_things_salle_claire, pin=33)
		lift_stranger_things_salle_claire.save()

		self.stdout.write(self.style.SUCCESS(' OK'))
