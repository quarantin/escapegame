#!/bin/bash

# Clear database
rm -f db.sqlite3

# Create database
python3 manage.py makemigrations
python3 manage.py migrate

# Add video player "mplayer"
python3 manage.py shell -c "from video.models import VideoPlayer; VideoPlayer(video_player='mplayer').save()"

# Add video player "omxplayer"
python3 manage.py shell -c "from video.models import VideoPlayer; VideoPlayer(video_player='omxplayer').save()"

# Add escape game "Mille et une nuits"
python3 manage.py shell -c "from escapegame.models import EscapeGame; EscapeGame(name='Mille et une nuits', video='test.h264').save()"

# Add escape game "Stranger Things"
python3 manage.py shell -c "from escapegame.models import EscapeGame; EscapeGame(name='Mille et une nuits', video='test.h264').save()"

python3 manage.py createsuperuser --user gamemaster --email none@mail.com
