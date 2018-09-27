/*
 * One second is 1000 miliseconds.
 */
var second = 1000;

/*
 * Timeout for AJAX requests (3 seconds).
 */
var timeout = 3 * second;

/*
 * Retrieve language country code from URL.
 */
function get_language()
{
	return location.pathname.split('/')[1];
}

/*
 * Retrieve the URL of the Raspberry Pi selected in the radio button list.
 */
function get_selected_video_raspi()
{
	raspi = $('input[name=selected-raspberry-pi-video]:checked');

	return (raspi.length > 0 ? raspi : false);
}


function get_selected_audio_raspi()
{
	raspi = $('input[name=selected-raspberry-pi-audio]:checked');

	return (raspi.length > 0 ? raspi : false);
}
/*
 * Return the video URL for the video selected in select field.
 */
function get_video_url(action)
{
	selected_video = $('#selected-video').val();
	selected_raspi = get_selected_video_raspi();

	raspi_url = '';
	if (selected_raspi)
		raspi_url = selected_raspi.data('raspi-url');

	return raspi_url + '/' + get_language() + '/api/video/' + selected_video + '/' + action + '/';
}


/*
 *Return the audio URL for the audio selected in select field.
 */

function get_audio_url(action)
{
	selected_audio = $('#selected-audio').val();
	selected_raspi = get_selected_audio_raspi();

	raspi_url = '';
	if (selected_raspi)
		raspi_url = selected_raspi.data('raspi-url');
	return raspi_url + '/' + get_language() + '/api/audio/' + selected_audio + '/' + action + '/';

}

/*
 * Switch visibility of buttons according to state.
 */
function toggle_elements(lock_button, unlock_button, locked)
{
	if (locked) {
		$(lock_button).addClass('d-none');
		$(unlock_button).removeClass('d-none');
	}
	else {
		$(lock_button).removeClass('d-none');
		$(unlock_button).addClass('d-none');
	}
}

/*
 * Toggle online status for the supplied Raspberry Pi
 */
function toggle_online_status(raspi)
{
	console.log('toggle_online_status');

	var span = $('#raspberry-pi-' + raspi.slug);
	var input = span.parent().find('input');

	span.removeClass('badge-' + raspi.not_badge);
	span.addClass('badge-' + raspi.badge);
	span.text(raspi.status);
	input.prop('disabled', !raspi.online);

	if (!raspi.online)
		input.prop('checked', false);

	selected_raspi_video = get_selected_video_raspi();
	selected_raspi_audio = get_selected_audio_raspi();

	if (!selected_raspi_video)
		$('input[name=selected-raspberry-pi-video]:enabled:first').prop('checked', true);


	if (!selected_raspi_audio)
		$('input[name=selected-raspberry-pi-audio]:enabled:first').prop('checked', true);
}

/**
 * Toggle lifts according to their state
 */
function toggle_lifts(game)
{
	for (var lift_index in game.lifts) {

		var lift = game.lifts[lift_index];
		var lift_id = game.slug + '-' + lift.slug;
		if (lift.raised) {
			$('button#raise-' + lift_id).addClass('button-disabled');
			$('button#lower-' + lift_id).removeClass('button-disabled');
		}
		else {
			$('button#raise-' + lift_id).removeClass('button-disabled');
			$('button#lower-' + lift_id).addClass('button-disabled');
		}
	}
}

/*
 * Toggle all elements in the page:
 *   - raspberry pis online status
 *   - door lock/unlock buttons
 *   - challenge validate/reset buttons
 */
function toggle_all_elements(game)
{
	toggle_lifts(game);

	for (var raspi_index in game.raspberrypis) {

		var raspi = game.raspberrypis[raspi_index];

		toggle_online_status(raspi);
	}

	for (var door_index in game.doors) {

		var door = game.doors[door_index];
		var door_name = game.slug + '-extra-' + door.slug;
		toggle_elements('button#lock-' + door_name, 'button#unlock-' + door_name, door.locked);
	}

	for (var room_index in game.rooms) {

		var room = game.rooms[room_index];
		var door = room.door;
		var door_name = game.slug + '-' + room.slug + '-' + door.slug;
		toggle_elements('button#lock-' + door_name , 'button#unlock-' + door_name, door.locked);

		for (var chall_index in room.challenges) {

			var chall = room.challenges[chall_index];
			var chall_name = game.slug + '-' + chall.slug;
			toggle_elements('a#validate-' + chall_name, 'a#reset-' + chall_name, chall.solved);
		}
	}
}

