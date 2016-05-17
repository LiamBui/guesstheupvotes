var attempt = 1;
var runningscore = 0;
var form = '<input id="input" type="text" name="prediction" placeholder="Predict a score"></div><button type="button" class="btn"> Go! </button>';

$('#next').click(function(){
	console.log('next');
	$.ajax({
		data: {attempt: attempt},
		dataType: 'json',
		success: function(output) {
			$('.comment').html(output.comment);
			$('.result').html('');
			$('.guess').html(form);
		},
		error: function(output) {
			console.log(output);
		},
		complete: function(output, textstatus) {
			console.log(textstatus);
		}
	});
	attempt += 1;
});

$('.btn').click(function(){
	console.log('click button');
	$.ajax({
		data: {prediction: $('#input').val(), attempt: attempt},
		dataType: 'json',
		success: function(output) {
			$('.guess').html('');
			runningscore += output[1];
			var result = '<h1>Your score</h1><p>Correct number of upvotes is: ' + output[0].score + '</p><p>Your total score is ' + runningscore + ' out of ' + toString(attempt * 100) + '</p><a id="next">Next</a>';
			$('.result').html(result);
		},
		error: function(output) {
			console.log(output);
		},
		complete: function(output, textstatus) {
			console.log(textstatus);
		}
	});
});