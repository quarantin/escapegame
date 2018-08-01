
$(document).ready(function() {

	$('#start-escapegame').click(function() {

		var slug = $('#start-escapegame').val();

		$.ajax({
			url: '/escapegame/' + slug + '/start',
		});
	});


	$('#stop-escapegame').click(function() {

		var slug = $('#stop-escapegame').val();

		$.ajax({
			url: '/escapegame/' + slug + '/reset',
		});
	});

});
