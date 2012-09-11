from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core import serializers
from datetime import date
from datetime import timedelta

import simplejson
import urllib2
import re

def twitter(request, query, lang):
	today = date.today()
	one_day = timedelta(days = 1)
	yesterday = today - one_day
	tweet_short_urls = {}
	locale = {
		'it': "lang=it&geocode=41.8954656%2C12.4823243%2C500mi",
	}

	for i in range(1, 2):
		# url = "http://search.twitter.com/search.json?filter[]=links&result_type=mixed&rpp=100&since=" + today.isoformat() + "&page=" + str(i) + "&lang=" +  + "&q=" + query
		url = "http://search.twitter.com/search.json?filter[]=links&rpp=100&lang=" + lang + "&since=" + yesterday.isoformat() + "&until=" + yesterday.isoformat() + "&page=" + str(i) + "&ands=" + query
		content = urllib2.urlopen(url).read()
		json = simplejson.loads(content)

		#if i == 1:
		#	max_id = json.get("max_id")

		for tweet in json.get("results"):
			tweet_short_url = re.search("(?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", tweet.get("text")).group("url")

			try:
				tweet_url = urllib2.urlopen(tweet_short_url).url
			except:
				tweet_url = tweet_short_url
			
			if tweet_url in tweet_short_urls:
				tweet_short_urls[tweet_url] += 1
			else:
				tweet_short_urls[tweet_url] = 1

	#tweet_urls = {}

	#for url, nbr in tweet_urls:
	#	tweet_short_urls = urlparse(url)[1]
	#	break
	#	if urlparse(url)[1] == "bit.ly":
	#		short_url = urllib2.urlopen(url).url
			
	#		if not short_url in tweet_urls:
	#			tweet_urls[short_url] = nbr
	#		else:
	#			tweet_urls[short_url] += nbr
		
	return render_to_response(
		'fetch/twitter.html',
			{'tweet_urls': tweet_short_urls,
			}
	)
