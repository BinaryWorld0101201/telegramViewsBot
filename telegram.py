#!/usr/bin/python

import threadManager
import proxylist
import threading
import requests
import re
import sys

# colors
read 	= "\033[0;31m"
green	= "\033[0;32m"
white	= "\033[0;37m"
yellow  = "\033[0;33m"

stats_format = white+"Stats: views :"+green+"{:^3}"+white+", errors: "+read+"{:^3}"+white+", fails: "+yellow+"{:^3}\r"

# params
curr_proxy = 0
proxies = None
lock = threading.Lock()

agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; Xbox)'

Headers = {
        'Host': 't.me',
        'User-Agent': agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': "",
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

postData = {'_rl': 1}

# stats
views  = 0
errors = 0
fails  = 0

def stats_displayer():
	global views
	global errors
	global fails
	global stats_format

	while True:
		print(stats_format.format(views, errors, fails),end='')


def worker(post_link):
	global proxies
	global Headers
	global views
	global errors
	global fails
	global postData
	global curr_proxy
	global lock

        sess = requests.session()

	while True:

		try:
			link = '{}{}'.format(post_link, '?embed=1')
			proxy = {
					'http': proxies[curr_proxy],
					'https': proxies[curr_proxy]
				}

			# send request
			req = sess.get(link, proxies=proxy, headers=Headers, timeout=10)
			Data = re.findall('data-view="(.*)"', req.text.encode('utf8'))[0].split('" data-view="')[0]

			Headers['Content-type'] = 'application/x-www-form-urlencoded'
			Headers['Referer'] = link
			# post req
			sess.post(link, proxies=proxy, data=postData, headers=Headers, timeout=10)

			Headers['Cookie'] = req.headers.get('Set-Cookie')
			# 3rd req
			req = sess.get('https://t.me/v/?views={}'.format(Data), proxies=proxy, headers=Headers, timeout=10)

			if req.text == 'true':
				views += 1
			else:
				fails += 1
		except:
			errors	      += 1


		# next proxy
		lock.acquire()
		curr_proxy += 1

		if curr_proxy >= len(proxies):
			curr_proxy = 0
		lock.release()

def main():
	global proxies
	postLink   = input('>>> Enter telegram channel post link: ')
	# get proxies
	proxy_type = input('[0] Http\n[1] Socks4\n[2] Socks5\n>>> Enter proxy type:')
	while not ('0'<= proxy_type <= '2'):
		proxy_type = input('[0] Http\n[1] Socks4\n[2] Socks5\n>>> Enter proxy type:')

	filename = input('Enter proxies path: ')
	filename = filename.replace("'", "")
	filename = filename.replace("\"", "")

	try:
		proxies = proxylist.proxylist(filename=filename, proxy_type=int(proxy_type))
		nthreads = input('>>> Threads(1-200): ')

		tm = threadManager.ThreadManager(worker, nthreads=int(nthreads), args=(postLink,))

		tm.start()

		stats = threading.Thread(target=stats_displayer)
		stats.daemon = True
		stats.start()

	except Exception as e:
		print(str(e))
		sys.exit(1)

if __name__ == '__main__':
	main()
