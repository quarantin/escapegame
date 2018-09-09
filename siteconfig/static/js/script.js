$(document).ready(function() {

	/*
	 * Retrieve language country code from URL.
	 */
	function get_language() {
		return location.pathname.split('/')[1];
	}

	/*
	 * Return the video URL for the video selected in select field.
	 */
	function get_video_url(action) {

		selected_video = $('#selected-video').val();
		selected_raspi = $('#selected-raspberry-pi').val();

		return selected_raspi + '/' + get_language() + '/api/video/' + selected_video + '/' + action + '/';
	}


	/*
	 * Escape game reset button
	 */

	// Handler for the button to reset the escape game
	$('button#reset-escapegame').click(function() {

		ok = confirm('Are you really sure you want to reset the current escape game?\n\nThis will reset all challenge state and current score.');
		if (ok !== true)
			return;

		$.ajax({
			url: '/' + get_language() + '/' + this.value + '/reset/',
			success: function() {
				location.reload();
			},
		});
	});


	/*
	 * Video control buttons:
	 *   - play
	 *   - pause
	 *   - stop
	 */

	// Handler for the button to start the video
	$('#selected-video').on('change', function(){
		$('#selected-video').val(this.value);
	});

	$('button#video-play').click(function() {
		$('button#video-play').toggleClass('d-none');
		$('button#video-pause').toggleClass('d-none');

		$.ajax({
			url: get_video_url('pause'),
		});
	});

	// Handler for the button to pause the video
	$('button#video-pause').click(function() {

		$('button#video-play').toggleClass('d-none');
		$('button#video-pause').toggleClass('d-none');

		$.ajax({
			url: get_video_url('pause'),
		});
	});

	// Handler for the button to stop the video
	$('button#video-stop').click(function() {

		$.ajax({
			url: get_video_url('stop'),
		});
	});

	/*
	 * Door control buttons
	 */

	// Handler for lock buttons
	$('button.lock-button').click(function() {

		ok = confirm('Are you really sure you want to unlock the door?');
		if (ok !== true)
			return;

		$.ajax({
			url: this.value,
			success: function() {
				location.reload();
			},
		});
	});

	// Handler for unlock buttons
	$('button.unlock-button').click(function() {

		ok = confirm('Are you really sure you want to lock the door?');
		if (ok !== true)
			return;

		$.ajax({
			url: this.value,
			success: function() {
				location.reload();
			},
		});
	});

	/*
	 * Challenge control buttons
	 */

	// Handler for challenge reset buttons
	$('a.challenge-reset').click(function (e) {

		ok = confirm('Are you really sure you want to reset this challenge?');
		if (ok !== true)
			return;

		// Don't follow href
		e.preventDefault();

		$.ajax({
			url: this.href,
			success: function() {
				location.reload();
			},
		});
	});

	// Handler for challenge validate buttons
	$('a.challenge-validate').click(function (e) {

		ok = confirm('Are you really sure you want to validate this challenge?');
		if (ok !== true)
			return;

		// Don't follow href
		e.preventDefault();

		$.ajax({
			url: this.href,
			success: function() {
				location.reload();
			},
		});
	});

	function drawImage(ctx, imageObj) {
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

			for (var index in game.rooms) {
				var room = game.rooms[index];
				if (room.door_image && room.door.locked == false) {
					drawImage(ctx, room.door_image);
				}
			}
		};
	};

	function refresh_page() {

		var game_slug = $('button#reset-escapegame').val();

		$.ajax({
			url: '/' + get_language() + '/' + game_slug + '/status/',
			success: function(game) {

				if (typeof game === 'undefined')
					return;

				draw_map(game);
			},
		});
	}

	function create_websocket() {

		var port;
		var protocol;

		if (location.protocol == 'http:') {
			port = (location.port == 80 ? '' : ':' + location.port);
			protocol = 'ws:';
		}
		else if (location.protocol == 'https:') {
			port = (location.port == 443 ? '' : ':' + location.port);
			protocol = 'wss:';
		}
		else {
			console.log('Unsupported protocol: ' + location.protocol);
			return;
		}

		var game_slug = $('button#reset-escapegame').val();

		var ws = new WebSocket(protocol + '//' + location.hostname + port + '/ws/notify-' + game_slug + '?subscribe-broadcast');

		ws.onopen = function() {
			console.log('websocket connected');
		};

		ws.onmessage = function(e) {
			console.log('websocket received data: ' + e.data);
			if (e.data.startsWith('notify')) {
				refresh_page();
			}
			else
				$('div#counter').text(e.data);
		};

		ws.onerror = function(e) {
			console.error(e);
		};

		ws.onclose = function(e) {
			console.log('websocket closed');
		};
	}

	refresh_page();

	create_websocket();
});
