
function switch_elements(selector1, selector2, state)
{
	// Just for debug
	//alert("Switching '" + selector1 + "' with '" + selector2 + "' " + state);

	if (state) {
		$(selector1).show();
		$(selector2).hide();
	}
	else {
		$(selector1).hide();
		$(selector2).show();
	}
}

$(document).ready(function() {

	// The slug of the current escape game
	game_slug = $('input#game-slug').val();
	if (game_slug === undefined)
		return;

	//switch_elements('button#start-escapegame', 'button#pause-escapegame', true);

	// Handler for the button to start the video
	start_but = $('button#start-escapegame');
	start_but.show();
	start_but.click(function() {

		//switch_elements('button#start-escapegame', 'button#pause-escapegame', false);

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: '/web/' + game_slug + '/start/',
			crossDomain: true,
		});
	});

	// Handler for the button to pause the video
	pause_but = $('button#pause-escapegame');
	pause_but.show();
	pause_but.click(function() {

		//switch_elements('button#start-escapegame', 'button#pause-escapegame', true);

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: '/web/' + game_slug + '/pause/',
			crossDomain: true,
		});
	});

	// Handler for the button to stop the video
	stop_but = $('button#stop-escapegame');
	stop_but.show();
	stop_but.click(function() {

		//switch_elements('button#start-escapegame', 'button#stop-escapegame', false);

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: '/web/' + game_slug + '/stop/',
			crossDomain: true,
		});
	});

	// Handler for lock buttons
	lock_buts = $('button.lock-button');
	lock_buts.click(function() {

		ok = confirm('Are you really sure you want to unlock the door?');
		if (ok !== true)
			return;

		switch_elements('button#' + this.id, 'button#un' + this.id, false);

		$.ajax({
			xhrFields: {
				withCredentials: false
			},
			url: this.value,
			crossDomain: true,
		});
	});

	// Handler for unlock buttons
	unlock_buts = $('button.unlock-button');
	unlock_buts.click(function() {

		ok = confirm('Are you really sure you want to lock the door?');
		if (ok !== true)
			return;

		switch_elements('button#' + this.id, 'button#' + this.id.substring(2), false);

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

			ctx.drawImage(map_image, 0, 0, game.map_image.width, game.map_image.height);

			if (game.sas_door_locked === false) {
				drawImage(ctx, game.sas_door_image);
			}

			if (game.corridor_door_locked === false) {
				drawImage(ctx, game.corridor_door_image);
			}

			for (var index in game.rooms) {
				var room = game.rooms[index];
				if (room.door_locked == false) {
					drawImage(ctx, room.door_unlocked_image);
				}
			}
		};
	};

	function refresh_page() {
		$.ajax({
			url: '/web/' + game_slug + '/status/',
			crossDomain: true,
			success: function(game) {

				if (typeof game === 'undefined')
					return;

				switch_elements('button#lock-sas-' + game.slug, 'button#unlock-sas-' + game.slug, game.sas_door_locked);
				switch_elements('button#lock-corridor-' + game.slug, 'button#unlock-corridor-' + game.slug, game.corridor_door_locked);

				// For each room...
				for (var index in game.rooms) {

					var room = game.rooms[index];

					switch_elements('button#lock-' + room.slug, 'button#unlock-' + room.slug, room.door_locked);

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
		console.log("websocket connected");
	};

	ws.onmessage = function(e) {
		console.log("websocket received data: " + e.data);
		refresh_page();
	};

	ws.onerror = function(e) {
		console.error(e);
	};

	ws.onclose = function(e) {
		console.log("websocket closed");
	};
});
