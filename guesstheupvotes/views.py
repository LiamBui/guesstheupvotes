from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, RequestContext
import praw
import random
import math



def index(request):

	r = praw.Reddit(user_agent = "Guesstheupvotes by /u/guesstheupvotes")
	listing = {}
	predicted = False
	runningscore = 0
	attempts = 0

	if not request.GET.get('runningscore'):
		#r.login('guesstheupvotes','yomamasux780', disable_warning=True)
		askreddit = r.get_subreddit('askreddit')
		listings = list(askreddit.get_top_from_all(limit=100))[random.randint(0,99)]
		comment = listings.comments[random.randint(0,len(listings.comments)-1)]

		while (not hasattr(comment, 'body_html')):
			comment = listings.comments[random.randint(0,len(listings.comments)-1)]

		listing['comment'] = comment.body_html
		listing['score'] = comment.score
		listing['permalink'] = comment.permalink

	if request.GET.get('runningscore'):
		if not request.GET.get('prediction'):
			askreddit = r.get_subreddit('askreddit')
			listings = list(askreddit.get_top_from_all(limit=100))[random.randint(0,99)]
			comment = listings.comments[random.randint(0,len(listings.comments)-1)]

			while (not hasattr(comment, 'body_html')):
				comment = listings.comments[random.randint(0,len(listings.comments)-1)]

			listing['comment'] = comment.body_html
			listing['score'] = comment.score
			listing['permalink'] = comment.permalink
			runningscore = int(request.GET.get('runningscore'))
			attempts = int(request.GET.get('attempts'))

		if request.GET.get('prediction'):
			predicted = True
			prediction = int(request.GET.get('prediction'))
			permalink = request.GET.get('permalink')
			runningscore = int(request.GET.get('runningscore'))
			attempts = int(request.GET.get('attempts'))
			comment = r.get_submission(permalink).comments[0]
			listing['comment'] = comment.body_html
			listing['score'] = comment.score
			listing['permalink'] = comment.permalink
			runningscore += max((100 - int(100 * math.fabs(comment.score - prediction) / comment.score)), 0)
			attempts += 1
			if attempts == 5:
				return render_to_response('final_score.html',{'runningscore': runningscore})

	return render_to_response('index.html',{'listing': listing, 'predicted': predicted, 'runningscore': runningscore, 'attempts': attempts})