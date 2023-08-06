
class tts():
	import requests
	import json


	def __init__(self,tts_mess,giong):
		
		self.tts_mess = tts_mess
		self.giong = giong
		
	def requestlink(self):
		import requests
		if self.giong == "nam_mienbac":
			self.giong = "male"
		if self.giong == "nu_mienbac":
			self.giong = "female"
		if self.giong == "nu_miennam":
			self.giong = "hatieumai"
		if self.giong == "nu_hue":
			self.giong = "ngoclam"
		
		self.url = 'http://api.openfpt.vn/text2speech/v4'

		self.headers = {'api_key': '7121c9185cf9404595f297f23d352039','speed':'2','prosody':'1', 'voice': self.giong}
		self.payload = str(self.tts_mess).encode('utf-8')
		r = requests.post(self.url, data=self.payload, headers=self.headers)
		datajson = r.json()
		datajson=datajson['async']
		urltts = datajson
		
		return urltts
			
class kiemtrafile():
	
	def __init__(self,link,dirfile = "/home/mt/.homeassistant/www/tts.mp3"):
		self.link = link
		self.dirfile = dirfile
		
	def checkfile(self):
		import os
		import time
		
		self.filesize = 1
		while self.filesize < 2000:
			time.sleep(0.2)
			r = requests.get(self.link)
			with open(dirfile, 'wb') as f:
				f.write(r.content)
			f.close()
			filesize = int(os.path.getsize(dirfile))



	
