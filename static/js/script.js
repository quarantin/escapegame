
$(document).ready(function() {

	$('#play-video').click(function() {

		var filename = $('#play-video').val();

		$.ajax({
			url: '/video/play/' + filename,
		});
	});
});
