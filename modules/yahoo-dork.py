#!/usr/bin/env python
# coding: utf-8

import os
import pychrome
import urlparse
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
from pocsuite.lib.core.data import paths,logger
from pocsuite.lib.core.common import getUnicode
from pocsuite.lib.core.common import normalizeUnicode
from pocsuite.lib.core.enums import CUSTOM_LOGGING


# 环境配置:
# 	本地配置chrome的headless，执行如下命令:
# 	headless mode (chrome version >= 59):
# 	$ google-chrome --headless --disable-gpu --remote-debugging-port=9222

# 	或者直接使用docker
# 	$ docker pull fate0/headless-chrome
# 	$ docker run -it --rm --cap-add=SYS_ADMIN -p9222:9222 fate0/headless-chrome

# 	PS:使用google-dork等需要那啥的时候打开ss就好

# 使用说明:
# 	对目标使用搜索dork语法，程序会返回抓取的域名
# 	python pocsuite.py -r modules/yahoo-dork.py -u site:i.mi.com --verify
# 	默认对域名做了去重输出，根据需要可以修改script


class Dork(POCBase):
	vulID = '0'  # ssvid
	version = '1.0'
	author = ['z3r0yu']
	vulDate = '2018-12-22'
	createDate = '2018-12-22'
	updateDate = '2018-12-22'
	references = ['https://zeroyu.xyz/']
	name = 'yahoo dork'
	appPowerLink = 'https://search.yahoo.com/'
	appName = 'yahoo-dork'
	appVersion = '1'
	vulType = 'search dork'
	desc = '''
	   使用chrome headless对使用yahoo搜索引擎的搜索结果进行抓取
	'''
	samples = ['site:i.mi.com']
	install_requires = ['pychrome']


	def SearchDork(self,target):

		browser = pychrome.Browser(url="http://127.0.0.1:9222")
		tab = browser.new_tab()
		tab.start()
		tab.Page.enable()
		tab.Network.enable()
		tab.Runtime.enable()
		step=1
		subdomins=[]
		while(1):

			url="https://search.yahoo.com/search?p={}".format(target)
			url=url+"&b={}&pz=40".format(step)
			step=step+40

			try:
				# call method with timeout
				tab.Page.navigate(url=url, _timeout=5)
				tab.wait(5)

				exp='document.getElementsByClassName(" ac-algo fz-l ac-21th lh-24").length'
				length= tab.Runtime.evaluate(expression=exp)		

				if length['result']['value']==0:
					break

				for l in range(0,length['result']['value']):
					# tab.wait(1)
					exp1='document.getElementsByClassName(" ac-algo fz-l ac-21th lh-24")[{}].href'.format(l)
					res1= tab.Runtime.evaluate(expression=exp1)
					logger.info(res1['result']['value'])
					subdomins.append(res1['result']['value'])
			except:
				pass

		tab.stop()
		browser.close_tab(tab)
		return subdomins

	def _output2file(self,outputPath,msg):
		with open(outputPath,'a') as f:
			for m in msg:
				f.write(m + '\n')

	def _attack(self):
		return self._verify() 

	def _verify(self):
		result = {}
		DorkGrammar = self.url.replace("http://","")
		subdomins=self.SearchDork(DorkGrammar)
		tmp=[]
		for sub in subdomins:
			url=urlparse.urlparse(sub)
			tmp.append(url.scheme+"://"+url.netloc)
		# 去重
		subdomins=list(set(tmp))
		result['VerifyInfo'] = {}
		outputPath = os.path.join(getUnicode(paths.POCSUITE_OUTPUT_PATH), normalizeUnicode(getUnicode(DorkGrammar)))
		outputPath = os.path.join(outputPath,"yahoo2result.txt")
		j=1
		if subdomins:
			self._output2file(outputPath,subdomins)	
			for s in subdomins:
				t="URL"+str(j)
				result['VerifyInfo'][t] = s
				j=j+1
		outputPathInfo="outpath:"+outputPath
		logger.log(CUSTOM_LOGGING.SYSINFO, outputPathInfo)
		return self.parse_output(result)

	def parse_output(self, result):
		#parse output
		output = Output(self)
		if result['VerifyInfo']:
			output.success(result)
		else:
			output.fail('Find nothing or Internet error~')
		return output


register(Dork)