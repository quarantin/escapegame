$(document).ready(function() {

	var slug = $('input#game-slug').val();

	$('#start-escapegame').show();
	$('#stop-escapegame').hide();

	$('#start-escapegame').click(function() {

		$('#start-escapegame').hide();
		$('#stop-escapegame').show();

		$.ajax({
			url: '/escapegame/' + slug + '/start',
		});
	});

	$('#stop-escapegame').click(function() {

		$('#stop-escapegame').hide();
		$('#start-escapegame').show();

		$.ajax({
			url: '/escapegame/' + slug + '/reset',
		});
	});

	$.ajax({
		url: '/escapegame/' + slug + '/challenge/status',
		success: function(data) {

			if (typeof data === 'undefined')
				return;

			for (var index in data['rooms']) {
				var room = data['rooms'][index];
				var html = '\t<tr>\n\t\t<th>Enigmes</th>\n\t\t<th>Statut</th></tr>\n';
				var datadiv = $('div#' + room.slug).find('div#' + room.slug + '-data');
				for (var subindex in room['challenges']) {
					var chall = room['challenges'][subindex];
					var solved = '<img src="/static/admin/img/' + (chall.solved ? 'icon-yes.svg' : 'icon-no.svg') + '"/>';
					html += '\t<tr>\n\t\t<td>' + chall.name + "</td>\n\t\t<td>" + solved + '</td>\n\t</tr>\n';

				}

				datadiv.html('<table>\n' + html + '</table>\n');
			}
		},
	});
});
