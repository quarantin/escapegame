
$(document).ready(function() {

	var slug = $('#slug').val();

	$('#start-escapegame').click(function() {

		$.ajax({
			url: '/escapegame/' + slug + '/start',
		});
	});


	$('#stop-escapegame').click(function() {

		$.ajax({
			url: '/escapegame/' + slug + '/reset',
		});
	});

	$.ajax({
		url: '/escapegame/' + slug + '/challenge/status',
		success: function(data) {
			alert(data['escapegame_name']);
		},
	});

});
