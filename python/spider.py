import requests as rq
from bs4 import BeautifulSoup as bs
import time
import random
import multiprocessing as mp
from functools import reduce

def getIPProxy(url):
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
    soup = bs(rq.get(url, headers = headers, timeout = 20,proxies = {'proxy':'http://114.99.13.171:21686'}).text, 'lxml')
    time.sleep(random.random()*5)
    ip_hosts = soup.select('#ip_list tr')
    ips = [item.select('td')[1].text + ':' + item.select('td')[2].text for item in ip_hosts[1:]]
    return ips

def testIP(ip):
		headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
		url = 'http://www.baidu.com/'
		status = 'ok'
		try:
				resp = rq.get(url, proxies = {'proxy':ip}, headers = headers, timeout = 20)
				print(resp)
		except:
				status = 'no'
		if status is 'ok':
				return ip
		else:
				return None
			

def getProxyPool(pages):
    pool = mp.Pool(processes = 10)
    pageurls = ['http://www.xicidaili.com/nn/' + str(i) for i in range(1,pages)]
    proxyPools = pool.map(getIPProxy, pageurls)
    proxyPool = list(map(lambda x : r'http://'+x,reduce(lambda x, y : x+y,proxyPools)))
    result = pool.map(testIP, proxyPool)
    ippool = list(filter(lambda elem : elem != None, result))
    pool.close()
    pool.join()
    print('----------IP Proxy Pool Finished----------')
    return ippool
    
if __name__ == '__main__':
		proxies = getProxyPool(10)
		with open(r'C:\Users\chengsong\Desktop\proxies.txt', 'w') as writer:
			for proxy in proxies:
				writer.write(proxy + '\n')
		
			
		