/*
 * Draw the given image onto the supplied context.
 */
function draw_image(ctx, imageObj)
{
	image = new Image();
	image.src = '/media/' + imageObj.image_path;
	console.log("Drawing image: " + image.src);
	ctx.drawImage(image, 0, 0, imageObj.width, imageObj.height);
}

/*
 * Draw the map of the game and its elements (doors, challenges, etc).
 */
function draw_map(game)
{
	var index;
	var canvas = $('canvas#map')[0];
	var ctx = canvas.getContext('2d');

	// Reset canvas
	ctx.clearRect(0, 0, canvas.width, canvas.height);

	if (game.map_image)
		draw_image(ctx, game.map_image);

	for (index in game.rooms) {

		var room = game.rooms[index];
		if (room.door_image && !room.door.locked)
			draw_image(ctx, room.door_image);
	}

	for (index in game.doors) {

		var door = game.doors[index];
		if (door.image && !door.locked)
			draw_image(ctx, door.image);
	}
};

/*
 * Refresh the page:
 *   - toggle door lock/unlock buttons
 *   - toggle challenge validate/reset buttons
 *   - draw the map with all current information available about the game.
 */
function refresh_page()
{
	console.log('refreshing page');

	var game_slug = $('button#reset-escapegame').val();

	$.ajax({
		url: '/' + get_language() + '/' + game_slug + '/status/',
		timeout: timeout,
		success: function(game) {

			if (typeof game === 'undefined') {
				alert('Invalid escape game status!');
				return;
			}

			toggle_all_elements(game);
			draw_map(game);
		},
		error: function() {
			alert('Could not retrieve escape game status!');
		},
	});
}

/*
 * Create the websocket to receive events from the server.
 */
function create_websocket()
{
	var port;
	var protocol;

	console.log('creating websocket');

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

	var heartbeat_msg = '--heartbeat--', heartbeat_interval = null, missed_heartbeats = 0;

	var ws = new WebSocket(protocol + '//' + location.hostname + port + '/ws/notify-' + game_slug + '?subscribe-broadcast');

	ws.onopen = function() {
		console.log('websocket connected');

		if (heartbeat_interval === null) {
			missed_heartbeats = 0;
			heartbeat_interval = setInterval(function() {
				try {
					missed_heartbeats++;
					if (missed_heartbeats >= 3)
						throw new Error("Too many missed heartbeats.");
					ws.send(heartbeat_msg);
				}
				catch(e) {
					clearInterval(heartbeat_interval);
					heartbeat_interval = null;
					console.warn("Closing connection. Reason: " + e.message);
					ws.close();
				}
			}, 5000);
		}
	};

	ws.onmessage = function(e) {

		// Heartbeat messages
		if (e.data === heartbeat_msg) {
			missed_heartbeats = 0;
			return;
		}

		console.log('websocket received data: ' + e.data);

		// Notify messages, meaning we have to refresh the page
		if (e.data.startsWith('notify')) {
			refresh_page();
			return;
		}

		// Timer messages, meaning we have to update the game counter
		$('div#counter').text(e.data);
	};

	ws.onerror = function(e) {
		console.log('websocket error');
		console.error(e);
	};

	ws.onclose = function(e) {
		console.log('websocket closed');
	};
}

/*
 * Assign click event handler for the escape game reset button.
 */
