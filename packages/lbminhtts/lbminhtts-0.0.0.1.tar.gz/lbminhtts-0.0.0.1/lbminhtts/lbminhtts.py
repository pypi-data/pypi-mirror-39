# DOMAIN = 'lbminh_tts'

# import requests
# import json
# import os
# import time

# REQUIREMENTS = ['requests==1.0.2']
# def setup(hass, config):
	
def tts_call(entity_id,tts_mess,giong,url_hass):
	if __name__ == '__main__':
		

		if giong == "nam_mienbac":
		giong = "male"
		if giong == "nu_mienbac":
			giong = "female"
		if giong == "nu_miennam":
			giong = "hatieumai"
		if giong == "nu_hue":
			giong = "ngoclam"
		url = 'http://api.openfpt.vn/text2speech/v4'

		headers = {'api_key': '7121c9185cf9404595f297f23d352039','speed':'2','prosody':'1', 'voice': giong}
		payload = str(tts_mess).encode('utf-8')
		
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

		tts_link = url_hass+'local/tts.mp3'
		
		return entity_id, tts_link
	



	# services_data = {'entity_id': entity_id,'media_content_id':tts_link,'media_content_type': 'audio' }
	# hass.services.call('media_player','turn_off')
	# time.sleep(0.1)
	# hass.services.call('media_player','play_media',services_data)
		

		
		# time.sleep(5)
		# os.remove("/home/mt/.homeassistant/www/tts.mp3")
	
