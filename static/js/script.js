
function switch_elements(selector1, selector2, state)
{
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

	slug = $('input#game-slug').val();

	switch_elements('button#start-escapegame', 'button#stop-escapegame', true);

	start_but = $('button#start-escapegame');
	start_but.click(function() {

		switch_elements('button#start-escapegame', 'button#stop-escapegame', false);

		$.ajax({
			url: '/escapegame/' + slug + '/start',
		});
	});

	stop_but = $('button#stop-escapegame')
	stop_but.click(function() {

		switch_elements('button#start-escapegame', 'button#stop-escapegame', true);

		$.ajax({
			url: '/escapegame/' + slug + '/reset',
		});
	});

	lock_buts = $('button.lock-button');
	lock_buts.click(function() {

		switch_elements('button#' + this.id, 'button#un' + this.id, false);

		$.ajax({
			url: '/escapegame/' + slug + '/door/' + this.val() + '/unlock',
		});
	});

	unlock_buts = $('button.unlock-button');
	unlock_buts.click(function() {

		switch_elements('button#' + this.id, 'button#' + this.id.substring(2), false);

		$.ajax({
			url: '/escapegame/' + slug + '/door/' + this.val() + '/lock',
		});
	});

	$.ajax({
		url: '/escapegame/' + slug + '/status',
		success: function(game) {

			if (typeof game === 'undefined')
				return;

			switch_elements('button#lock-sas-' + game.slug, 'button#unlock-sas-' + game.slug, true);
			switch_elements('button#lock-corridor-' + game.slug, 'button#unlock-corridor-' + game.slug, true);

			// For each room...
			for (var index in game.rooms) {

				var room = game.rooms[index];

				switch_elements('button#lock-' + room.slug, 'button#unlock-' + room.slug, true);

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
