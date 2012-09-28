import urllib, time, json, logging
from google.appengine.api import memcache

def chunks(l,n):
	for i in xrange(0, len(l), n):
		yield l[i:i+n] 

def pull_stocks():
	logging.info('Processing stocks start.')
	f = open('symbols.txt', 'r')
	symbols = [x.replace("\n", "") for x in f]   
	blocks = list(chunks(symbols, 100))
	output = {}
	for symbol_block in list(chunks(symbols, 100)):
		query = "+".join(symbol_block)
		url = "http://finance.yahoo.com/d/quotes.csv?s="+query+"&f=sl1"
		result = urllib.urlopen(url)
		for line in result.readlines():
			split = line.split(",")
			symbol = str(split[0].replace("\"", ""))
			price = split[1].replace("\r\n", "")
			output[symbol] = price
	memcache.add("whole_nyse", output)
	time.sleep(300)
	deferred.defer(pull_stocks, _countdown=3)
	logging.info('Processing stocks done.')
	return output
