#/usr/bin/env python

# imports
import json
import requests
import argparse
import logging
import bs4

# different apis for url shortener

api = {
	'bitly' : 'https://api-ssl.bitly.com/v3/shorten?format=json&login=hzlzh&apiKey=R_e8bcc43adaa5f818cc5d8a544a17d27d&longUrl={}',
    'tinyurl' : 'http://tinyurl.com/api-create.php?url={}',
	'isgd' : 'http://is.gd/create.php?format=json&url={}',
	'vgd' : 'http://v.gd/create.php?format=json&url={}',
	'tinycc' : 'http://tiny.cc/?c=rest_api&m=shorten&version=2.0.3&format=json&shortUrl=&login=hzlzh&apiKey=9f175aa2-ff30-4df5-b958-1346c59b4884&longUrl={}'
}

apiViews = {
	'bitly' : 'https://api-ssl.bitly.com/v3/link/clicks?access_token=cf33582fe16dc7cc6166f513a5b5488b473819c4&link={}',
	'isgd' : 'https://is.gd/stats.php?url={}',
	'vgd' : 'https://v.gd/stats.php?url={}',
	'tinycc' : 'http://tiny.cc/?c=rest_api&m=total_visits&version=2.0.3&format=json&hash={}&login=hzlzh&apiKey=9f175aa2-ff30-4df5-b958-1346c59b4884'
}

# get JSON if that is the output
def getJSON(service, url):
	# generate link for specified service
	apiLink = api[service].format(url)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

	# get JSON reuslt
	result = requests.get(apiLink, headers=headers).json()
	return result

# get text response if that is the output
def getText(service, url):
	# generate link for specified service
	apiLink = api[service].format(url)
	# get text result
	result = requests.get(apiLink).text
	return result

def getViewsJSON(service, id):
	# generate URL for service
	if (service == 'bitly'): # bit.ly requires entire link, not just ID
		id = "http://bit.ly/" + id

	viewsLink = apiViews[service].format(id)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

	# get JSON result
	result = requests.get(viewsLink, headers=headers).json()
	return result

def getViewsScraping(service, id):
	# generate ID
	viewsLink = apiViews[service].format(id)

	# load web page that shows views
	result = requests.get(viewsLink)
	c = result.content

	# load HTMl into beautifulsoup
	soup = bs4.BeautifulSoup(c, features="html.parser")
	div = (soup.find("div", {"id": "main"})) # get main div
	views = div.table.b.text # get number of views
	return views



def main():
	# setup arguments
	parser = argparse.ArgumentParser(description="Shorten URL using the following services: bit.ly, tinyurl, t.cn, is.gd, v.gd, tiny.cc.")
	parser.add_argument("url", help="Enter the URL to shorten here")
	parser.add_argument("-t", "--tinyurl", help="use tinyurl to shorten url", action="store_true")
	parser.add_argument("-i", "--isgd", help="use is.gd to shorten url", action="store_true")
	parser.add_argument("-v", "--vgd", help="use v.gd to shorten url", action="store_true")
	parser.add_argument("-c", "--tinycc", help="use tiny.cc to shorten url", action="store_true")
	parser.add_argument("-w", "--views", help="get total views for shortened link", action="store_true")

	parser.add_argument("-V", "--version", action='version', version='%(prog)s 1.0')
	args = parser.parse_args()

	# setup log file
	logging.basicConfig(filename="links.log", level=logging.INFO)

	# set url
	url = args.url

	service = ''
	output = ''
	outputViews = ''


	# add http to url if neccessary
	if (('http' in url) == False and not args.views):
		url = 'http://' + url

	# get shortened link
	if (args.tinyurl and not args.views):
		service = 'tinyurl'
		output = getText(service, url)

	if (args.isgd and not args.views):
		service = 'isgd'
		output = getJSON(service, url)['shorturl']

	if (args.vgd and not args.views):
		service = 'vgd'
		output = getJSON(service, url)['shorturl']

	if (args.tinycc and not args.views):
		service = 'tinycc'
		output = getJSON(service, url)['results']['short_url']

	if (service == '' and not args.views):
		service = 'bitly'
		output = getJSON(service, url)['data']['url']

	# if views arg is selected, get views
	if (args.tinyurl and args.views):
		outputViews = "Tinyurl does not support view tracking."

	if (args.isgd and args.views):
		service = 'isgd'
		outputViews = getViewsScraping(service, url)

	if (args.vgd and args.views):
		service = 'vgd'
		outputViews = getViewsScraping(service, url)

	if (args.tinycc and args.views):
		service = 'tinycc'
		outputViews = getViewsJSON(service, url)['results']['clicks']

	if (service == '' and args.views):
		service = 'bitly'
		outputViews = getViewsJSON(service, url)['data']['link_clicks']

	if (output != ''):
		print ("Shortened URL: " + output)
		logging.info(" Shortened: " + output + " Original: " + url)
	elif (outputViews != ''):
		print("Total views: " + str(outputViews))
	else:
		print ("Error, please try again.")

if __name__ == '__main__':
    main()
