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
function get_selected_raspi(media)
{
	raspi = $('input[name=selected-raspberry-pi-' + media + ']:checked');

	return (raspi.length > 0 ? raspi : false);
}

/*
 * Return the media URL for the media selected in select field.
 */
function get_media_url(media, action)
{
	selected_media = $('#selected-' + media).val();
	selected_raspi = get_selected_raspi(media);

	raspi_url = '';
	if (selected_raspi)
		raspi_url = selected_raspi.data('raspi-url');

	return raspi_url + '/' + get_language() + '/api/video/' + selected_media + '/' + action + '/';
}

/*
 * Initialize media buttons for the supplied media
 */
function init_media_buttons(media)
{
	$('button#' + media + '-play').removeClass('d-none');
	$('button#' + media + '-pause').addClass('d-none');
	$('button#' + media + '-rewind').addClass('button-disabled');
	$('button#' + media + '-stop').addClass('button-disabled');
	$('button#' + media + '-fast-forward').addClass('button-disabled');
	$('button#' + media + '-volume-down').addClass('button-disabled');
	$('button#' + media + '-volume-up').addClass('button-disabled');
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
	var media_type = raspi.media_type;
	var no_media = $('select#selected-' + media_type).length === 0;

	var span = $('#raspberry-pi-' + raspi.slug);
	var input = span.parent().find('input');

	span.removeClass('badge-' + raspi.not_badge);
	span.addClass('badge-' + raspi.badge);
	span.text(raspi.status);
	input.prop('disabled', !raspi.online || no_media);

	if (!raspi.online)
		input.prop('checked', false);

	selected_raspi_video = get_selected_raspi('video');
	selected_raspi_audio = get_selected_raspi('audio');

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
	image.src = '/media/' + imageObj.path;
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

	if (!game.map_image)
		return;

	var map = new Image();

	map.onload = function() {

		canvas.width = map.width;
		canvas.height = map.height;
		ctx.drawImage(map, 0, 0, map.width, map.height);

		for (index in game.rooms) {

			var room = game.rooms[index];
			if (room.door_image && !room.door.locked)
				draw_image(ctx, room.door_image);
		}
	};

	map.src = '/media/' + game.map_image.path;
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

				init_media_buttons('video');
				init_media_buttons('audio');

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
 * Assign click event handler for media control buttons.
 */
function media_control_handler(media, action)
{
	$('select#selected-' + media).change(function() {
		init_media_buttons(media);
	});

	$('button#' + media + '-' + action).click(function() {

		var disabled = $(this).hasClass('button-disabled');
		if (disabled)
			return;

		if (action == 'play') {

			$('button#' + media + '-rewind').removeClass('button-disabled');
			$('button#' + media + '-play').addClass('d-none');
			$('button#' + media + '-pause').removeClass('d-none');
			$('button#' + media + '-stop').removeClass('button-disabled');
			$('button#' + media + '-fast-forward').removeClass('button-disabled');
			$('button#' + media + '-volume-down').removeClass('button-disabled');
			$('button#' + media + '-volume-up').removeClass('button-disabled');
		}
		else if (action == 'pause' || action == 'stop') {

			$('button#' + media + '-play').removeClass('d-none');
			$('button#' + media + '-pause').addClass('d-none');

			if (action == 'stop')
				init_media_buttons(media);
		}

		var media_url = get_media_url(media, action);

		$.ajax({
			url: media_url,
			timeout: timeout,
			success: function() {
				//refresh_page();
			},
			error: function() {
				alert('Could not connect to URL: ' + media_url);
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

		var disabled = $(this).hasClass('button-disabled');
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

		var disabled = $(this).hasClass('button-disabled');
		if (disabled)
			return;

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

		var disabled = $(this).hasClass('button-disabled');
		if (disabled)
			return;

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

	media_types = [
		'video',
		'audio',
	];

	actions = [
		'play',
		'pause',
		'stop',
		'rewind',
		'fast-forward',
		'volume-down',
		'volume-up',
	];

	// Handler for the button to reset the escape game
	game_control_handler('reset');

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

	// Handlers for all media player buttons
	for (media_index in media_types) {

		media = media_types[media_index];

		for (action_index in actions) {

			action = actions[action_index]

			media_control_handler(media, action);
		}
	}

	// Create our websocket
	create_websocket();

	// Call refresh_page() to draw the map
	refresh_page();
});
