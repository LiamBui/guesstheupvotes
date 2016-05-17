var attempt = 1;
var runningscore = 0;
var form = '<input id="input" type="text" name="prediction" placeholder="Predict a score"></div><button type="button" class="btn"> Go! </button>';
$(document).ready(function(){
	$('#input').focus();
});

$(document).on('click','#next', function(){
	$.ajax({
		data: {attempt: attempt},
		dataType: 'json',
		success: function(output) {
			$('.comment').html(output.comment);
			$('.result').html('');
			$('.guess').html(form);
			$(function() {
				$('#input').focus(); 
			});
			attempt += 1;
			console.log(attempt-1);
		},
		error: function(output) {
			console.log(output);
			//$('body').innerHTML = '<p>Your final score is: ' + runningscore.toString() + ' out of 500</p>';
		},
		complete: function(output, textstatus) {
			console.log(textstatus);
		}
	});
});

$(document).on('click','.btn', function(){
	console.log('click button');
	$.ajax({
		data: {prediction: document.getElementById('input').value, attempt: attempt},
		dataType: 'json',
		success: function(output) {
			runningscore += Math.max(0, 100-parseInt(100 * Math.abs(output.score - parseInt(document.getElementById('input').value)) / output.score));
			if(attempt == 5){
				var result = '<h1>Your score</h1><p>Correct number of upvotes is: ' + output.score + '</p><p>Your total score is ' + runningscore.toString() + ' out of ' + (attempt * 100).toString() + '</p><a href="http://guesstheupvotes.herokuapp.com/">Try again!</a>';
			}
			else{
				var result = '<h1>Your score</h1><p>Correct number of upvotes is: ' + output.score + '</p><p>Your total score is ' + runningscore.toString() + ' out of ' + (attempt * 100).toString() + '</p><button type="button" id="next"> Next! </button>';
			}
			$('.guess').html('');
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

$(document).on('keypress', '#input', function(e){
	if(e.which == 13){
		$('.btn').click();
	}
});

