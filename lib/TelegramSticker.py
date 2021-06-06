import requests, urllib.parse, json



def getSticker(name):
	token  = "1509501513:AAH6zWa3qKl2jJMXKj9m7KQ7ucEd4tOnsO0"
	api = 'https://api.telegram.org/bot{}/'.format(token)
	params = {"name":name}
	param_string = '?' + urllib.parse.urlencode(params)
	fstring = "getStickerSet"
	link_api = '{}{}{}'.format(api, fstring, param_string)
	url = requests.get(link_api).json()
	#link='https://api.telegram.org/file/bot{}/{}'.format(token, url['result']['file_id'])
	return url

def getStickerFile(file_id):
	token  = "1509501513:AAH6zWa3qKl2jJMXKj9m7KQ7ucEd4tOnsO0"
	api = 'https://api.telegram.org/bot{}/'.format(token)
	params = {"file_id":file_id}
	param_string = '?' + urllib.parse.urlencode(params)
	fstring = "getFile"
	url = requests.get('{}{}{}'.format(api, fstring, param_string)).json()
	link=url['result']['file_path']
	return link

#print(json.dumps(getSticker("LINE_Menhera_chan_ENG"),indent=4,ensure_ascii=False))
#print(getStickerFile("CAACAgIAAxUAAWBgVbBzUzf3bbXLS_-hJS4OKslZAAK0PwAC4KOCByT3eeG020JOHgQ"))

