$(document).ready(function() {

	/*
	 * Escape game controls:
	 *   - start
	 *   - reset
	 */

	// Handler for the button to start the escape game
	$('button#start-escapegame').click(function() {

		ok = confirm('Are you really sure you want to start a new escape game?\nThis will reset all challenge state and current score.');
		if (ok !== true)
			return;

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: '/web/' + this.value + '/start/',
			crossDomain: true,
		});
	});

	// Handler for the button to reset the escape game
	$('button#reset-escapegame').click(function() {

		ok = confirm('Are you really sure you want to reset the current escape game?\nThis will reset all challenge state and current score.');
		if (ok !== true)
			return;

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: '/web/' + this.value + '/reset/',
			crossDomain: true,
		});
	});

	/*
	 * Video controls:
	 *   - play
	 *   - pause
	 *   - stop
	 */

	// Handler for the button to start the video
	$('button#video-play').click(function() {

		$('button#video-play').toggleClass('d-none');
		$('button#video-pause').toggleClass('d-none');

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: '/api/video/' + this.value + '/play/',
			crossDomain: true,
		});
	});

	// Handler for the button to pause the video
	$('button#video-pause').click(function() {

		$('button#video-play').toggleClass('d-none');
		$('button#video-pause').toggleClass('d-none');

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: '/api/video/' + this.value + '/pause/',
			crossDomain: true,
		});
	});

	// Handler for the button to stop the video
	$('button#video-stop').click(function() {

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: '/api/video/' + this.value + '/stop/',
			crossDomain: true,
		});
	});

	// Handler for lock buttons
	$('button.lock-button').click(function() {

		ok = confirm('Are you really sure you want to unlock the door?');
		if (ok !== true)
			return;

		$('button#'   + this.id).toggleClass('d-none');
		$('button#un' + this.id).toggleClass('d-none');

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: this.value,
			crossDomain: true,
		});
	});

	// Handler for unlock buttons
	$('button.unlock-button').click(function() {

		ok = confirm('Are you really sure you want to lock the door?');
		if (ok !== true)
			return;

		$('button#' + this.id             ).toggleClass('d-none');
		$('button#' + this.id.substring(2)).toggleClass('d-none');

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: this.value,
			crossDomain: true,
		});
	});

	function drawImage(ctx, imageObj) {
		console.log(imageObj);
		image = new Image();
		image.src = '/media/' + imageObj.image_path;
		ctx.drawImage(image, 0, 0, imageObj.width, imageObj.height);
	}

	function draw_map(game) {

		var canvas = $('canvas#map')[0];
		var ctx = canvas.getContext('2d');

		var map_image = new Image();

		map_image.src = '/media/' + game.map_image.image_path;
		map_image.onload = function () {

			if (game.map_image) {
				ctx.drawImage(map_image, 0, 0, game.map_image.width, game.map_image.height);
			}

			if (game.sas_door_image && game.sas_door_locked === false) {
				drawImage(ctx, game.sas_door_image);
			}

			if (game.corridor_door_image && game.corridor_door_locked === false) {
				drawImage(ctx, game.corridor_door_image);
			}

			for (var index in game.rooms) {
				var room = game.rooms[index];
				if (room.door_image && room.door_locked == false) {
					drawImage(ctx, room.door_image);
				}
			}
		};
	};

	function refresh_page() {

		var game_slug = $('button#start-escapegame').val();

		$.ajax({
			url: '/web/' + game_slug + '/status/',
			crossDomain: true,
			success: function(game) {

				if (typeof game === 'undefined')
					return;

				// For each room...
				for (var index in game.rooms) {

					var room = game.rooms[index];

					var html = '\t<tr>\n\t\t<th>Enigmes</th>\n\t\t<th>Statut</th></tr>\n';
					var statusdiv = $('div#' + room.slug + '-data');

					if (room.challenges.length == 0) {
						html = '<div class="col"><span><p>No challenge configured for this room.<br>You can visit <a href="/admin/escapegame/escapegamechallenge">this</a> page to create new challenges.</p></span></div>';
					}
					else {
						// For each challenge...
						for (var subindex in room.challenges) {
							var chall = room.challenges[subindex];
							var solved = '<img src="/static/admin/img/' + (chall.solved ? 'icon-yes.svg' : 'icon-no.svg') + '"/>';
							html += '\t<tr>\n\t\t<td width="80%">' + chall.challenge_name + '</td>\n\t\t<td width="20%">' + solved + '</td>\n\t</tr>\n';
						}

						html = '<table class="challenge-status">\n' + html + '</table>\n';
					}

					statusdiv.html(html);
				}

				draw_map(game);
			},
		});
	}

	refresh_page();

	var ws = new WebSocket('ws://' + location.hostname + '/ws/notify?subscribe-broadcast')

	ws.onopen = function() {
		console.log('websocket connected');
	};

	ws.onmessage = function(e) {
		console.log('websocket received data: ' + e.data);
		refresh_page();
	};

	ws.onerror = function(e) {
		console.error(e);
	};

	ws.onclose = function(e) {
		console.log('websocket closed');
	};
});