function game_control_handler(action)
{
	$('button#' + action + '-escapegame').click(function() {

		ok = confirm('Are you really sure you want to reset the current escape game?\n\nThis will reset all challenge state and current score.');
		if (ok !== true)
			return;

		$.ajax({
			url: '/' + get_language() + '/' + this.value + '/' + action + '/',
			success: function() {
				refresh_page();
				alert('Game reset was successful!');
			},
			error: function() {
				alert('Failed to reset the game.');
			},
		});
	});
}

/*
 * Assign click event handler for video control buttons.
 */
function video_control_handler(action)
{
	$('button#video-' + action).click(function() {

		if (action == 'play') {

			$('button#video-play').addClass('d-none');
			$('button#video-pause').removeClass('d-none');
		}
		else {

			$('button#video-play').removeClass('d-none');
			$('button#video-pause').addClass('d-none');
		}

		var video_url = get_video_url(action);

		$.ajax({
			url: video_url,
			timeout: timeout,
			success: function() {
				//refresh_page();
			},
			error: function() {
				alert('Could not connect to URL: ' + video_url);
			},
		});
	});
}

function audio_control_handler(action)
{
	$('button#audio-' + action).click(function(){
		if (action == 'play') {
			$('button#audio-play').addClass('d-none');
			$('button#audio-pause').removeClass('d-none');
		}
		else{
			$('button#audio-play').removeClass('d-none');
			$('button#audio-pause').addClass('d-none');
		}

		var audio_url = get_audio_url(action);

		$.ajax({
			url: audio_url,
			timeout: timeout,
			success: function() {
				//refresh_page();
			},
			error: function() {
				alert('Could not connect to URL: ' + audio_url);
			},
		});
	});
}

/*
 * Assign click event handler for lift control buttons.
 */
function lift_control_handler(action)
{
	$('button.' + action + '-lift').click(function() {

		var disabled = $(this).hasClass('button-disabled')
		if (disabled)
			return;

		ok = confirm('Are you really sure you want to ' + action + ' the lift?');
		if (ok !== true)
			return;

		$.ajax({
			url: this.value,
			success: function() {
				refresh_page();
			},
			error: function() {
				alert('Failed to ' + action + ' the lift.');
			},
		});
	});
}

/*
 * Assign click event handler for door control buttons.
 */
function door_control_handler(action)
{
	$('button.' + action + '-button').click(function() {

		ok = confirm('Are you really sure you want to ' + action + ' the door?');
		if (ok !== true)
			return;

		$.ajax({
			url: this.value,
			success: function() {
				refresh_page();
			},
			error: function() {
				alert('Failed to ' + action + ' the door.');
			},
		});
	});
}

/*
 * Assign click event handler for challenge control buttons.
 */
function challenge_control_handler(action)
{
	$('a.challenge-' + action).click(function (e) {

		ok = confirm('Are you really sure you want to ' + action + ' this challenge?');
		if (ok !== true)
			return;

		// Don't follow href
		e.preventDefault();

		$.ajax({
			url: this.href,
			success: function() {
				refresh_page();
			},
			error: function() {
				alert('Failed to ' + action + ' this challenge.');
			},
		});
	});
}

$(document).ready(function() {

	// Handler for the button to reset the escape game
	game_control_handler('reset');

	// Handler for the button to start the video
	video_control_handler('play');

	// Handler for the button to pause the video
	video_control_handler('pause');

	// Handler for the button to stop the video
	video_control_handler('stop');

	// Handler for the button to start the audio
	audio_control_handler('play');

	// Handler for the button to pause the audio
	audio_control_handler('pause');

	// Handler for the button to stop the audio
	audio_control_handler('stop');

	// Handler for the buttons to raise the lifts
	lift_control_handler('raise');

	// Handler for the buttons to lower the lifts
	lift_control_handler('lower');

	// Handler for the buttons to lock doors
	door_control_handler('lock');

	// Handler for the buttons to unlock doors
	door_control_handler('unlock');

	// Handler for the buttons to reset challenges
	challenge_control_handler('reset');

	// Handler for the buttons to validate challenges
	challenge_control_handler('validate');

	// Create our websocket
	create_websocket();

	// Call refresh_page() to draw the map
	refresh_page();
	refresh_page();
	refresh_page();
});
