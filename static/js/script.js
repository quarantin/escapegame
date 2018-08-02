$(document).ready(function() {

	start_but = $('button#start-escapegame');
	stop_but = $('button#stop-escapegame')

	lock_buts = $('button.lock-button');
	unlock_buts = $('button.unlock-button');

	start_but.show();
	stop_but.hide();

	lock_buts.show();
	unlock_buts.hide();

	slug = $('input#game-slug').val();

	start_but.click(function() {

		start_but.hide();
		stop_but.show();

		$.ajax({
			url: '/escapegame/' + slug + '/start',
		});
	});

	stop_but.click(function() {

		stop_but.hide();
		start_but.show();

		$.ajax({
			url: '/escapegame/' + slug + '/reset',
		});
	});

	lock_buts.click(function() {

		lock_but = $('button#' + this.id);
		unlock_but = $('button#un' + this.id);

		lock_but.hide();
		unlock_but.show();
	});

	unlock_buts.click(function() {

		unlock_but = $('button#' + this.id);
		lock_but = $('button#' + this.id.substring(2));

		lock_but.show();
		unlock_but.hide();
	});

	$.ajax({
		url: '/escapegame/' + slug + '/challenge/status',
		success: function(data) {

			if (typeof data === 'undefined')
				return;

			// For each room...
			for (var index in data.rooms) {

				var room = data.rooms[index];

				alert("room.door_locked = " + room.door_locked);
				if (room.door_locked === true) {
					$('button#lock-' + room.slug).show();
					$('button#unlock-' + room.slug).hide();
				}
				else {
					$('button#lock-' + room.slug).hide();
					$('button#unlock-' + room.slug).show();
				}

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
						html += '\t<tr>\n\t\t<td>' + chall.name + "</td>\n\t\t<td>" + solved + '</td>\n\t</tr>\n';

					}

					html = '<table>\n' + html + '</table>\n';
				}

				statusdiv.html(html);
			}
		},
	});
});
