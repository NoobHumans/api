import requests, html5lib, json, random, cloudscraper
from bs4 import BeautifulSoup as bs
import hmac, hashlib, base64, time, datetime
from urllib.parse import urlencode

def pj(jsonnya):print(json.dumps(jsonnya,indent=4,ensure_ascii=False))

r = cloudscraper.create_scraper()

s = requests.Session()

def make_digest(message, key):
    key     = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')
    digester = hmac.new(key, message, hashlib.sha1)
    sig = digester.hexdigest()
    return sig

def ts_gen():
	d = datetime.datetime.now()
	unixtime = datetime.datetime.timestamp(d)*1000
	str_ = str(unixtime)
	return str_.split('.')[0]

class image_maker:

	def ver_1(template_id, url_image):
		header_upload = {
			'Accept': '*/*',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Host': 'temp.ws.pho.to',
			'Origin': 'https://funny.pho.to',
			'Referer': 'https://funny.pho.to/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.0 Safari/537.36'
		}

		form_data_upload = {
			'files[1][path]': url_image,
			'r': '6945238',
			'gen_preview': '1',
			'resizeWidth': '1200'
		}

		upload = s.post(
			url='https://temp.ws.pho.to/upload.php',
			headers=header_upload,
			data=form_data_upload
			)

		xml = f'<image_process_call><image_url order="1">{upload.text}</image_url><methods_list><method order="1"><name>collage</name><params>template_name={template_id}</params></method></methods_list><result_size>1400</result_size><result_quality>90</result_quality><template_watermark>true</template_watermark><lang>en</lang><abort_methods_chain_on_error>true</abort_methods_chain_on_error></image_process_call>'
		key = 'd6ca8626f27c5c4d371ff74464c4947a'

		queue_data = {
			'app_id': '680478baa1933902787cded755b141a1',
			'data': xml,
			'sign_data': make_digest(xml, key)
			}

		queue_headers = {
			'Accept': 'application/xml, text/xml, */*; q=0.01',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Host': 'opeapi.ws.pho.to',
			'Origin': 'https://funny.pho.to',
			'Referer': 'https://funny.pho.to/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.0 Safari/537.36'
		}

		queue = requests.post(
			url='https://opeapi.ws.pho.to/queue_url.php?service_id=7',
			headers=queue_headers,
			data=queue_data,
			params=urlencode({'service_id': '7'})
			)

		bs_queue = bs(queue.text, 'lxml')
		request_id = bs_queue.find('request_id').text

		url_get_result = f'https://opeapi.ws.pho.to/get-result.php?request_id={request_id}&_={ts_gen}'
		time.sleep(3)
		get_result = bs(requests.get(
			url=url_get_result,
			headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.0 Safari/537.36'},
			).text, 'lxml')

		result_url = get_result.find('result_url').text
		return result_url