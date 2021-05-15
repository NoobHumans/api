import bs4,requests,json;from datetime import *
mozhdr,z,harii={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"},{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"},["Senin","Selasa","Rabu","Kamis","Jum'at","Sabtu","Minggu"]
class h:
	def bs(link,hdr=True):
		if hdr == False:return bs4.BeautifulSoup(requests.get(link).content, "html.parser")
		else:return bs4.BeautifulSoup(requests.get(link,headers=z).content, "html.parser")
	def pj(jsonnya):print(json.dumps(jsonnya,indent=4,ensure_ascii=False))
	def bsverif(link,hdr=True):
		if hdr == False:return bs4.BeautifulSoup(requests.get(link,verify=False).content, "html.parser")
		else:return bs4.BeautifulSoup(requests.get(link,verify=False,headers=mozhdr).content, "html.parser")