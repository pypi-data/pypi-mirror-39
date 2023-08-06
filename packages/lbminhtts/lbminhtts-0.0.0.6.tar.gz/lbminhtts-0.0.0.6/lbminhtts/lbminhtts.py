# DOMAIN = 'lbminh_tts'

# import requests
# import json
# import os
# import time

# REQUIREMENTS = ['requests==1.0.2']
# def setup(hass, config):
class tts():
	import requests
	import time
	import os
	import json


	def __init__(self,entity_id,tts_mess,giong,url_hass):
		self.entity_id = entity_id
		self.tts_mess = tts_mess
		self.giong = giong
		self.url_hass = url_hass
	def tts_call(self):
		if self.giong == "nam_mienbac":
			self.giong = "male"
		if self.giong == "nu_mienbac":
			self.giong = "female"
		if self.giong == "nu_miennam":
			self.giong = "hatieumai"
		if self.giong == "nu_hue":
			self.giong = "ngoclam"
		url = 'http://api.openfpt.vn/text2speech/v4'

		headers = {'api_key': '7121c9185cf9404595f297f23d352039','speed':'2','prosody':'1', 'voice': self.giong}
		payload = str(self.tts_mess).encode('utf-8')
		
		r = requests.post(url, data=payload, headers=headers)
		datajson = r.json()
		datajson=datajson['async']
		urltts = datajson
		while filesize < 2000:
			time.sleep(0.2)
			r = requests.get(urltts)
			with open('/home/mt/.homeassistant/www/tts.mp3', 'wb') as f:
				f.write(r.content)
			f.close()
			filesize = int(os.path.getsize("/home/mt/.homeassistant/www/tts.mp3"))

		tts_link = self.url_hass+'local/tts.mp3'
			
		return self.entity_id, tts_link		
	



	# services_data = {'entity_id': entity_id,'media_content_id':tts_link,'media_content_type': 'audio' }
	# hass.services.call('media_player','turn_off')
	# time.sleep(0.1)
	# hass.services.call('media_player','play_media',services_data)
		

		
		# time.sleep(5)
		# os.remove("/home/mt/.homeassistant/www/tts.mp3")
	
