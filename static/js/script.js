
$(document).ready(function() {

	$('#play-video').click(function() {

		var video = $('#play-video').val();

		$.ajax({
			url: '/video/play/' + video,
		});
	});
});
