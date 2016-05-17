from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, RequestContext
import praw
import random
import math
import json

def index(request):
	r = praw.Reddit(user_agent = "Guesstheupvotes by /u/guesstheupvotes")
	global output

	if not request.GET.get('prediction'):
		if not request.GET.get('attempt'):
			output = []
			askreddit = r.get_subreddit('askreddit')
			top_submissions = list(askreddit.get_top_from_all(limit=100))
			for i in range(0,5):
				listing = {}			
				listings = top_submissions[random.randint(0,99)]
				comment = listings.comments[random.randint(0,len(listings.comments)-1)]
				while (not hasattr(comment, 'body_html')):
					comment = listings.comments[random.randint(0,len(listings.comments)-1)]
				listing['comment'] = comment.body_html
				listing['score'] = comment.score
				listing['permalink'] = comment.permalink
				output.append(listing)
			return render_to_response('index.html',{'listing': output[0]})
		elif not request.GET.get('truth'):
			attempt = int(request.GET.get('attempt'))
			return HttpResponse(json.dumps(output[attempt]), content_type="application/json")
	else:
		if request.GET.get('truth'):
			attempt = int(request.GET.get('attempt'))
			return HttpResponse(json.dumps(output[attempt]), content_type="application/json")
		else:
			attempt = int(request.GET.get('attempt'))
			return HttpResponse(json.dumps(output[attempt-1]), content_type="application/json")

