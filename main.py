#from lib.pytube import YouTube
from lib.dewa import *
from lib.anime import *
from lib.search import *
from urllib.parse import *
from datetime import *
from flask import *
from lib.sn import h
from lib.scraper import scr
from lib.xpath import Xpath
from crop import cropping as crop
from bs4 import BeautifulSoup as bs
from requests import get, post
import urllib.request
from youtubesearchpython import *
from hurry.filesize import size
from werkzeug.utils import secure_filename
from PIL import Image, ImageFile
import os, math, json, random, re, html_text, base64, time, smtplib, pickle, cloudscraper, io, requests, qrcode, string, tempfile
from flask_ipban import IpBan


ua_ig = 'Mozilla/5.0 (Linux; Android 9; SM-A102U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Instagram 155.0.0.37.107 Android (28/9; 320dpi; 720x1468; samsung; SM-A102U; a10e; exynos7885; en_US; 239490550)'

app = Flask(__name__)
apiKey = 'rambu'
apiKey_ocr = '09731daace88957'
app.config['MEDIA'] = 'tts'
app.config['JSON_SORT_KEYS'] = False
app.secret_key = b'BB,^z\x90\x88?\xcf\xbb'


ip_ban = IpBan()
ip_ban.init_app(app)
ip_ban.block('13.212.185.200', permanent=True, no_write=False, timestamp=None, url='badjingan')

UPLOAD_FOLDER = 'file'
UPLOAD_TTS = 'tts'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_PDF = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_TTS'] = UPLOAD_TTS

#net = detect.load_model(model_name="u2netp")

os.environ['TZ'] = 'Asia/Jakarta'

def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return '%s %s' % (s, size_name[i])


def shortener(url):
    data = {'u': url}
    p = bs(requests.post('https://www.shorturl.at/shortener.php', data).text, 'html.parser').find('input', id='shortenurl')['value']
    return 'https://'+p

def id_generator(size=25, chars=string.ascii_uppercase + string.digits+string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def apng2gif(url):
    r = cloudscraper.create_scraper()
    res = bs(r.post('https://s7.ezgif.com/apng-to-gif', data={'new-image': '(binary)', 'new-image-url': url}).text, 'html.parser')
    png = res.find('img', id='target')['src']
    i_d = png.replace('//im7.ezgif.com/tmp/ezgif-7-', '').replace('.png', '')
    url = res.find('a', class_='m-btn-apng-to-gif active')['href']
    token = bs(r.get(url).text, 'html.parser').find('input', attrs={'name': 'token'})['value']
    gif = bs(r.post('https://s7.ezgif.com/apng-to-gif/ezgif-7-'+i_d+'.png?ajax=true', data={'file': 'ezgif-7-'+i_d+'.png', 'token': token}).text, 'html.parser')
    gif_file = gif.find('img')['src']
    result = 'https:'+gif_file
    return result

def convert_and_save(b64_string):
    with open("img/remove_bg.png", "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_pdf(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_PDF
def file_tts():
    file_ = 'tts/'+id_generator()+'.mp3'
    return file_

def ig_header():
    result = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "id,en-US;q=0.7,en;q=0.3",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "mid=YF7sjAALAAF-MqtkhOPIopCo5kNU; ig_did=1D303523-9F83-4CF9-8E13-1433BD0F9352; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; csrftoken=G5Bq0h0W3rSWhjV9bnADx8hJIRlfkp3h; ds_user_id=44449831791; sessionid=44449831791%3AUWaB4y4KQW9O6G%3A12; shbid=2573; shbts=1621268761.4835796; rur=NAO",
        "Host": "www.instagram.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    return result

def add_total_hit():
    try:
        load = json.load(open('static/hit.json'))
        write = open('static/hit.json', 'w')
        load['total'] +=1
        json.dump(load, write)
    except Exception as e:
        print(e)

@app.after_request
def log_the_status_code(response):
    status_as_integer = response.status_code
    rule = request.url_rule
    if '/api/' in rule.rule:
        if response.status_code == 200:
            try:
                add_total_hit()
            except Exception:
                pass

    return response

@app.route('/api/spamcall', methods=['GET','POST'])
def spamcall():
    if request.args.get('no'):
        no = request.args.get('no')
        if str(no).startswith('8'):
            hasil = ''
            kyaa = post('https://id.jagreward.com/member/verify-mobile/%s' % no).json()
            print(kyaa['message'])
            if 'Anda akan menerima' in kyaa['message']:
                hasil += '[!] Berhasil mengirim spam call ke nomor : 62%s' % no
            else:
                hasil += '[!] Gagal mengirim spam call ke nomor : 62%s' % no
            return {
                'status': 200,
                'logs': hasil
            }
        else:
            return {
                'status': False,
                'msg': '[!] Tolong masukkan nomor dengan awalan 8'
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter no' 
        }
@app.route('/api/spamsms', methods=['GET','POST'])
def spamming():
    if request.args.get('no'):
        if request.args.get('jum'):
            no = request.args.get('no')
            jum = int(request.args.get('jum'))
            if jum > 20: return {
                'status': 200,
                'msg': '[!] Max 20 ganteng'
            }
            url = 'https://www.lpoint.co.id/app/member/ESYMBRJOTPSEND.do'
            head = {'UserAgent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1853) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'}
            data = {'pn': '',
                'bird': '',
                'webMbrId': '',
                'webPwd': '',
                'maFemDvC': '',
                'cellNo': no,
                'otpNo': '',
                'seq': '',
                'otpChk': 'N',
                'count': ''
            }
            hasil = ''
            for i in range(jum):
                kyaa = post(url, headers=head, data=data).text
                if 'error' in kyaa:
                    hasil += '[!] Gagal\n'
                else:
                    hasil += '[!] Sukses\n'
            return {
                'status': 200,
                'logs': hasil
            }
        else:
            return {
                'status': False,
                'msg': '[!] Masukkin parameter jum juga ganteng'
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter no'
        }

def wimki(url):
    data=h.bs('https://id.wikipedia.org/wiki/'+url)
    for gambar in data.findAll("div", class_="mw-parser-output"):
        listimg=["https:"+image.get("src") for image in gambar.findAll("img")]
        return listimg

@app.route('/api/wiki', methods=['GET','POST'])
def wikipedia():
    if request.args.get('q'):
        try:
            kya = request.args.get('q')
            cih = f'https://id.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={kya}'
            heuh = get(cih).json()
            heuh_ = heuh['query']['pages']
            hueh = re.findall(r'(\d+)', str(heuh_))
            result = heuh_[hueh[0]]['extract']
            return {
                'status': 200,
                'result': result,
                'img': wimki(kya)
            }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': '[❗] Yang anda cari tidak bisa saya temukan di wikipedia!'
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan param q'
        }

@app.route('/api/mediafire', methods=['GET','POST'])
def mediafire():
    if request.args.get('url'):
        try:
            link = request.args.get('url')
            data=h.bs(link)
            fname=data.find("div", class_="filename").text
            ft=data.find("div", class_="filetype")
            ftp=ft.findAll("span")[1]
            jir=data.find("ul", class_="details")
            lo=jir.find("li").span
            fls=jir.find("li").span.text
            up=jir.findAll("li")[1].span.text
            d=data.find("div", class_="DLExtraInfo-sectionDetails")
            desc=d.find("p").text
            for p in data.findAll("a", class_="input popsok"):
                l = p.get("href")
                return {
                    'status': 200,
                    'filename': fname,
                    'url': l,
                    'filesize': fls,
                    'uploaded': up,
                    'filetype':ftp.text.replace("(", "").replace(")", "").replace(" ", ""),
                    'desc': desc
                }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'Link yang anda kirim tidak valid!'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter url!'
        }
                

@app.route('/api/chord', methods=['GET','POST'])
def chord():
    if request.args.get('q'):
        try:
            q = request.args.get('q').replace(' ','+')
            id = get('http://app.chordindonesia.com/?json=get_search_results&exclude=date,modified,attachments,comment_count,comment_status,thumbnail,thumbnail_images,author,excerpt,content,categories,tags,comments,custom_fields&search=%s' % q).json()['posts'][0]['id']
            chord = get('http://app.chordindonesia.com/?json=get_post&id=%s' % id).json()
            result = html_text.parse_html(chord['post']['content']).text_content()
            return {
                'status': 200,
                'result': result
            }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': '[❗] Maaf chord yang anda cari tidak dapat saya temukan!'
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter q'
        }

@app.route('/api/dewabatch', methods=['GET','POST'])
def dewabatch():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            he=search_dewabatch(quote(q))
            dewabatch=cari(he)
            if he != '':
                return {
                    'status': 200,
                    'sinopsis': dewabatch['result'],
                    'thumb': dewabatch['cover'],
                    'result': dewabatch['info']
                }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'Anime %s Tidak di temukan!' % unquote(q)
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter q'
        }

@app.route('/api/komiku', methods=['GET','POST'])
def komiku():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            komi = search_komiku(q)
            if 'Tidak di temukan' not in komi:
                manga = scrap_komiku(komi)
                return {
                    'status': 200,
                    'info': manga['info'],
                    'genre': manga['genre'],
                    'sinopsis': manga['sinopsis'],
                    'thumb': manga['thumb'],
                    'link_dl': manga['dl_link']
                }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'Manga %s Tidak di temukan' % unquote(q)
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter q'
        }

@app.route('/api/kuso', methods=['GET','POST'])
def kusonime():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            he=search_kusonime(quote(q))
            kuso=scrap_kusonime(he)
            if he != '':
                return {
                    'status': 200,
                    'sinopsis': kuso['sinopsis'],
                    'thumb': kuso['thumb'],
                    'info': kuso['info'],
                    'title': kuso['title'],
                    'link_dl': kuso['link_dl']
                }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'Anime %s Tidak di temukan' % unquote(q)
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter q'
        }

@app.route('/api/otakudesu')
def otakudesuu():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            he=search_otakudesu(quote(q))
            if he != '':
                otaku=scrap_otakudesu(he)
                return {
                    'status': 200,
                    'sinopsis': otaku['sinopsis'],
                    'thumb': otaku['thumb'],
                    'info': otaku['info'],
                    'title': otaku['title']
                }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'Anime %s Tidak di temukan' % unquote(q)
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter q'
        }
            
@app.route('/api/nekonime', methods=['GET','POST'])
def nekonimek():
    try:
        neko = get('https://waifu.pics/api/sfw/neko').json()
        nimek = neko['url']
        return {
            'status': 200,
            'result': nimek
        }
    except:
        neko = get('https://waifu.pics/api/sfw/neko').json()
        nimek = neko['url']
        return {
            'status': 200,
            'result': nimek
        }

@app.route('/api/randomloli', methods=['GET','POST'])
def randomloli():
    be = bs(get('https://wallpapercave.com/hd-anime-loli-wallpapers').text, 'html.parser')
    url = random.choice([link['src'] for link in be.findAll('img', class_='wpimg')])
    print(url)
    r = requests.get('https://wallpapercave.com'+url)
    with open('img/loli.jpg', 'wb') as f:
        f.write(r.content)
    return send_file('img/loli.jpg')
    
@app.route('/api/ig', methods=['GET','POST'])
def igeh():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            data = {'id': url}
            result = get('https://www.villahollanda.com/api.php?url=' + url).json()
            if result['descriptionc'] == None:
                return {
                    'status': False,
                    'result': 'https://c4.wallpaperflare.com/wallpaper/976/117/318/anime-girls-404-not-found-glowing-eyes-girls-frontline-wallpaper-preview.jpg',
                }
            else:
                return {
                    'status': 200,
                    'result': result['descriptionc'],
                }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'result': 'https://c4.wallpaperflare.com/wallpaper/976/117/318/anime-girls-404-not-found-glowing-eyes-girls-frontline-wallpaper-preview.jpg',
                'error': True
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter url'
        }

@app.route('/api/stalk', methods=['GET','POST'])
def stalk():
    if request.args.get('username'):
        try:
            username = request.args.get('username').replace('@','')
            url = 'https://www.instagram.com/'+username+'/?__a=1'
            header = ig_header()
            res = requests.get(url, headers=header).json()
            user = res['graphql']['user']
            bio = user['biography']
            external_url = user['external_url']
            followers = user['edge_followed_by']['count']
            following = user['edge_follow']['count']
            name = user['full_name']
            category_name = user['category_name']
            is_private = user['is_private']
            is_verified = user['is_verified']
            profile_pic = user['profile_pic_url_hd']
            result = dict(
                username = username,
                biography= bio,
                external_url = external_url,
                followers = followers,
                following = following,
                name = name,
                category_name = category_name,
                is_private = is_private,
                is_verified = is_verified,
                profile_pic = profile_pic
                )

            return result
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': '[❗] Username salah!'
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter username'
        }

@app.route('/daerah', methods=['GET','POST'])
def daerah():
    daerah = 'Andreas, Ambon, Amlapura, Alford, Argamakmur, Atambua, Babo, Bagan Siapiapi, Central Kalimantan, Birmingham, Samosir, Balikpapan, Banda Aceh, Bandar Lampung, Bandung, Bangkalan, Cianjur, Bangko, Bangli, Banjar, Banjar Baru, Banjarmasin, Corn, BANTAENG , Banten, Bantul, Banyuwangi, Barabai, Barito, Barru, Batam, Batang, Batu, Baturaja, Batusangkar, Baubau, Bekasi, Bengkalis, Bengkulu, Benteng, Biak, Bima, Binjai, Bireuen, Bitung, Blitar, Blora, Bogor, Bojonegoro , Bondowoso, Bontang, Boyolali, Brebes, Bukit Tinggi, Maluku, Bulukumba, Buntok, Cepu, Ciamis, Cianjur, Cibinong, Cilacap, Cilegon, Cimahi, Cirebon, Curup, Demak, Denpasar, Depok, Dili, Dompu, Donggala, Dumai, Ende, Enggano, Enrekang, Fakfak, Garut, Gianyar, Gombong, Gorontalo, Gresik, Gunung Sitoli, Indramayu, Jakarta Barat, Jakarta Pusat, Jakarta Selatan, Jakarta Timur, Jakarta Utara, Jambi,Jayapura, Jember, Jeneponto, Jepara, Jombang, Kabanjahe, Kalabahi, Kalianda, Kandangan, Karanganyar, Karawang, Kasungan, Kayuagung, Kebumen, Kediri, Kefamenanu, Kendal, Kendari, Kertosono, Ketapang, Kisaran, Klaten, Kolaka, Kota Baru Pulau Laut , Bumi Bumi, Kota Jantho, Kotamobagu, Kuala Kapuas, Kuala Kurun, Kuala Pembuang, Kuala Tungkal, Kudus, Kuningan, Kupang, Kutacane, Kutoarjo, Labuhan, Lahat, Lamongan, Langsa, Larantuka, Lawang, Lhoseumawe, Limboto, Lubuk Basung, Lubuk Linggau, Lubuk Pakam, Lubuk Sikaping, Lumajang, Luwuk, Madiun, Magelang, Magetan, Majalengka, Majene, Makale, Makassar, Malang, Mamuju, Manna, Manokwari, Marabahan, Maros, Martapura Kalsel, Sulsel, Masohi, Mataram, Maumere, Medan, Mempawah, Menado, Mentok, Merauke, Metro, Meulaboh, Mojokerto, Muara Bulian, Muara Bungo, Muara Enim, Muara Teweh, Muaro Sijunjung, Muntilan, Nabire,Negara, Nganjuk, Ngawi, Nunukan, Pacitan, Padang, Padang Panjang, Padang Sidempuan, Pagaralam, Painan, Palangkaraya, Palembang, Palopo, Palu, Pamekasan, Pandeglang, Pangka_, Pangkajene Sidenreng, Pangkalan Bun, Pangkalpinang, Panyabungan, Par_, Parepare, Pariaman, Pasuruan, Pati, Payakumbuh, Pekalongan, Pekan Baru, Pemalang, Pematangsiantar, Pendopo, Pinrang, Pleihari, Polewali, Pondok Gede, Ponorogo, Pontianak, Poso, Prabumulih, Praya, Probolinggo, Purbalingga, Purukcahu, Purwakarta, Purwodadigrobogan, Purwarta Purworejo, Putussibau, Raha, Rangkasbitung, Rantau, Rantauprapat, Rantepao, Rembang, Rengat, Ruteng, Sabang, Salatiga, Samarinda, Kalbar, Sampang, Sampit, Sanggau, Sawahlunto, Sekayu, Selong, Semarang, Sengkang, Serang, Serui, Sibolga, Sidikalang, Sidoarjo, Sigli, Singaparna, Singaraja, Singkawang, Sinjai, Sintang, Situbondo, Slawi,Sleman, Soasiu, Soe, Solo, Solok, Soreang, Sorong, Sragen, Stabat, Subang, Sukabumi, Sukoharjo, Sumbawa Besar, Sumedang, Sumenep, Sungai Liat, Sungai Penuh, Sungguminasa, Surabaya, Surakarta, Tabanan, Tahuna, Takalar, Takengon , Tamiang Layang, Tanah Grogot, Tangerang, Tanjung Balai, Tanjung Enim, Tanjung Pandan, Tanjung Pinang, Tanjung Redep, Tanjung Selor, Tapak Tuan, Tarakan, Tarutung, Tasikmalaya, Tebing Tinggi, Tegal, Temanggung, Tembilahan, Tenggarong, Ternate, Tolitoli , Tondano, Trenggalek, Tual, Tuban, Tulung Agung, Ujung Berung, Ungaran, Waikabubak, Waingapu, Wamena, Watampone, Watansoppeng, Wates, Wonogiri, Wonosari, Wonosobo, YogyakartaTakalar, Takengon, Tamiang Layang, Tanah Grogot, Tangerang, Tanjung Balai, Tanjung Enim, Tanjung Pandan, Tanjung Pinang, Tanjung Redep, Tanjung Selor, Tapak Tuan, Tarakan, Tarutung, Tasikmalaya, Tebing Tinggi, Tegal, Temanggung, Tembilahan, Tenggarong, Ternate, Tolitoli, Tondano, Trenggalek, Tual, Tuban, Tulung Agung, Ujung Berung, Ungaran, Waikabubak, Waingapu, Wamena, Watampone, Watansoppeng, Wates, Wonogiri, Wonosari, Wonosobo, YogyakartaTakalar, Takengon, Tamiang Layang, Tanah Grogot, Tangerang, Tanjung Balai, Tanjung Enim, Tanjung Pandan, Tanjung Pinang, Tanjung Redep, Tanjung Selor, Tapak Tuan, Tarakan, Tarutung, Tasikmalaya, Tebing Tinggi, Tegal, Temanggung, Tembilahan, Tenggarong, Ternate, Tolitoli, Tondano, Trenggalek, Tual, Tuban, Tulung Agung, Ujung Berung, Ungaran, Waikabubak, Waingapu, Wamena, Watampone, Watansoppeng, Wates, Wonogiri, Wonosari, Wonosobo, YogyakartaWonogiri, Wonosari, Wonosobo, YogyakartaWonogiri, Wonosari, Wonosobo, Yogyakarta'
    no = 1
    hasil = ''
    for i in daerah.split(','):
        hasil += '%s. %s\n' % (no, i)
        no += 1
    return {
        'status': 200,
        'result': hasil
    }

@app.route('/api/waifu', methods=['GET','POST'])
def waifu():
    scrap = bs(get('https://mywaifulist.moe/random').text, 'html.parser')
    a = json.loads(scrap.find('script', attrs={'type':'application/ld+json'}).string)
    desc = bs(get(a['url']).text, 'html.parser').find('meta', attrs={'property':'og:description'}).attrs['content']
    result = json.loads(bs(get(a['url']).text, 'html.parser').find('script', attrs={'type':'application/ld+json'}).string)
    if result['gender'] == 'female':
        return {
            'status': 200,
            'name': result['name'],
            'desc': desc,
            'image': result['image'],
            'source': result['url']
        }
    else:
        return {
            'status': 200,
            'name': '%s (husbu)' % result['name'],
            'desc': desc,
            'image': result['image'],
            'source': result['url']
        }

@app.route('/api/infogempa', methods=['GET','POST'])
def infogempa():
    be = bs(get('https://www.bmkg.go.id/').text, 'html.parser').find('div', class_="col-md-4 md-margin-bottom-10")
    em = be.findAll('li')
    img = be.find('a')['href']
    return {
        'status': 200,
        'map': img,
        'waktu': em[0].text,
        'magnitude': em[1].text,
        'kedalaman': em[2].text,
        'koordinat': em[3].text,
        'lokasi': em[4].text,
        'potensi': em[5].text
    }

@app.route('/api/renungan', methods=['GET','POST'])
def renungan():
    al = bs(get('https://alkitab.mobi/renungan/rh/').text, 'html.parser').find('body')
    res = al.findAll('p')
    res2 = al.findAll('div')
    return {
        'status': 200,
        'judul': res[3].text,
        'Isi': res2[4].text,
        'pesan': res[7].text.replace('*', '')
    }

@app.route('/api/blackpink', methods=['GET','POST'])
def blackpink():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            r = cloudscraper.create_scraper()
            url = 'https://textpro.me/create-blackpink-logo-style-online-1001.html'
            be = bs(r.get(url).text, 'html.parser')
            token = be.find('input', id='token')['value']
            build_server = be.find('input', attrs={'name': 'build_server'})['value']
            build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
            data = {'text[]': text, 'submit': 'Go', 'token': token}
            bes = bs(r.post(url, data).text, 'html.parser')
            fv = bes.find('div', id='form_value').text
            js = json.loads(fv)
            res = r.post('https://textpro.me/effect/create-image', data={'id': '1001', 'text[]': text, 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
            result = 'https://textpro.me'+res['image']
            req = r.get(result)
            with open('img/blackpink.jpg', 'wb') as f:
                f.write(req.content)
            crop.crop4('', 'blackpink')
            return send_file('img/blackpink.jpg')
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'error': '[❗] Terjadi kesalahan'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter text'
        }

@app.route('/api/tiktok_nowm', methods=['GET','POST'])
def tiktok_nowm():
    if request.args.get('url'):
        try:
            video_url = request.args.get('url')
            s = requests.Session()
            get_post = bs(s.get(
                url='https://ssstik.io/',
            ).text, 'html.parser').find('form', class_='pure-form pure-g hide-after-request')['data-hx-post']
            base = bs(s.post(
                url=f'https://ssstik.io{get_post}',
                headers={'HX-Current-URL': 'https://ssstik.io/', 'Host': 'ssstik.io', 'Origin': 'https://ssstik.io', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'},
                data={'id': video_url, 'locale': 'en', 'tt': '0', 'ts': '0'}
            ).text, 'html.parser')
            from_ = base.find('img')['alt']
            caption = base.find('p', class_='maintext').text
            s1 = 'https://ssstik.io'+base.find('a', class_='pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark snaptik')['href']
            s2 = base.find('a', class_='pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark_direct snaptik')['href']
            return{
                "from": from_,
                "caption": caption,
                "download":{"server1": s1, "server2": s2}
            }
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'error': '[❗] Terjadi kesalahan'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter url'
        }	

@app.route('/api/tiktokpp', methods=['GET','POST'])
def tiktokpp():
    if request.args.get('user'):
        try:
            user = request.args.get('user')
            data=h.bs('https://www.tiktok.com/@'+ user)
            p=data.find('div', class_="share-info")
            img=p.find("img")
            imeg=img.get("src")
            return {
                'status': 200,
                'result': imeg
            }
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'error': '[❗] Terjadi kesalahan'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter user!'
        }

@app.route('/api/samehadaku', methods=['GET','POST'])
def samehadaku():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            smhdk = bs(get('https://samehadaku.vip/?s='+ q, headers={'User-Agent':'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36'}).text, 'html.parser').find('div', class_='animepost')
            smhdk_ = smhdk.findAll('h2')
            thumb = smhdk.find('img')['src']
            link = smhdk.find('a')['href']
            smhdk2 = bs(get(link, headers={'User-Agent':'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36'}).text, 'html.parser')
            desc = smhdk2.find('div', class_='desc')
            det = smhdk2.find('div', class_='spe')
            return {
                'status': 200,
                'title': smhdk_[0].text,
                'thumb': thumb,
                'link': link,
                'desc': desc.text
            }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'tidak dapat di temukan di samehadaku!'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter q'
        }

@app.route('/api/samehadaku2', methods=['GET','POST'])
def samehadaku2():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            smhdk = bs(get(url, headers={'User-Agent':'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36'}).text, 'html.parser').find('div', class_='post-body')
            smhdk_ = smhdk.findAll('h1')
            desc = smhdk.findAll('p')
            thumb = smhdk.find('img')['src']
            genre = smhdk.findAll('a')
            bjir = smhdk.find('div', class_='spe')
            det = bjir.findAll('span')
            return {
                'status': 200,
                'title': smhdk_[0].text,
                'desc': desc[0].text,
                'thumb': thumb,
                'genre': genre[0].text
            }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'Link yang anda kirim mungkin tidak valid!!'
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter url'
        }

@app.route('/api/alkitab', methods=['GET','POST'])
def alkitab():
    r = cloudscraper.create_scraper()
    dataz=bs(r.get('https://www.bible.com/id/verse-of-the-day').text,'html5lib')
    image = dataz.find("meta",{"property":"og:image"})["content"]
    link=dataz.find("meta", {"property":"og:url"})["content"]
    baca = dataz.find('div', class_="verse-wrapper ml1 mr1 mt4 mb4")
    tesk = baca.findAll('p')
    return {
        'result':{
            'isi': tesk[0].text,
            'ayat': tesk[1].text,
            'link': link,
            'img': image
        }
    }

@app.route('/api/waifu2', methods=['GET','POST'])
def waifu2():
    be = bs(get('http://randomwaifu.altervista.org/').text, 'html.parser')
    wfu = be.find('div', class_="imgbox")
    url = wfu.find('img')['src']
    res = 'http://randomwaifu.altervista.org/'+url
    return {
        'img': res
    }

@app.route('/api/text3d', methods=['GET','POST'])
def text3d():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            r = cloudscraper.create_scraper()
            url = 'https://ephoto360.com/tao-hieu-ung-chu-3d-gradient-tuyet-dep-online-702.html'
            be = bs(r.get(url).text, 'html.parser')
            token = be.find('input', attrs={'name': 'token'})['value']
            #radio = random.choice(['05acf523-6deb-4b9d-bb28-abc4354d0858', '843a4fc2-059c-4283-87e4-c851c013073b', 'd951e4be-450e-4658-9e73-0f7c82c63ee3', 'a5b374f3-2f29-4da4-ae15-32dec01198e2'])
            build_server = be.find('input', attrs={'name': 'build_server'})['value']
            build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
            data = {'text[]': text, 'submit': 'Create a photo', 'token': token, 'build_server': build_server, 'build_server_id': build_server_id}
            bes = bs(r.post(url, data).text, 'html.parser')
            fv = bes.find('input', id='form_value_input')['value']
            js = json.loads(fv)
            res = r.post('https://ephoto360.com/effect/create-image', data={'id': '702', 'text[]': text, 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
            result = build_server+res['image']
            r = r.get(result)
            with open('img/text3d.jpg', 'wb') as f:
                f.write(r.content)
            crop.crop4('', 'text3d')
            return send_file('img/text3d.jpg')
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'error': '[❗] Terjadi kesalahan'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter text'
        }

@app.route('/api/ttlogo', methods=['GET','POST'])
def ttlogo():
    if request.args.get('text1'):
        if request.args.get('text2'):
            try:
                text1 = request.args.get('text1')
                text2 = request.args.get('text2')
                res = scr.glitch('', text1, text2)
                sc = cloudscraper.create_scraper()
                r = sc.get(res)
                with open('img/TiktokGlitch.jpg', 'wb') as f:
                    f.write(r.content)
                return send_file('img/TiktokGlitch.jpg')
            except Exception as e:
                print('Error : %s ' % e)
                return {
                    'status': False,
                    'result': '[❗] Terjadi kesalahan'
                    }
        else:
            return {
                'status': False,
                'result': 'Masukkan parameter text2!'
            }
    else:
        return {
            'status': False,
            'result': 'Masukkan parameter text1!'
        }

def randomFML():
    return {"fml":random.choice([fml.text.split(" FML")[0].replace("\n","") for fml in h.bs("https://www.fmylife.com/random").findAll("a",class_="article-link")])}


@app.route('/api/fml', methods=['GET','POST'])
def fml():
    return {
        'status': 200,
        'result': randomFML()
    }

def alkitabcari(q):
    scraper = cloudscraper.create_scraper()
    dataz,dataa=bs(scraper.get('https://www.bible.com/id/search/bible?q='+quote(q)).text, 'html.parser'),[]
    for wildan in dataz.findAll("li", {"class": "reference"}):
        ayat=wildan.a.text
        link="https://bible.com"+wildan.a.get("href")
        isi=wildan.p.text.replace("\n","")
        dataa.append({"ayat":ayat,"isi": isi, "link":link})
    return dataa

@app.route('/api/alkitabsearch', methods=['GET','POST'])
def alkitabsearch():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            res = alkitabcari(q)
            return {
                'status': 200,
                'result': res
            }
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'result': '[❗] Terjadi kesalahan'
            }
    else:
        return {
            'status': False,
            'result': 'Masukkan parameter q!'
        }

def getDataFilm():
    data,dataa=h.bs("http://filmindonesia.or.id/movie/viewer").tbody,[]
    for film in data.findAll("tr"):
        r=film.td.text
        filmm=film.a
        link,title=filmm.get("href"),filmm.text
        pen=film.findAll("td")[-1].text
        dataa.append({"rank":r,"title":title,"link":link,"penonton":pen})
    return dataa

@app.route('/api/mostviewfilm', methods=['GET','POST'])
def mostviewfilm():
    res = getDataFilm()
    return{
        'result': res
    }

channels=["antv","gtv","indosiar","inewstv","kompastv","mnctv","metrotv","nettv","rcti","sctv","rtv","trans7","transtv"]
jam=str(datetime.now().time()).split(":");jam="{}:{}".format(jam[0],jam[1])
def getJadwalTV(channel):
    if channel.lower() in channels:
        data,dataa=bs(get('https://www.jadwaltv.net/channel/'+channel, headers={'User-Agent':'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36'}).text, 'html.parser'),[]
        for jadwal in data.findAll("tr")[1:]:
            info=jadwal.findAll("td")
            dataa.append("{} - {}".format(info[0].text.replace("WIB"," WIB"),info[1].text.title()))
        return dataa
    else:h.pj({"error":"Channel yang dituju salah! Daftar Channel yang tersedia: "+", ".join([ch.upper() for ch in channels])})

def getJadwalTVNow():
    data,dataa=h.bs("https://www.jadwaltv.net/channel/acara-tv-nasional-saat-ini"),{"jam":jam,"jadwalTV":[]}
    for jadwal in data.findAll("tr")[1:]:
        info=" - ".join([x.text for x in jadwal.findAll("td")])
        dataa["jadwalTV"].append(info.replace("WIB"," WIB"))
    x="\n".join(dataa["jadwalTV"])
    dataa["jadwalTV"] = x
    return dataa

@app.route('/api/jadwaltv', methods=['GET','POST'])
def jadwaltv():
    if request.args.get('ch'):
        try:
            ch = request.args.get('ch').lower()
            res = getJadwalTV(ch)
            return {
                'result': res
            }
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'result': '[❗] Terjadi kesalahan'
            }
    else:
        return{
            'status': 'error',
            'result': 'Masukkan prameter q!'
        }

@app.route('/api/jadwaltvnow', methods=['GET','POST'])
def jadwaltvnow():
    res = getJadwalTVNow()
    return {
        'result': res
    }


urlkr="https://m.karir.com"
def loker():
    data,dataa=h.bs(urlkr+"/search").find("ul",class_="opportunities-list"),[]
    for ker in data.findAll("li",class_="opportunity opportunity-search-click"):
        perusahaan=ker.h3.text
        link=urlkr+ker.get("data-url")
        profesi=ker.h2.text.title()
        if profesi.endswith(" "):profesi=profesi[:-1]
        gaji=ker.find("span",class_="tdd-salary").text
        lokasi=ker.find("div",class_="tdd-location").text
        info=h.bs(link)
        infoo=info.findAll("div",class_="bm-opportunity-stat__value")
        pengalaman=infoo[2].text
        jobfunction=infoo[1].text
        levelkarir=infoo[3].text
        edukasi=infoo[4].text
        info2=info.findAll("section",class_="b-matte__content")
        desc=info2[0].text
        req=info2[1].text
        dataa.append({"perusahaan":perusahaan,"link":link,"profesi":profesi,"gaji":gaji,"lokasi":lokasi,"pengalaman":pengalaman,"jobFunction":jobfunction,"levelKarir":levelkarir,"edukasi":edukasi,"desc":desc,"syarat":req})
    return dataa

@app.route('/api/infoloker', methods=['GET','POST'])
def infoloker():
    res = loker()
    return{
        'result': res
    }

def catOfTheDay():
    data=h.bs("http://www.funnycatpix.com/")
    title=h.bs(data.base.get("href")+data.find("div",class_="catphoto").a.get("href")).title.text
    cat=data.base.get("href")+data.img.get("src")
    res = {"title":title,"image":cat}
    return res

def randomFunnyCatVideo():
    data,dataa=h.bs("http://www.catsvscancer.org/section/video/"),[]
    for vids in data.findAll("div",class_="video-btn-wrapper"):
        vid=h.bs(vids.a.get("href"))
        title=vid.h3.text[:-1]
        link=vid.iframe.get("src")
        if "facebook" in link:
            x=link.split("href=")[1].split("&show")[0]
            link=h.bs("https://www.videofk.com/facebook-video-download/search?url={}&select=facebook".format(x))
            link=link.findAll("a")[9].get("href")
        else:
            id=link.split("embed/")[1].split("?")[0]
            try:
                linkk=h.ytmp4(id)
            except:
                id=id[:-5].replace("//","")
                linkk=h.ytmp4(id)
            dataa.append({"title":title,"video":linkk})
            res = random.choice(dataa)
    return res

def hoaxes():
    data,dataa=h.bsverif("https://turnbackhoax.id"),[]
    for hoax in data.findAll("div",class_="mh-loop-content mh-clearfix"):
        link=hoax.a.get("href");image=h.bs(link).figure.img.get("src")
        title=hoax.a.text[6:][:-4]
        tag=title[1:].split("]")[0]
        title=title.split("] ")[1]
        if title == title.upper():title=title.title()
        dataa.append({"tag":tag,"title":title,"link":link,"image":image})
    return dataa

def getHoax(link):
    data,dataa=h.bsverif("https://turnbackhoax.id"),[]
    data=h.bsverif(link).find("div",class_="entry-content mh-clearfix")
    berita=data.text[5:][:-74]
    listimg=[image.get("src") for image in data.findAll("img")]
    return {
        "berita":berita,
        "listImage":listimg
    }

@app.route('/api/infohoax', methods=['GET','POST'])
def infohoax():
    return{
        'result': hoaxes()
    }

@app.route('/api/gethoax', methods=['GET','POST'])
def gethoaxs():
    if request.args.get('url'):
        try:
            q = request.args.get('url')
            return {
                'result': getHoax(q)
            }
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'result': '[❗] Terjadi kesalahan'
            }
    else:
        return{
            'status': 'error',
            'result': 'Masukkan prameter url!'
        }

@app.route('/api/catvid', methods=['GET','POST'])
def catvid():
    res = randomFunnyCatVideo()
    return {
        'res': res
    }

@app.route('/api/catOfTheDay', methods=['GET','POST'])
def catoptheday():
    res = catOfTheDay()
    return {
        'res': res
    }

urlcn="https://m.21cineplex.com/"
def cineplex(chc):
    dataa=[]
    if chc=="nowplaying":data=h.bs(urlcn)
    elif chc=="comingsoon":data=h.bs(urlcn+"gui.coming_soon.php")
    for film in data.findAll("div",class_="grid_movie"):
        link=urlcn+film.a.get("href")
        title=film.find("div",class_="title").text.title()
        dimensi=film.span.text
        try:rating=film.findAll("a")[1].text
        except:rating="-"
        data2=h.bs(link)
        genre=data2.findAll("div",class_="col-xs-8 col-sm-11 col-md-11")[1].text.replace('                                    ',"").replace('                                ','')
        if genre.endswith(" "):genre=genre[:-1]
        poster=data2.find("img",class_="img-responsive pull-left gap-left").get("src")
        trailer=data2.findAll("button")[4].get("onclick").split("'")[1].split("'")[0]
        sinopsis=data2.find("p",{"id":"description"}).text
        info=data2.findAll("p")
        producer=info[7].text
        if producer.startswith(" "):producer=producer[1:]
        director=info[9].text
        writer=info[11].text
        casts=info[13].text
        distributor=info[15].text
        if len(info) == 17 and info[17].get("href") != "":
            linkmovie=info[17].get("href")
        else:linkmovie="-"
        dataa.append({"title":title,"distributor":distributor,"poster":poster,"genre":genre,"dimensi":dimensi,"rating":rating,"sinopsis":sinopsis,"producer":producer,"director":director,"writer":writer,"casts":casts,"sinopsis":sinopsis,"link":link,"linkmovie":linkmovie})
    return dataa

@app.route('/api/cineplex', methods=['GET','POST'])
def cinema21():
    return{
        'result': cineplex("comingsoon")
    }

daerahs=json.loads(open("lib/js.json","r").read())
def jadwalSholat(daerah):
    daerah=daerah.title()
    if daerah in daerahs.keys():
        data=[waktu.text for waktu in h.bs("https://www.jadwalsholat.org/adzan/monthly.php?id="+daerahs[daerah]).find("tr",class_="table_highlight").findAll("td")[1:]]
        imsyak,subuh,dhuha,dzuhur,ashar,maghrib,isya=data[0],data[1],data[2],data[3],data[4],data[5],data[6]
        return {"Imsyak":imsyak,"Subuh":subuh,"Dhuha":dhuha,"Dzuhur":dzuhur,"Ashar":ashar,"Maghrib":maghrib,"Isya":isya}
    else:
        h.pj({"error":"Daerah yang tersedia hanya: {}".format(", ".join(daerahs.keys()))})

@app.route('/api/jadwalshalat', methods=['GET','POST'])
def jadwalsholat():
    if request.args.get('daerah'):
        try:
            daer = request.args.get('daerah')
            res = jadwalSholat(daer)
            return jsonify(res)
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'result': '[❗] Terjadi kesalahan'
            }
    else:
        return{
            'status': 'error',
            'result': 'Masukkan prameter daerah!'
        }

def trendingtwt():
    dataz,dataa=h.bs('https://getdaytrends.com/indonesia/').tbody,[]
    for wildan in dataz.findAll("tr"):
        hastak=wildan.find("td", class_="main")
        hastag=hastak.a.text
        r=wildan.th.text
        twit=hastak.find("div", class_="desc")
        twits=twit.span.text
        link="https://twitter.com/search?q="+hastag
        dataa.append(
            {
                "hastag":hastag,
                "rank":r,
                "tweet":twits,
                "link":link
            }
            )
    return dataa

@app.route('/api/trendingtwitter', methods=['GET','POST'])
def tren():
    return {
        'result': trendingtwt()
    }

@app.route('/api/infonomor', methods=['GET','POST'])
def infonomor():
    if request.args.get('no'):
        try:
            nomore = request.args.get('no')
            dataz,dataa=h.bs('https://id.tellows.net/num/'+nomore).tbody,[]
            njir=dataz.findAll('tr')[4]
            op=njir.findAll('td')[1].text
            q=dataz.findAll('tr')[5]
            no=q.findAll('td')[1].text.replace(" ", "").replace("\n", "").replace("\t", "")
            b=dataz.findAll('tr')[6]
            itl=b.findAll('td')[1].text.replace(" ", "").replace("\n", "")
            return {
                'nomor': no,
                'op': op,
                'international': itl
            }
        except Exception as e:
            print(e)
            return{
                'status': False,
                'result': 'Nomor yang kamu kirim tidak valid!'
            }
    else:
        return{
            'result': 'Masukkkan parameter no!'
        }

def neonime():
    data,dataa=h.bs("https://neonime.vip/episode/").tbody,[]
    for film in data.findAll("tr"):
        jdl=film.find('td', class_="bb")
        judul=jdl.a.text
        lnk=jdl.a
        link=lnk.get("href")
        gbr=film.td
        gbr2=gbr.find('div', class_="imagen-td")
        p=gbr2.img
        img=p.get("data-src")
        tgl=film.find('td', class_='dd').text
        dataa.append({
            'judul': judul,
            'link': link,
            'img': img,
            'rilis':tgl
        }
        )
    return dataa

@app.route('/api/neonime_lastest', methods=['GET','POST'])
def neonimelast():
    return{
        'result': neonime()
    }

@app.route('/api/thunder', methods=['GET','POST'])
def thunder():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            r = cloudscraper.create_scraper()
            url = 'https://textpro.me/thunder-text-effect-online-881.html'
            be = bs(r.get(url).text, 'html.parser')
            token = be.find('input', id='token')['value']
            build_server = be.find('input', attrs={'name': 'build_server'})['value']
            build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
            data = {'text[]': text, 'submit': 'Go', 'token': token}
            bes = bs(r.post(url, data).text, 'html.parser')
            fv = bes.find('div', id='form_value').text
            js = json.loads(fv)
            res = r.post('https://textpro.me/effect/create-image', data={'id': '881', 'text[]': text, 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
            result = 'https://textpro.me'+res['image']
            req = r.get(result)
            with open('img/thunder.jpg', 'wb') as f:
                f.write(req.content)
            crop.crop2('', 'thunder')
            return send_file('img/thunder.jpg')
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'error': '[❗] Terjadi kesalahan'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter text'
        }

def randomKataCinta():
    data,dataa=h.bs("https://jagokata.com/kata-bijak/kata-cinta.html"),[]
    for film in data.findAll("q", class_="fbquote"):
        kata=film.text
        dataa.append(kata)
    return dataa

@app.route('/api/katacinta', methods=['GET','POST'])
def ktacinta():
    kata=randomKataCinta()
    res=random.choice(kata)
    return {
        'result': res
    }

def randomTwichQuote():
    data,dataa=h.bs("https://www.twitchquotes.com/"),[]
    for film in data.findAll("span", class_="-main-text"):
        kata=film.text
        dataa.append(kata)
    return dataa

@app.route('/api/twichquote', methods=['GET','POST'])
def twichquotes():
    kata=randomTwichQuote()
    res=random.choice(kata)
    return {
        'result': res
    }

def pribahasa(q):
    data,dataa=h.bs('https://jagokata.com/peribahasa/'+q+'.html'),[]
    for film in data.findAll("ul", class_="peribahasa")[0:]:
        kata=film.li.text
        dataa.append(kata)
    return dataa

@app.route('/api/pribahasa', methods=['GET','POST'])
def prbahasa():
    if request.args.get('q'):
        kata=request.args.get('q').replace(" ", "+")
        res=pribahasa(kata)
        return{
            'result': res
        }
    else:
        return{
            'result': 'masukkan parameter q!'
        }

def getComicWebtoon(linkepisode):
    webtun,comics=h.bs(linkepisode),{"size":0,"c":[]},1,0
    images=webtun.find("div",{"id":"_imageList"})
    for comic in images.findAll("img"):
        image=comic.get("data-url").replace("webtoo","swebtoo")
        comics["c"].append(
            {
                'img': image
            })
    return comics

@app.route('/api/webtoon', methods=['GET','POST'])
def weptun():
    if request.args.get('url'):
        url = request.args.get('url')
        return{
            'result': getComicWebtoon(url)
        }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/randomquotes', methods=['GET','POST'])
def quotes():
    quotes_file = json.loads(open('quotes.json').read())
    result = random.choice(quotes_file)
    print(result)
    return {
        'status': 200,
        'author': result['author'],
        'quotes': result['quotes']
    }

@app.route('/api/wolf', methods=['GET','POST'])
def wolf():
    if request.args.get('text1'):
        if request.args.get('text2'):
            try:
                text1 = request.args.get('text1')
                text2 = request.args.get('text2')
                res = scr.wolf('', text1, text2)
                r = requests.get(res)
                with open('img/wolf.jpg', 'wb') as f:
                    f.write(r.content)
                return send_file('img/wolf.jpg')
            except Exception as e:
                print('Error : %s ' % e)
                return {
                    'status': False,
                    'result': '[❗] Terjadi kesalahan'
                    }
        else:
            return {
                'status': False,
                'result': 'Masukkan parameter text2!'
            }
    else:
        return {
            'status': False,
            'result': 'Masukkan parameter text1!'
        }
@app.route('/api/ytdl', methods=['GET','POST'])
def ytdl():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            ytdlr = scr.ytdl('', url)
            return ytdlr
        except Exception as e:
            return{
                'result': 'Terjadi kesalahan'
            }
    else:
        return {
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/ytmp3', methods=['GET','POST'])
def ytmp3():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
            match = regex.match(url)
            id = match.group('id')
            r = bs(get('http://vid-loader.com/file/mp3/'+id).text, 'html.parser')
            title = r.find('h2', class_='text-lg text-teal-600 font-bold m-2 text-center')
            filesize = r.findAll('div', class_='text-shadow-1')[14]
            f = r.findAll('a', class_='shadow-xl bg-blue-600 text-white hover:text-gray-300 focus:text-gray-300 focus:outline-none rounded-md p-2 border-solid border-2 border-black ml-2 mb-2 w-25')
            dl = f[3]['href']
            return {
                'title': title.text,
                'thumb': 'https://i.ytimg.com/vi/'+id+'/hqdefault.jpg',
                'filesize': filesize.text,
                'result': shortener(dl)
            }
        except Exception as e:
            print(e)
            return{
                'result':'Terjadi kesalahan'
            }
    else:
        return{
            'result':'Masukkan parameter url'
        }

@app.route('/api/ytmp4', methods=['GET','POST'])
def ytmp4():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
            match = regex.match(url)
            id = match.group('id')
            r = bs(get('http://vid-loader.com/file/mp4/'+id).text, 'html.parser')
            title = r.find('h2', class_='text-lg text-teal-600 font-bold m-2 text-center')
            filesize = r.findAll('div', class_='text-shadow-1')[2]
            f = r.find('a', class_='shadow-xl bg-blue-600 text-white hover:text-gray-300 focus:text-gray-300 focus:outline-none rounded-md p-2 border-solid border-2 border-black ml-2 mb-2 w-25')
            dl = f['href']
            return {
                'title': title.text,
                'thumb': 'https://i.ytimg.com/vi/'+id+'/hqdefault.jpg',
                'filesize': filesize.text,
                'result': shortener(dl)
            }
        except Exception as e:
            print(e)
            return{
                'result':'Terjadi kesalahan'
            }
    else:
        return{
            'result':'Masukkan parameter url'
        }

@app.route('/api/neon_light', methods=['GET','POST'])
def neon_light():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            r = cloudscraper.create_scraper()
            url = 'https://ephoto360.com/hieu-ung-chu-anh-sang-theo-phong-cach-cong-nghe-tuong-lai-769.html'
            be = bs(r.get(url).text, 'html.parser')
            token = be.find('input', attrs={'name': 'token'})['value']
            radio = random.choice(['05acf523-6deb-4b9d-bb28-abc4354d0858', '843a4fc2-059c-4283-87e4-c851c013073b', 'd951e4be-450e-4658-9e73-0f7c82c63ee3', 'a5b374f3-2f29-4da4-ae15-32dec01198e2'])
            build_server = be.find('input', attrs={'name': 'build_server'})['value']
            build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
            data = {'radio0[radio]': radio, 'text[]': text, 'submit': 'Create a photo', 'token': token, 'build_server': build_server, 'build_server_id': build_server_id}
            bes = bs(r.post(url, data).text, 'html.parser')
            fv = bes.find('input', id='form_value_input')['value']
            js = json.loads(fv)
            res = r.post('https://ephoto360.com/effect/create-image', data={'id': '769', 'radio0[radio]': radio, 'text[]': text, 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
            result = build_server+res['image']
            r = r.get(result)
            with open('img/neon-light.jpg', 'wb') as f:
                f.write(r.content)
            crop.crop6('', 'neon-light')
            return send_file('img/neon-light.jpg')
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'error': '[❗] Terjadi kesalahan'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter text'
        }

@app.route('/api/tiktok_wm', methods=['GET','POST'])
def tiktok_wm():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            s = requests.Session()
            base = bs(s.get(
                url='https://ttdownloader.com/',
                ).text, 'html.parser')

            token = base.find('input', id='token')['value']
            ajax = bs(s.post(
                url='https://ttdownloader.com/ajax/',
                headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
                },
                data=dict(
                    url=url,
                    format="",
                    token=token)
                ).text, 'html.parser')
            result = ajax.find('a', class_='download-link')['href']
            return {'result': result}
        except Exception as e:
            print(e)
            return {
                'result': 'Terjadi kesalahan'
            }
    else:
        return {
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/yt-play', methods=['GET','POST'])
def yt_play():
    from youtubesearchpython import VideosSearch
    from hurry.filesize import size
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            det = VideosSearch(q, limit = 1).result()
            id = det['result'][0]['id']
            up = det['result'][0]['publishedTime']
            dur = det['result'][0]['duration']
            view = det['result'][0]['viewCount']['text']
            ch = det['result'][0]['channel']['name']
            link = 'https://www.youtube.com/watch?v='+id
            yta = post('https://www.y2mate.com/mates/en60/analyze/ajax',data={'url':link,'q_auto':'0','ajax':'1'}).json()
            yaha = bs(yta['result'], 'html.parser').findAll('td')
            thumb = bs(yta['result'], 'html.parser').find('img')['src']
            title = bs(yta['result'], 'html.parser').find('b').text
            p = requests.post('https://yt1s.com/api/ajaxSearch/index', data={'q': link, 'vt': 'mp3'}).json()
            k = p['kc']
            i_d = p['vid']
            p = bs(requests.get('http://vid-loader.com/file/mp3/'+id).text, 'html.parser')
            inf = p.findAll('a', class_='shadow-xl bg-blue-600 text-white hover:text-gray-300 focus:text-gray-300 focus:outline-none rounded-md p-2 border-solid border-2 border-black ml-2 mb-2 w-25')
            q = inf[3]
            dl = q['href']
            filesize = p.findAll('div', class_='text-shadow-1')[11]
            return {
                'title': title,
                'thumb': thumb,
                'uploaded': up,
                'duration': dur,
                'total_view': view,
                'channel': ch,
                'filesize': filesize.text,
                'link': dl
            }
        except Exception as e:
            print(e)
            return{
                'status': False,
                'result': q+' '+'Tidak di temukan'
            }
    else:
        return {
            'result' :'masukkan parameter q'
        }

def husbandofriday():
    data,dataa=h.bsverif("http://jurnalotaku.com/tag/husbando-friday/",True),[]
    for info in data.findAll("div",class_="article-wrapper article-tb m-tb"):
        link=info.a.get("href")
        image=info.img.get("src")
        waifu=info.img.get("alt").split("[Husbando Friday] ")[1]
        #reason=Helper.bsoup(link,True).find("div",class_="meta-content").h2.text.split("+ ")[1]
        dataa.append({"waifu":waifu,"image":image})
    result=random.choice(dataa)
    return result

@app.route('/api/husbuando', methods=['GET','POST'])
def husbuando():
    return husbandofriday()

@app.route('/api/fake_identity', methods=['GET','POST'])
def fake_identity():
    try:
        res = scr.fake_iden('')
        return res
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan!'
        }

@app.route('/api/screed', methods=['GET','POST'])
def screed():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            p = bs(post('http://wigflip.com/screedbot/', data={'text': text}).text, 'html.parser').find('p')
            res = p.find('img')['src']
            r = get(res)
            with open('img/screed.gif', 'wb') as f:
                f.write(r.content)
            return send_file('img/screed.gif')
        except Exception as e:
            print(e)
            return {
                'result': 'Terjadi kesalahan'
            }
    else:
        return{
            'result': 'Masukkan paramater text!'
        }
    
@app.route('/api/alkitab_songs', methods=['GET','POST'])
def alkitab_songs():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            p = bs(get('https://alkitab.app/songs/search?q='+q).content, 'html.parser').find('div', class_='judul-lagu-hasil')
            url = 'https://alkitab.app'+p.find('a')['href']
            bes = bs(get(url).content, 'html.parser')
            judul = bes.find('div', class_='judul').text
            judul_asli = bes.find('div', class_='judul_asli').text
            nada_dasar = bes.find('div', class_='nadaDasar').text
            lirik = bes.find('div', class_='lirik').text
            audio = bes.find('audio')['src']
            return {
                'result':{
                    'judul': judul,
                    'judul_asli': judul_asli,
                    'nada_dasar': nada_dasar,
                    'audio': audio,
                    'lirik': lirik.replace('  ', '')
                }
            }
        except Exception as e:
            print(e)
            return {
                'result': q+' '+'tidak di temukan!'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/insta', methods=['GET','POST'])
def insta():
    if request.args.get('url'):
        if '/tv/' in request.args.get('url'):
            return{
                'result': 'Url tidak valid!'
            }
        elif re.match(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', request.args.get('url')):
            try:
                url = request.args.get('url')
                p = post('https://www.ins-porter.com/api/single_search', json={"keyword": url, "search_type": "post"}).json()
                res = p['results']
                return json.loads(res)
            except Exception as e:
                print(e)
                return{
                    'result': 'Url tidak valid!'
                }
        else:
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/insta_v2', methods=['GET','POST'])
def insta_v2():
    if request.args.get('username'):
        if '/tv/' in request.args.get('username'):
            return{
                'result': 'Username tidak valid!'
            }
        elif re.match(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', request.args.get('username')):
            return{
                'result': 'Username tidak valid!'
            }
        else:
            try:
                url = request.args.get('username')
                p = post('https://www.ins-porter.com/api/single_search', json={"keyword": url, "search_type": "post"}).json()
                res = p['results']
                return json.loads(res)
            except Exception as e:
                print(e)
                return{
                    'result': 'Username tidak valid!'
                }
    else:
        return{
            'result': 'Masukkan parameter username!'
        }

@app.route('/api/igtv', methods=['GET','POST'])
def igtv():
    if request.args.get('url'):
        if '/tv/' in request.args.get('url'):
            try:
                url = request.args.get('url')
                p = post('https://www.ins-porter.com/api/single_search', json={"keyword": url, "search_type": "post"}).json()
                res = p['results']
                return json.loads(res)
            except Exception as e:
                print(e)
                return{
                    'result': 'Url tidak valid!'
                }
        elif re.match(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', request.args.get('url')):
            return{
                'result': 'Url tidak valid!'
            }
        else:
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

from flask import jsonify

@app.route('/api/igstory', methods=['GET','POST'])
def igstory():
    if request.args.get('username'):
        try:
            bes = bs(get('https://pastebin.com/v7JikhK8').text, 'html.parser')
            kuki = bes.find('textarea', class_='textarea').text
            head = {'cookie': kuki}
            user = get('https://www.instagram.com/'+request.args.get('username')+'/?__a=1', headers=head).text
            js = json.loads(user)
            i_d = js['graphql']['user']['id']
            r = get(f'https://www.instagram.com/graphql/query/?query_hash=de8017ee0a7c9c45ec4260733d81ea31&variables=%7B%22reel_ids%22%3A%5B%22'+i_d+f'%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22%22%7D', headers=head).text
            res = json.loads(r)
            result = []
            for i in res['data']['reels_media'][0]['items']:
                if (i['is_video'] == True):
                    media = 'video_resources'
                else:
                    media = 'display_resources'
                if (media == 'video_resources'):
                    typ = 'video'
                else:
                    typ = 'image'
                url = i[media][0]['src']
                uploaded = datetime.utcfromtimestamp(int(i['taken_at_timestamp'])).strftime(f'%Y-%m-%d %H:%M:%S')
                expired = datetime.utcfromtimestamp(int(i['expiring_at_timestamp'])).strftime(f'%Y-%m-%d %H:%M:%S')
                filesize = requests.head(url).headers
                result.append(
                    {
                        'url': url,
                        'uploaded': uploaded,
                        'expired': expired,
                        'filesize': size(int(filesize['Content-Length']))+'B',
                        'type': typ
                    }
                )
            return jsonify({
                'count': len(result),
                'from': request.args.get('username'),
                'result': result
            }) 
        except Exception as e:
            print(e)
            return{
                'result': 'Username tidak valid/Story tidak tersedia'
            }
    else:
        return{
            'result': 'Masukkan parameter username!'
        }

@app.route('/api/ighighlight', methods=['GET','POST'])
def ighighlight():
    if request.args.get('username'):
        try:
            username = request.args.get('username')
            r = requests.Session()
            token = bs(r.get('https://instagrilz.com/en/download-highlights/').text, 'html.parser').find('input', id='token')['value']
            res = r.post('https://instagrilz.com/ajax/action/', data={'url': 'https://instagram.com/'+username, 'action': 'highlights', 'token': token, 'locale': 'en'}).text
            js = json.loads(res)
            result = []
            for i in js['medias']:
                result.append(i)
            return jsonify({
                'username': js['user']['username'],
                'full_name': js['user']['fullName'],
                'bio': js['user']['biography'],
                'result': result
            })
        except Exception as e:
            print(e)
            return{
                'result': 'Username tidak valid'
            }
    else:
        return{
            'result': 'Masukkan parameter username!'
        }

@app.route('/api/wattpad_search', methods=['GET','POST'])
def wattpad_search():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            res = scr.wattpad_search('', q)
            return {
                'result': res
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/wattpad_info', methods=['GET','POST'])
def wattpad_info():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            r = cloudscraper.create_scraper()
            bes = bs(r.get(url).text, 'html.parser')
            title = bes.find('h1').text
            th = bes.find('div', class_='cover cover-lg')
            thumb = th.find('img')['src']
            inf = bes.find('div', class_='meta')
            info = inf.findAll('span')
            a = bes.find('div', class_='author-info clearfix')
            parts = []
            table = bes.find('ul', class_='table-of-contents')
            for i in table.findAll('li'):
                link = i.find('a')['href']
                titles = i.find('a').text
                parts.append({
                    'title': " ".join(re.findall("[a-zA-Z]+", titles)),
                    'url': 'https://www.wattpad.com'+link
                })

            return jsonify({
                'title': title.replace('   ', ''),
                'reads': ''.join(filter(lambda i: i.isdigit(), info[0].text))+' Reads',
                'votes': ''.join(filter(lambda i: i.isdigit(), info[1].text))+' Votes',
                'parts_count': info[2].text,
                'desc': bes.find('h2', class_='description').text,
                'author':{
                    'url': 'https://www.wattpad.com'+a.find('a')['href'],
                    'name': a.find('a', class_='send-author-event on-navigate').text,
                    'pic': a.find('img')['src']
                },
                'thumb': thumb,
                'parts': parts
            })
        except Exception as e:
            print(e)
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/wattpad_parts', methods=['GET','POST'])
def wattpad_parts():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            r = cloudscraper.create_scraper()
            bes = bs(r.get(url).text, 'html.parser')
            #img = bes.find('div', class_='background-lg media background')
            #return{
            #    'banner': img.find('img')['src']
            #}
        except Exception as e:
            print(e)
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/ssweb', methods=['GET','POST'])
def ssweb():
    if request.args.get('url'):
        if request.args.get('device'):
            perangkat = request.args.get('device').lower()
            url = request.args.get('url')
            if perangkat == 'dekstop':
                device = 'dekstop'
            elif perangkat == 'tablet':
                device = 'tablet'
            elif perangkat == 'phone':
                device = 'phone'
            else:
                device = 'desktop'
            try:
                r = cloudscraper.create_scraper()
                form = {'url': url, 'device': device, 'cacheLimit': 0}
                res = r.post('https://www.screenshotmachine.com/capture.php', data=form).json()
                result = 'https://www.screenshotmachine.com/'+res['link']
                fl = r.get(result, data={'file':result.replace('serve.php?file=', '')})
                with open('img/ss.jpg', 'wb') as f:
                    f.write(fl.content)
                return send_file('img/ss.jpg')
            except Exception as e:
                print(e)
                return{
                    'result': 'Url tidak valid!'
                }
        else:
            return{
                'result': 'Masukkan parameter device!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/ssweb_full', methods=['GET','POST'])
def ssweb_full():
    if request.args.get('url'):
        if request.args.get('device'):
            perangkat = request.args.get('device').lower()
            url = request.args.get('url')
            if perangkat == 'dekstop':
                device = 'dekstop'
            elif perangkat == 'tablet':
                device = 'tablet'
            elif perangkat == 'phone':
                device = 'phone'
            else:
                device = 'desktop'
            try:
                r = cloudscraper.create_scraper()
                form = {'url': url, 'device': device, 'full': 'on', 'cacheLimit': 0}
                res = r.post('https://www.screenshotmachine.com/capture.php', data=form).json()
                result = 'https://www.screenshotmachine.com/'+res['link']
                fl = r.get(result, data={'file':result.replace('serve.php?file=', '')})
                with open('img/ss_full.jpg', 'wb') as f:
                    f.write(fl.content)
                return send_file('img/ss_full.jpg')
            except Exception as e:
                print(e)
                return{
                    'result': 'Url tidak valid!'
                }
        else:
            return{
                'result': 'Masukkan parameter device!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/ssweb_pdf', methods=['GET','POST'])
def ssweb_pdf():
    if request.args.get('url'):
        try:
            r = cloudscraper.create_scraper()
            url = request.args.get('url')
            res = r.post('https://www.screenshotmachine.com/capture-pdf.php', data={'url': url, 'orientation': 'portrait'}).json()
            result = 'https://www.screenshotmachine.com/'+res['link']
            fl = r.get(result, data={'file':result.replace('serve.php?file=', '')})
            with open('file/ssweb.pdf', 'wb') as f:
                f.write(fl.content)
            return send_file('file/ssweb.pdf')
        except Exception as e:
            print(e)
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/tiktok_audio', methods=['GET','POST'])
def tiktok_audio():
    if request.args.get('url'):
        try:
            link = request.args.get('url')
            scraper = cloudscraper.create_scraper()
            be = bs(scraper.get('https://ssstik.io/id').text, 'html.parser').find('form', class_='pure-form pure-g hide-after-request')
            url = 'https://ssstik.io'+be['data-hx-post']
            tt_s = be['include-vals']
            tt = tt_s[4:36]
            ts = tt_s[42:56]
            posts = bs(scraper.post(url, data={'id': link, 'locale': 'id', 'tt': tt, 'ts': ts}).text, 'html.parser')
            mp3 = 'https://ssstik.io'+posts.find('a', class_='pure-button pure-button-primary is-center u-bl dl-button download_link music')['href']
            return{
                'result': mp3
            }
        except Exception as e:
            print(e)
            return {
                'result': 'Terjadi kesalahan'
            }
    else:
        return {
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/tiktok_profile', methods=['GET','POST'])
def tiktok_profile():
    if request.args.get('username'):
        try:
            r = requests
            user = request.args.get('username').replace('@', '')
            be = bs(r.get('https://www.tiktok.com/@'+user+'?').text, 'html.parser').find('header', class_='jsx-4037782421 share-layout-header share-header')
            n = be.find('div', class_='share-title-container')
            username = n.find('h2').text
            if n.find('svg'):
                verified = 'true'
            else:
                verified = 'false'
            title = n.find('h1').text
            pp = be.find('img')['src']
            data = be.find('h2', class_='count-infos')
            following = data.find('strong', attrs={'title': 'Following'}).text
            followers = data.find('strong', attrs={'title': 'Followers'}).text
            likes = data.find('strong', attrs={'title': 'Likes'}).text
            desc = be.find('h2', class_='share-desc mt10').text
            return{
                'username': username,
                'title': title,
                'verified': verified,
                'profile_pic': pp,
                'followers': followers,
                'following': following,
                'likes': likes,
                'description': desc
            }
        except Exception as e:
            print(e)
            return {
                'result': 'Username tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter username!'
        }

@app.route('/api/fb', methods=['GET','POST'])
def fb():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            be = bs(requests.post('https://www.getfvid.com/downloader', data={'url': url}).text, 'html.parser').find('div', class_='col-md-4 btns-download')
            dl = be.findAll('a')
            hd = dl[0]
            normal = dl[1]
            return{
                'result':{
                    'hd': hd['href'],
                    'normal': normal['href']
                }
            }
        except Exception as e:
            print(e)
            return{
                'result': 'Url tidak vaid'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/line_sticker', methods=['GET','POST'])
def line_sticker():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            bes = bs(requests.get(url).text, 'html.parser')
            be = bes.find('div', class_='mdCMN09ImgListWarp')
            results = []
            for i in be.findAll('li'):
                js_data = i['data-preview']
                jason = json.loads(js_data)
                tipe = jason['type']
                if tipe == 'animation':
                    data = 'animationUrl'
                    stiker = apng2gif(jason[data])
                else:
                    data = 'staticUrl'
                    stiker = jason[data]
                results.append({
                    'type': tipe,
                    'sticker': stiker
                })
            return{
                'author':{
                    'name': bes.find('a', attrs={'data-test': 'sticker-author'}).text,
                    'url': 'https://store.line.me'+bes.find('a', attrs={'data-test': 'sticker-author'})['href']
                },
                'title': bes.find('p', attrs={'data-test': 'sticker-name-title'}).text,
                'thumb': bes.find('img', class_='FnImage')['src'],
                'count': len(be.findAll('li')),
                'result': results
            }	
        except Exception as e:
            print(e)
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/translate', methods=['GET','POST'])
def translate():
    if request.args.get('text'):
        text = request.args.get('text')
        if request.args.get('from'):
            f_rom = request.args.get('from')
            if request.args.get('to'):
                to = request.args.get('to')
                try:
                    r = cloudscraper.create_scraper()
                    payload = {
                        'text_to_translate': text, 
                        'source_lang': f_rom, 
                        'translated_lang': to, 
                        'use_cache_only': 'false'
                    }
                    tr = r.post('https://www.translate.com/translator/ajax_translate', data=payload).text
                    res = json.loads(tr)
                    return{
                        'from': f_rom,
                        'to': to,
                        'original_text': res['original_text'],
                        'translated_text': res['translated_text']
                    }
                except Exception as e:
                    print(e)
                    return{
                        'result': 'Kode bahasa tidak valid!'
                    }
            else:
                return{
                    'result': 'Masukkan parameter to!'
                }
        else:
            return{
                'result': 'Masukkan parameter from'
            }
    else:
        return{
            'result': 'Masukkan parameter text'
        }

@app.route('/api/pinterest', methods=['GET','POST'])
def pinterest():
    if request.args.get('url'):
        try:
            q = request.args.get('url')
            r = cloudscraper.create_scraper()
            be = bs(r.post('https://pinterestvideodownloader.com/', data={'url': q}).text, 'html.parser').find('div', class_='col-sm-12')
            if be.find('video'):
                result = be.find('source')['src']
            else:
                result = be.find('img')['src']
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url'
        }

@app.route('/api/kbbi', methods=['GET','POST'])
def kbbi():
    if request.args.get('q'):
        try:
            r = cloudscraper.create_scraper()
            q = request.args.get('q')
            be = bs(r.get('https://kbbi.kemdikbud.go.id/entri/'+q).text, 'html.parser').find('ol')
            res = []
            for i in be.findAll('li'):
                res.append({
                    'result': i.text
                })
            return{
                'query': q,
                'search': res
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/gsm_arena', methods=['GET','POST'])
def gsm_arena():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            r = requests

            bes = bs(r.get('https://www.gsmarena.com/res.php3?sSearch='+q).text, 'html.parser').find('div', class_='makers')
            url = 'https://www.gsmarena.com/'+bes.find('a')['href']
            be = bs(r.get(url).text, 'html.parser')
            title = be.find('h1', class_='specs-phone-name-title').text
            release = be.find('span', attrs={'data-spec': 'released-hl'}).text
            weight = be.find('span', attrs={'data-spec': 'body-hl'}).text
            os_ver = be.find('span', attrs={'data-spec': 'os-hl'}).text
            storage = be.find('span', attrs={'data-spec': 'storage-hl'}).text
            display_size = be.find('span', attrs={'data-spec': 'displaysize-hl'}).text
            display_res = be.find('div', attrs={'data-spec': 'displayres-hl'}).text
            camera_pixel =  be.find('span', attrs={'data-spec': 'camerapixels-hl'}).text+' MP'
            video_pixel =  be.find('div', attrs={'data-spec': 'videopixels-hl'}).text
            ram = be.find('span', attrs={'data-spec': 'ramsize-hl'}).text
            battery = be.find('span', attrs={'data-spec': 'batsize-hl'}).text
            spec_list = be.find('div', id='specs-list')
            spec = []
            for i in spec_list.findAll('table'):
                spec.append({
                    'list': i.text
                })
            sp = be.find('div', class_='specs-photo-main')
            img = sp.find('img')['src']
            return{
                'title': title,
                'released': release,
                'img': img,
                'weight': weight,
                'os_version': os_ver,
                'storage': storage,
                'display_size': display_size,
                'display_resolution': display_res,
                'camera_pixel': camera_pixel,
                'video_pixel': video_pixel,
                'ram': ram,
                'battery': battery,
                'spec': spec
            }
        except Exception as e:
            print(e)
            return {
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/emoji2png', methods=['GET','POST'])
def emoji2png():
    if request.args.get('emoji'):
        if request.args.get('type'):
            try:
                moji = request.args.get('emoji')
                emoji = '{:X}'.format(ord(moji)).lower()
                tipe = request.args.get('type')
                if tipe == 'apple':
                    url = 'https://emoji.aranja.com/static/emoji-data/img-apple-160/'+emoji+'.png'
                elif tipe == 'google':
                    url = 'https://emoji.aranja.com/static/emoji-data/img-google-136/'+emoji+'.png'
                elif tipe == 'twitter':
                    url = 'https://emoji.aranja.com/static/emoji-data/img-twitter-72/'+emoji+'.png'
                elif tipe == 'facebook':
                    url = 'https://emoji.aranja.com/static/emoji-data/img-facebook-96/'+emoji+'.png'
                elif tipe == 'messenger':
                    url = 'https://emoji.aranja.com/static/emoji-data/img-messenger-128/'+emoji+'.png'
                else:
                    url = 'https://emoji.aranja.com/static/emoji-data/img-apple-160/'+emoji+'.png'
                req = get(url)
                with open('img/emoji.png', 'wb') as f:
                    f.write(req.content)
                return send_file('img/emoji.png')
            except Exception as e:
                return{
                    'result': 'Emoji tidak valid!'
                }
        else:
            return{
                'result': 'Masukkan parameter type!'
            }
    else:
        return{
            'result': 'Masukkan parameter emoji!'
        }

@app.route('/additional', methods=['GET','POST'])
def additional():
    return{
        'additional':{
            'emoji2png': 'type = apple, google, twitter, facebook, & messenger'
        }
    }


@app.route('/api/qrcode', methods=['GET','POST'])
def qrcode_gen():
    if request.args.get('text'):
        try:
            input_data = request.args.get('text')
            qr = qrcode.QRCode(
            version=2,
            box_size=15,
            border=2)
            qr.add_data(input_data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img.save('img/qrcode.png')
            return send_file('img/qrcode.png')
        except Exception as e:
            print(e)
            return{
                'result': 'Gagal membuat qr!'
            }
    else:
        return{
            'result': 'Masukkan parameter text!'
        }

@app.route('/api/qr_read', methods=['GET','POST'])
def qr_read():
    if request.args.get('image_url'):
        try:
            img = request.args.get('image_url')
            be = bs(get('https://zxing.org/w/decode?u='+img, json={'u': img}).text, 'html.parser').findAll('pre')
            raw_text = be[0].text
            raw_bytes = be[1].text
            return{
                'result':{
                    'raw_text': raw_text,
                    'raw_bytes': raw_bytes
                }
            }
        except Exception as e:
            print(e)
            return{
                'result':'Gagal scan qr'
            }
    else:
        return{
            'result': 'Masukkan parameter image_url'
        }

@app.route('/api/resep', methods=['GET','POST'])
def resep():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            r = cloudscraper.create_scraper()
            s = bs(r.get('https://cookpad.com/id/cari/'+q+'?event=search.suggestion').text, 'html.parser')
            be = bs(r.get('https://cookpad.com'+s.find('a', class_='media')['href']).text, 'html.parser')
            title = be.find('h1', class_='break-words mb-xs text-cookpad-18 xs:text-cookpad-24 md:text-cookpad-36 font-semibold leading-tight clear-both field-group--no-container-xs').text.replace('  ', '')
            uploaded_by = be.find('span', class_='text-cookpad-14 xs:text-cookpad-16').text
            pic = be.find('picture')
            thumb = pic.find('img')['src']
            bahan = be.find('div', class_='ingredient-list').text.replace('  ', '')
            langkah = []
            for i in be.findAll('p', class_='mb-sm inline'):
                langkah.append(i.text)
            return{
                'title': title,
                'uploaded by': uploaded_by,
                'img': thumb,
                'bahan': bahan,
                'langkah': langkah
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter q'
        }


@app.route('/api/remove-bg', methods=['GET','POST'])
def remove_bg():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            r = get('https://jojo-rmv-bg.herokuapp.com/api/remove-bg?url='+url)
            with open('img/remove_bg.png', 'wb') as f:
                f.write(r.content)

            return send_file('img/remove_bg.png')
        except Exception as e:
            print(e)
            return{
                'result': 'Gagal menghapus background'
            }
    else:
        return{
            'result': 'masukkan parameter url!'
        }

@app.route('/api/barcode_maker', methods=['GET','POST'])
def barcode_maker():
    if request.args.get('text'):
        try:
            be = bs(post('https://ezgif.com/barcode-generator?ajax=true', data={'barcode-content': request.args.get('text')}).text, 'html.parser')
            img = get('https:'+be.find('img')['src'])
            with open('img/barcode.png', 'wb') as f:
                f.write(img.content)
            return send_file('img/barcode.png')
        except Exception as e:
            print(e)
            return{
                'result': 'Gagal membuat qrcode'
            }
    else:
        return{
            'result':'Masukkan parameter text!'
        }

@app.route('/api/barcode_read', methods=['GET','POST'])
def barcode_read():
    if request.args.get('image_url'):
        try:
            img = request.args.get('image_url')
            be = bs(get('https://zxing.org/w/decode?u='+img, json={'u': img}).text, 'html.parser').findAll('pre')
            raw_text = be[0].text
            raw_bytes = be[1].text
            return{
                'result':{
                    'raw_text': raw_text,
                    'raw_bytes': raw_bytes
                }
            }
        except Exception as e:
            print(e)
            return{
                'result':'Gagal scan qr'
            }
    else:
        return{
            'result': 'Masukkan parameter image_url'
        }

@app.route('/api/img_upload', methods=['GET','POST'])
def img_upload():
    return render_template('img_upload.html')

@app.route('/upload_img', methods=['GET','POST'])
def up_img():
    if request.method=='POST':
        try:
            data_file = request.files['file']
            r = requests.Session()
            filename = id_generator()+secure_filename(data_file.filename)
            if allowed_file(data_file.filename):
                data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                token = bs(r.get('https://imgbb.com/upload').text, 'html.parser').find('input', attrs={'name': 'auth_token'})['value']
                j_son = r.post('https://imgbb.com/json', data={'type': 'file', 'action': 'upload', 'auth_token': token}, files={'source': open('file/'+filename, 'rb')}).json()
                return{
                    'result': {
                        'url':j_son['image']['url'],
                        'filesize': size(j_son['image']['size'])+'B',
                        'extension': j_son['image']['extension']
                    }
                }
                if os.path.exists('file/'+filename):
                    os.remove('file/'+filename)
            else:
                return{
                    'result': 'file not allowed!'
                }
        except Exception as e:
            print(e)
            return{
                'result': 'gagal'
            }
@app.route('/api/yt-search', methods=['GET','POST'])
def yt_search():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            return {
                'result': VideosSearch(q, limit = 10).result()
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/google-search', methods=['GET','POST'])
def google_search():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            print(search(q, num_results=10))
            return {
                'a':'b'
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/playstore', methods=['GET','POST'])
def playstore():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            scraper = cloudscraper.create_scraper()
            result = []
            be = bs(scraper.get('https://play.google.com/store/search?q='+q+'&c=apps').text, 'html.parser')
            for i in be.findAll('div', class_='ImZGtf mpg5gc'):
                base = 'https://play.google.com'
                url = base+i.find('a')['href']
                dev_id = base+i.find('a', class_='mnKHRc')['href']
                img = i.find('img', class_="T75of QNCnCf")['data-src']
                rate = i.find('div', attrs={'role': 'img'})['aria-label']
                result.append({
                    'app':{
                        'name': be.find('div', class_='WsMG1c nnK0zc')['title'],
                        'id': url.replace('https://play.google.com/store/apps/details?id=', ''),
                        'url': url
                    },
                    'developer':{
                        'name': i.find('a', class_='mnKHRc').text,
                        'id': dev_id
                    },
                    'img': img,
                    'rate': rate
                })
            return {
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': request.args.get('q')+' tidak di temukan'
            }
    else:
        return{
            'result': 'masukkan parameter q!'
        }

@app.route('/api/smule_recording', methods=['GET','POST'])
def smule_recording():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            scraper = cloudscraper.create_scraper()
            be = bs(scraper.post('https://singdownloader.com/index.php', data={'formurl': url}).text, 'html.parser')
            vid = be.find('source')['src']
            p = be.find('div', class_='getting-started-info')
            aud = p.find('a')['href'].replace(' ', '')
            return{
                'result':{
                    'video': vid.replace('\n', ''),
                    'audio': aud.replace('\n', '')
                }
            }
        except Exception as e:
            print(e)
            return{
                'result': 'url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/twitter', methods=['GET','POST'])
def twitter():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            r = cloudscraper.create_scraper()
            s = bs(r.post('https://www.savetweetvid.com/downloader', data={'url': url}).text, 'html.parser')
            be = s.find('tbody')
            result = []
            for i in be.findAll('tr'):
                td = i.findAll('td')
                result.append({
                    'quality': td[0].text,
                    'format': td[1].text,
                    'size': td[2].text,
                    'download': i.find('a')['href']
                })
            return{
                'result':{
                    'caption': s.find('p', class_='card-text').text,
                    'media': result
                }
            }
        except Exception as e:
            print(e)
            return{
                'result': 'url tidak valid!'
            }
    else:
        return{
            'result': 'masukkan parameter url!'
        }

@app.route('/api/neonime_search', methods=['GET','POST'])
def neonine_s():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            r = cloudscraper.create_scraper()
            be = bs(r.get('https://neonime.vip/?s='+q).text, 'html.parser')
            result = []
            for i in be.findAll('div', class_='item episode-home'):
                url = i.find('a')['href']
                judul = i.find('span', class_='tt title-episode').text
                thumb = i.find('img')['data-src']
                desc = i.find('span', class_='ttx').text
                result.append({
                    'title': judul,
                    'url': url,
                    'thumb': thumb,
                    'desc': desc
                })
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': request.args.get('q')+' tidak di temukan!'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/neonime_batch', methods=['GET','POST'])
def neonime_batch():
    if request.args.get('url'):
        try:
            url = request.args.get('url')
            r = cloudscraper.create_scraper()
            be = bs(r.get(url).text, 'html.parser').find('div', class_='entry-content')
            release = be.find('p').text
            img = be.find('img')['src']
            p = be.findAll('p')
            desc = p[3].text
            title_en = p[4].text
            title_jp = p[5].text
            episode = p[7].text
            duration = p[17].text
            rating = p[18].text
            score = p[19].text
            dl_link = []
            for dl in be.findAll('p', class_='smokeurl'):
                link = [links['href'] for links in dl.findAll('a')]
                dl_link.append({
                    dl.find('strong').text: link
                })
            return{
                'title':{
                    'en': title_en,
                    'jp': title_jp
                },
                'release': release,
                'img': img,
                'desc': desc,
                'episode': episode,
                'duration': duration,
                'rating': rating,
                'score': score,
                'download_link': dl_link
            }
        except Exception as e:
            print(e)
            return{
                'result': 'url tidak valid!'
            }
    else:
        return{
            'result': 'masukkan parameter url!'
        }

@app.route('/api/nhentai_search', methods=['GET','POST'])
def nhentai_search():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            r = cloudscraper.create_scraper()
            be = bs(r.get('https://nhentai.net/search/?q='+q).text, 'html.parser')
            result = []
            for i in be.findAll('gallery'):
                url = 'https://nhentai.net/'+i.find('a')['href']
                img = i.find('img')['src']
                caption = i.find('div', class_='caption').text
                code = url.replace('https://nhentai.net/g/', '').replace('/', '')
                print(img)
                print(caption)
                result.append({
                    'url': url,
                    'img': img,
                    'caption': caption,
                    'code': code
                })
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': request.args.get('q')+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter q!'
        }

@app.route('/api/getsticker', methods=['GET','POST'])
def getsticker():
    if request.args.get('q'):
        try:
            from random import randrange
            q = request.args.get('q')
            be = bs(get('https://getstickerpack.com/stickers?query='+q).text, 'html.parser')
            url = random.choice([i.find('a')['href'] for i in be.findAll('div', class_='col-md-6 col-lg-4 col-12 col-sm-6 sticker-pack-cols')])
            sc = bs(get(url).text, 'html.parser')
            title = sc.find('h1').text
            stiker = [i.find('img')['src'] for i in sc.findAll('div', class_='col-xl-3 col-lg-3 col-md-3 col-sm-4 col-4 sticker-pack-cols')]
            return{
                'title': title,
                'result':{
                    'sticker': stiker
                }
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/wallpaper_hd', methods=['GET','POST'])
def wallpaper_hd():
    if request.args.get('q'):
        try:
            q = request.args.get('q').replace(' ', '-')
            print(q)
            r = cloudscraper.create_scraper()
            be = bs(r.get('https://unsplash.com/s/photos/'+q).text, 'html.parser')
            result = []
            for i in be.findAll('img', class_='_2UpQX'):
                #print(i.find('img'))
                result.append(i['src'])
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'Masukkan parameter q!'
        }

@app.route('/api/shorturl-at', methods=['GET','POST'])
def shorturl_at():
    if request.args.get('url'):
        try:
            return{
                'result': shortener(request.args.get('url'))
            }
        except Exception as e:
            print(e)
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'masukkan parameter url!'
        }

@app.route('/api/cuttly', methods=['GET','POST'])
def cuttly():
    if request.args.get('url'):
        try:
            r = cloudscraper.create_scraper()
            return{
                'result': r.post('https://cutt.ly/scripts/shortenUrl.php', data={'url': request.args.get('url'), 'domain': '0'}).text
            }
        except Exception as e:
            print(e)
            return{
                'result': 'Url tidak valid!'
            }
    else:
        return{
            'result': 'masukkan parameter url!'
        }

@app.route('/api/cersex', methods=['GET','POST'])
def cersex():
    try:
        scraper = cloudscraper.create_scraper()
        r = bs(scraper.get('http://ceritasexindonesia.com/').text, 'html.parser')
        randoms = random.choice([i['href'] for i in r.findAll('a', class_='img-holder')])
        be = bs(scraper.get(randoms).text, 'html.parser')
        e = be.find('div', class_='entry-content clearfix single-post-content')
        res = []
        for i in e.findAll('p'):
            res.append(i.text)
        resl = json.dumps(res)
        title = be.find('span', class_='post-title').text
        img = be.find('img', attrs={'alt': title})['data-src']
        print(img)
        return{
            'result': {
                'judul': title,
                'img': img,
                'cersex': resl.replace('[', '').replace(']', '')
            }
        }
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan'
        }

@app.route('/api/cerpen', methods=['GET','POST'])
def cerpen():
    try:
        be = bs(get('http://cerpenmu.com/100-cerpen-kiriman-terbaru').text, 'html.parser').findAll('div', class_='box')[7]
        rk = random.choice([i.find('a')['href'] for i in be.findAll('li')])
        b_rp = bs(get(rk).text, 'html.parser')
        rp = random.choice([i.find('a')['href'] for i in b_rp.findAll('article', class_='post')])
        bes = bs(get(rp).text, 'html.parser')
        title = bes.find('h1').text
        res = bes.find('article', class_='post')
        a = res.findAll('a')
        pengarang = a[0].text
        kategori = a[1].text
        cp = []
        for i in res.findAll('p'):
            cp.append(i.text)
        cerpen = json.dumps(cp)
        return{
            'result':{
                'title': title,
                'pengarang': pengarang,
                'kategori': kategori,
                'cerpen': cerpen.replace('[', '').replace(']', '')
            }
        }
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan'
        }

@app.route('/api/tafsir', methods=['GET','POST'])
def tafsir():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            be = bs(get('https://tafsirq.com/topik/'+q).text, 'html.parser')
            res = []
            for i in be.findAll('div', class_='panel panel-default'):
                res.append({
                    i.find('span', class_='label label-default').text.replace(' ', '_'): i.find('div', class_='panel-heading panel-choco').text.replace('\n', '').replace('tafsir', '').replace('terjemahan ayat', ''),
                    'deskripsi': i.find('div', class_='panel-body excerpt').text.replace('\n  ', '').replace('  ', '')
                })
            return{
                'result': res
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan'
            }
    else:
        return{
            'result': 'masukkan parameter q!'
        }

@app.route('/api/gdrive_bypass', methods=['GET','POST'])
def gdrive_bypass():
    if request.args.get('url'):
        try:
            return jsonify(get('https://gdbypass.host/api/?link='+request.args.get('url')).json())
        except Exception as e:
            print(e)
            return{
                'result': 'url tidak valid!'
            }
    else:
        return{
            'result': 'Masukkan parameter url!'
        }

@app.route('/api/meme-gen', methods=['GET','POST'])
def meme_gen():
    if request.args.get('top'):
        top = request.args.get('top')
        if request.args.get('bottom'):
            bottom = request.args.get('bottom')
            if request.args.get('img'):
                img = request.args.get('img')
                try: 
                    r = get('https://api.memegen.link/images/custom/'+top+'/'+bottom+'.png?background='+img)
                    with open('img/meme_gen.jpg', 'wb') as f:
                        f.write(r.content)
                    return send_file('img/meme_gen.jpg') 
                except Exception as e:
                    print(e)
                    return{
                        'result': 'terjadi kesalahan!'
                    }
            else:
                return{
                    'result': 'Masukkan parameter img!'
                }
        else:
            return{
                'result': 'masukkan parameter bottom!'
            }
    else:
        return{
            'result': 'Masukkan parameter top!'
        }

@app.route('/api/github_profile', methods=['GET','POST'])
def github_profile():
    if request.args.get('username'):
        try:
            be = bs(get('https://github.com/'+request.args.get('username')).text, 'html.parser')
            fullname = be.find('span', class_='p-name vcard-fullname d-block overflow-hidden').text
            nickname = be.find('span', class_='p-nickname vcard-username d-block').text
            bio = be.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4').text
            #d = be.find('div', class_='mb-3')
            data = be.findAll('a', class_='link-gray no-underline no-wrap') 
            followers = data[0].text.replace('\n', '').replace('  ', '').replace('followers', '')
            following = data[1].text.replace('\n', '').replace('  ', '').replace('following', '')
            stars = data[2].text.replace('\n', '').replace('  ', '')
            return{
                'result':{
                    'fullname': fullname,
                    'nickname': nickname,
                    'bio': bio,
                    'followers': followers,
                    'following': following,
                    'stars': stars
                }
            }
        except Exception as e:
            print(e)
            return{
                'result': 'username tidak valid1'
            }
    else:
        return{
            'result': 'masukkan parameter username'
        }
@app.route('/api/artinama', methods=['GET','POST'])
def artinama():
    if request.args.get('nama'):
        try:
            be = bs(get('https://www.primbon.com/arti_nama.php?nama1='+request.args.get('nama')+'&proses=+Submit%21+').text, 'html.parser')
            res = be.find('div', id='body').text.replace('\n', '').replace('ARTI NAMA', '').replace('  ', '').replace('Nama:', '').replace('(JAWA)', '').replace('Berikut ini adalah kumpulan arti nama lengkap dari A-Z dalam budaya (bahasa) Jawa untuk Laki-laki (L) dan Perempuan', '')
            res2 = res.replace('(P).Arti Nama (L) Arti Nama (P) (ARAB / ISLAM)', '').replace('Berikut ini adalah kumpulan arti nama lengkap dari A-Z dalam budaya (bahasa) Arab atau bernuansa Islami untuk Laki-laki (L) dan Perempuan (P).Arti Nama (L) Arti Nama (P)Catatan: Gunakan juga aplikasi numerologi Kecocokan Nama, untuk melihat sejauh mana keselarasan nama anda dengan diri anda.', '')
            return{
                'result': res2
            }
        except Exception as e:
            print(e)
            return{
                'result': 'terjadi kesalahan!'
            }
    else:
        return{
            'result': 'masukkan parameter nama!'
        }

@app.route('/api/nomer_hoki', methods=['GET','POST'])
def nomer_hoki():
    if request.args.get('nomer'):
        try:
            sc = bs(post('https://www.primbon.com/no_hoki_bagua_shuzi.php', data={'nomer': request.args.get('nomer'), 'submit': 'Submit!'}).text, 'html.parser')
            be = sc.findAll('table')[1]
            be2 = sc.find('div', id='body')
            shuzi = be2.findAll('b')[2].text
            fa = be.findAll('td')
            positif = fa[0].text.replace('ENERGI POSITIF', '')
            negatif = fa[2].text.replace('ENERGI NEGATIF', '')
            return{
                'nomer': request.args.get('nomer'),
                'result':{
                    'angka_shuzi': shuzi,
                    'energi_positif': positif,
                    'energi_negatif': negatif
                }
            }
        except Exception:
            return{
                'result': 'Nomer hp salah!'
            }
    else:
        return{
            'result': 'masukkan parameter nomer'
        }

@app.route('/api/rain_gif', methods=['GET','POST'])
def rain_gif():
    if request.args.get('image_url'):
        try:
            image = request.args.get('image_url')
            r = get(image)
            with open('img/rain_gif.jpg', 'wb') as f:
                f.write(r.content)
            with open('img/rain_gif.jpg', "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            be = bs(post('https://photooxy.com/art-effects/gif-animated-rain-online-361.html', data={'image_0': encoded_string, 'login': 'OK'}).text, 'html.parser').find('div', class_='thumbnail')
            res = requests.get('https://photooxy.com'+be.find('img')['src'])
            print(res)
            with open('img/rain_gif.gif', 'wb') as f:
                f.write(res.content)
            return send_file('img/rain_gif.gif')
        except Exception as e:
            print(e)
            return{
                'result': 'Gambar tidak valid!'
            }
    else:
        return{
            'result': 'masukkan parameter image_url'
        }

@app.route('/api/fancy', methods=['GET','POST'])
def fancy():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            res = bs(requests.get('http://qaz.wtf/u/convert.cgi?text='+text).text, 'html.parser')
            result = [i.findAll('td')[1].text.replace('\n', '') for i in res.findAll('tr')]
            return {
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': 'gagal'
            }
    else:
        return{
            'result': 'Masukkan parameter text!'
        }

@app.route('/api/gaming', methods=['GET','POST'])
def gaming():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            r = cloudscraper.create_scraper()
            url = 'https://ephoto360.com/tao-logo-team-logo-gaming-phong-cach-sat-thu-653.html'
            be = bs(r.get(url).text, 'html.parser')
            token = be.find('input', attrs={'name': 'token'})['value']
            radio = random.choice([i['value'] for i in be.findAll('input', attrs={'type': 'radio'})])
            build_server = be.find('input', attrs={'name': 'build_server'})['value']
            build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
            data = {'autocomplete0': '0', 'radio0[radio]': radio, 'text[]': text, 'submit': 'Create a photo', 'token': token, 'build_server': build_server, 'build_server_id': build_server_id}
            bes = bs(r.post(url, data).text, 'html.parser')
            fv = bes.find('input', id='form_value_input')['value']
            js = json.loads(fv)
            res = r.post('https://ephoto360.com/effect/create-image', data={'id': '653', 'autocomplete0': '0', 'radio0[radio]': radio, 'text[]': text, 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
            result = build_server+res['image']
            req = r.get(result)
            with open('img/gaming_logo.jpg', 'wb') as f:
                f.write(req.content)
            crop.crop1('', 'gaming_logo')
            return send_file('img/gaming_logo.jpg')
        except Exception as e:
            print(e)
            return{
                'result': 'masukkan parameter text!'
            }
    else:
        return{
            'result': 'Masukkan parameter text!'
        }

@app.route('/api/galaxywp', methods=['GET','POST'])
def galaxywp():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            scraper = cloudscraper.create_scraper()
            url = 'https://ephoto360.com/tao-hinh-nen-dien-thoai-galaxy-theo-ten-dep-full-hd-684.html'
            gt = scraper.get(url)
            be = bs(gt.text, 'html.parser')
            token = be.find('input', attrs={'name': 'token'})['value']
            build_server = be.find('input', attrs={'name': 'build_server'})['value']
            build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
            radio = random.choice([i['value'] for i in be.findAll('input', attrs={'type': 'radio'})])
            frs = bs(scraper.post(url, data={'radio0[radio]': radio, 'text[]':text, 'submit': 'Create a photo', 'token': token, 'build_server': build_server, 'build_server_id': build_server_id }).text, 'html.parser')
            fv = frs.find('input', id='form_value_input')['value']
            js = json.loads(fv)
            p = scraper.post('https://ephoto360.com/effect/create-image', data={'id': '684', 'radio0[radio]': radio, 'text[]': text, 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
            result = build_server+p['image']
            req = scraper.get(result)
            with open('img/Galaxy Wallpaper.jpg', 'wb') as f:
                f.write(req.content)
            return send_file('img/Galaxy Wallpaper.jpg')
        except Exception as e:
            print(e)
            return{
                'result': 'terjadi kesalahan!'
            }
    else:
        return{
            'result': 'Masukkan parameter text!'
        }

@app.route('/api/toonify', methods=['GET','POST'])
def toonify():
    if request.args.get('image_url'):
        try:
            image = request.args.get('image_url')
            r = get(image)
            with open('img/toonify_before.jpg', 'wb') as f:
                f.write(r.content)
            be = bs(requests.post('https://toonify.photos/original', files={'image': open('img/toonify_before.jpg', 'rb')}).text, 'html.parser')
            cs = be.find('div', class_='row mt-5 mx-auto')
            img = cs.findAll('img')[1]['src']
            res = get(img)
            with open('img/toonify.jpg', 'wb') as f:
                f.write(res.content)
            return send_file('img/toonify.jpg')
        except Exception as e:
            print(e)
            return{
                'result': 'terjadi kesalahan!'
            }
    else:
        return{
            'result': 'masukkan parameter image_url'
        }

@app.route('/api/brainly', methods=['GET','POST'])
def brainly():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            scraper = cloudscraper.create_scraper()
            f = scraper.get('https://rest.farzain.com/api/brainly.php?id='+q+'&apikey=rambu').json()
            headers = requests.utils.default_headers()
            headers.update({
                'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
                'cookie': '__cfduid=d9d5840ba8b47a85e69a9b8811f11bd531612420017; _ga=GA1.3.492770082.1612420063; _hjid=2f0d1993-d9d8-4f64-9c24-f908e149238a; cf_chl_prog=a17; cf_clearance=4692728ef5db194c8494f64c8aa643b4c336e724-1612509394-0-250; _gid=GA1.3.2093313000.1612509395; _hjIncludedInSessionSample=1; _hjAbsoluteSessionInProgress=0; hl=id; experimentId=edb7372c70a30304c724178ef84e97e496166ab08ec3a4f92b77fce5d6934720; Zadanepl_cookie[Token][Guest]=b356a3f10118e49b4721e9f53c1dd9fa9e910c07467c4050ce6ea201bc588ea841f7360bf6b1b168; _pbjs_userid_consent_data=3524755945110770; _pubcid=2e0a05fe-dc07-49d9-944d-a29b7a103967; Zadanepl_cookie[infobar]=; _lr_geo_location=SG; _lr_retry_request=true; pbjs-unifiedid={"TDID":"f6c4ade3-d740-4976-b984-1a7d9a532e5d","TDID_LOOKUP":"TRUE","TDID_CREATED_AT":"2021-01-05T07:16:41"}; inHouseAds=JTdCJTIydG9wbGF5ZXJfcmVnaXN0cmF0aW9uJTIyJTNBJTVCMTYxMjUwOTQwNSU1RCU3RA==; __gads=ID=0fb8eb58caa25eb5:T=1612509407:S=ALNI_MbZbP70OQQDtj_0zy1g_EuJo39H6w; cto_bidid=vYi3B19DUUZYRk1FTGcwWiUyQlBIZkYzRGJWaHpxRmVXTzRpQmM2S0dFZDNMcHY4WiUyQnVNbzlUYTF6VnJRblhNeVhWT09KZjNLcmtaZ2ZLYjh5SDV6MDF1cEVYJTJCeWJkS3l3OUtiRHNIYUhEJTJGZVZZam9vJTNE; cto_bundle=YHc-RV9pJTJCOWZWN3ZNVnc3NXBXN2duaFRiU2VWVktyUGNzUW5uM20lMkI2TnglMkZrWTJDVFBFVTM1ZHFGJTJGSTZna0ptNzZKZCUyQlRkakNEenRNeFVDOEsyeWN5JTJCaXprdmszUWVzJTJCJTJGZjNuU0JXanVXWCUyRnM0em1zSHlQQnpnSDZwVzdRV2d5UU9VcFgyenNsJTJCR3lkanRvejdFTVV6bm9JZyUzRCUzRA; _dc_gtm_UA-43911963-1=1'
            })
            result = []
            proxy = {
                "http": "http://119.252.168.222:7676",
                "https": "https://119.252.168.222:7676"
            }
            for i in f:
                brainly = requests.get(i['url'], proxies=proxy)
                be = bs(brainly.text, "html.parser")
                print(be)
                pertanyaan = be.find('span', class_='sg-text sg-text--large sg-text--bold sg-text--break-words brn-qpage-next-question-box-content__primary').text
                jawaban = be.find('div', class_='sg-text sg-text--break-words brn-rich-content js-answer-content').text
                d = be.find('ul', class_='brn-horizontal-list')
                fa = d.findAll('li')
                pelajaran = fa[1].text.replace('\n', '')
                kelas = fa[2].text.replace('\n', '')
                result.append({
                    'pertanyaan': pertanyaan.replace('\n', ''),
                    'jawaban': jawaban.replace('\n', ''),
                    'pelajaran': pelajaran,
                    'kelas': kelas
                })
            return{
                'query': q,
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter q!'
        }

@app.route('/api/ip_geolocation', methods=['GET','POST'])
def ip_geolocation():
    if request.args.get('ip'):
        try:
            return jsonify(get('http://api.ipstack.com/'+request.args.get('ip')+'?access_key=57c8660a16b6b73d1207de03fac34ee8&format=1').json())
        except Exception as e:
            print(e)
            return{
                'result': 'ip tidak valid'
            }
    else:
        return{
            'result': 'masukkan parameter ip!'
        }

@app.route('/api/heroml', methods=['GET','POST'])
def heroml():
    if request.args.get('hero'):
        try:
            hero = request.args.get('hero')
            url = 'https://mobile-legends.fandom.com/wiki/'+hero
            be = bs(requests.get(url).text, 'html.parser')
            pic = be.find('div', class_='ml-img ml-round hero-img _link _xl _resize')
            img = pic.find('a')['href']
            tbody = be.findAll('tbody')[3]
            tbody2 = be.findAll('tbody')[4]
            tbody3 = be.findAll('tbody')[5]
            name = tbody.find('b').text
            quotes = tbody2.find('i').text
            role = tbody3.findAll('span', class_='mw-headline')[0].text
            speciality = tbody3.findAll('span', class_='mw-headline')[1].text
            laning_recommendation = tbody3.findAll('span', class_='mw-headline')[2].text
            release = tbody3.findAll('span', class_='mw-headline')[3].text
            atrributes = be.findAll('tbody')[6]
            movement = atrributes.findAll('td')[1].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[0].text, '')
            physical_atk = atrributes.findAll('td')[2].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[1].text, '')
            magic_pow = atrributes.findAll('td')[3].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[2].text, '')
            attack = atrributes.findAll('td')[4].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[3].text, '')
            physical_def = atrributes.findAll('td')[5].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[4].text, '')
            magic_def = atrributes.findAll('td')[6].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[5].text, '')
            basic_atk = atrributes.findAll('td')[7].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[6].text, '')
            hp = atrributes.findAll('td')[8].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[7].text, '')
            mana = atrributes.findAll('td')[9].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[8].text, '')
            ability = atrributes.findAll('td')[10].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[9].text, '')
            hp_regen = atrributes.findAll('td')[11].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[10].text, '')
            mana_regen = atrributes.findAll('td')[12].text.replace(atrributes.findAll('div', class_='text-transform-upr font-bold')[11].text, '')
            return{
                'result':{
                    'hero':{
                        'name': name,
                        'quotes': quotes,
                        'img': img,
                        'role': role,
                        'speciality': speciality,
                        'laning_recommendation': laning_recommendation,
                        'release_date': release,
                        'attributes':{
                            'movement_speed': movement.replace('\n', ''),
                            'physical_attack': physical_atk.replace('\n', ''),
                            'magic_power': magic_pow.replace('\n', ''),
                            'attack_speed': attack.replace('\n', ''),
                            'physical_defense': physical_def.replace('\n', ''),
                            'magic_defense': magic_def.replace('\n', ''),
                            'basic_atk_crit_rate': basic_atk.replace('\n', ''),
                            'hp': hp.replace('\n', ''),
                            'mana': mana.replace('\n', ''),
                            'ability_crit_rate': ability.replace('\n', ''),
                            'hp_regen': hp_regen.replace('\n', ''),
                            'mana_regen': mana_regen.replace('\n', '')
                        }
                    }
                }
            }
        except Exception as e:
            print(e)
            return{
                'result': hero+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter hero!'
        }

@app.route('/api/artimimpi', methods=['GET','POST'])
def artimimpi():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            be = bs(get('https://www.primbon.com/tafsir_mimpi.php?mimpi='+q+'&submit=+Submit+').text, 'html.parser')
            return{
                'result': be.find('div', id='body').text.replace('ARTI MIMPI ANDA', '').replace('Masukkan kata kunci dari mimpi anda:', '').replace('Misalnya: Anda mimpi sedang berbelanja di pasar, cari dengan kata kunci ', '').replace('belanja', '').replace('atau', '').replace('pasar', '').replace('Solusi - Menanggulangi akibat buruk dari mimpi', '').replace('\n', '')
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter q!'
        }

@app.route('/api/tanggal_jadian', methods=['GET','POST'])
def tanggal_jadian():
    if request.args.get('tgl'):
        tgl = request.args.get('tgl')
        if request.args.get('bln'):
            bln = request.args.get('bln')
            if request.args.get('thn'):
                thn = request.args.get('thn')
                try:
                    url = 'https://www.primbon.com/tanggal_jadian_pernikahan.php?tgl='+tgl+'&bln='+bln+'&thn='+thn+'&proses=+Submit%21+'
                    be = bs(requests.get(url).text, 'html.parser')
                    return{
                        'result': be.find('div', id='body').text
                    }
                except Exception as e:
                    print(e)
                    return{
                        'result': 'tidak di temukan!'
                    }
            else:
                return{
                    'result': 'masukkan parameter thn!'
                }
        else:
            return{
                'result': 'masukkan parameter bln!'
            }
    else:
        return{
            'result': 'masukkan parameter tgl!'
        }

@app.route('/api/watercolor', methods=['GET','POST'])
def watercolor():
    if request.args.get('text'):
        try:
            text = request.args.get('text')
            r = cloudscraper.create_scraper()
            url = 'https://ephoto360.com/tao-hieu-ung-chu-mau-nuoc-an-tuong-truc-tuyen-775.html'
            be = bs(r.get(url).text, 'html.parser')
            token = be.find('input', attrs={'name': 'token'})['value']
            #radio = random.choice(['05acf523-6deb-4b9d-bb28-abc4354d0858', '843a4fc2-059c-4283-87e4-c851c013073b', 'd951e4be-450e-4658-9e73-0f7c82c63ee3', 'a5b374f3-2f29-4da4-ae15-32dec01198e2'])
            build_server = be.find('input', attrs={'name': 'build_server'})['value']
            build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
            data = {'text[]': text, 'submit': 'Create a photo', 'token': token, 'build_server': build_server, 'build_server_id': build_server_id}
            bes = bs(r.post(url, data).text, 'html.parser')
            fv = bes.find('input', id='form_value_input')['value']
            js = json.loads(fv)
            res = r.post('https://ephoto360.com/effect/create-image', data={'id': '775', 'text[]': text, 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
            result = build_server+res['image']
            r = r.get(result)
            with open('img/watercolor.jpg', 'wb') as f:
                f.write(r.content)
            return send_file('img/watercolor.jpg')
        except Exception as e:
            print('Error : %s ' % e)
            return {
                'status': False,
                'error': '[❗] Terjadi kesalahan'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukkan parameter text'
        }

@app.route('/api/sparkling', methods=['GET','POST'])
def sparkling():
    if request.args.get('text1'):
        text1 = request.args.get('text1')
        if request.args.get('text2'):
            text2 = request.args.get('text2')
            try:
                scraper = cloudscraper.create_scraper()
                url = 'https://ephoto360.com/hieu-ung-chu-lap-lanh-nhieu-mau-sac-776.html'
                gt = scraper.get(url)
                be = bs(gt.text, 'html.parser')
                token = be.find('input', attrs={'name': 'token'})['value']
                build_server = be.find('input', attrs={'name': 'build_server'})['value']
                build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
                time.sleep(3)
                radio = random.choice([i['value'] for i in be.findAll('input', attrs={'type': 'radio'})])
                frs = bs(scraper.post(url, data={'radio0[radio]': radio, u'text[]': [u'%s' % text1,u'%s' % text2], 'submit': 'Create a photo', 'token': token, 'build_server': build_server, 'build_server_id': build_server_id }).text, 'html.parser')
                fv = frs.find('input', id='form_value_input')['value']
                js = json.loads(fv)
                p = scraper.post('https://ephoto360.com/effect/create-image', data={'id': '776', 'radio0[radio]': radio, u'text[]': [u'%s' % text1,u'%s' % text2], 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
                result = build_server+p['image']
                print(result)
                req = scraper.get(result)
                with open('img/sparkling.jpg', 'wb') as f:
                    f.write(req.content)
                return send_file('img/sparkling.jpg')
            except Exception as e:
                print(e)
                return{
                    'result': 'terjadi kesalahan!'
                }
        else:
            return{
                'result': 'masukkan parameter text2!'
            }
    else:
        return{
            'result': 'masukkan parameter text1!'
        }

@app.route('/api/random_baguette', methods=['GET','POST'])
def random_baguette():
    try:
        scraper = cloudscraper.create_scraper()
        api = scraper.get('https://api.computerfreaker.cf/v1/baguette').json()
        url = api['url']
        req = scraper.get(url)
        with open('img/baguette.jpg', 'wb') as f:
            f.write(req.content)
        return send_file('img/baguette.jpg')
    except Exception as e:
        print(e)
        return{
            'result': 'gagal'
        }

@app.route('/api/random_dva', methods=['GET','POST'])
def random_dva():
    try:
        scraper = cloudscraper.create_scraper()
        api = scraper.get('https://api.computerfreaker.cf/v1/dva').json()
        url = api['url']
        req = scraper.get(url)
        with open('img/baguette.jpg', 'wb') as f:
            f.write(req.content)
        return send_file('img/baguette.jpg')
    except Exception as e:
        print(e)
        return{
            'result': 'gagal'
        }

@app.route('/api/random_yuri', methods=['GET','POST'])
def random_yuri():
    try:
        scraper = cloudscraper.create_scraper()
        api = scraper.get('https://api.computerfreaker.cf/v1/yuri').json()
        url = api['url']
        req = scraper.get(url)
        with open('img/yuri.jpg', 'wb') as f:
            f.write(req.content)
        return send_file('img/yuri.jpg')
    except Exception as e:
        print(e)
        return{
            'result': 'gagal'
        }

@app.route('/api/tongue_twister', methods=['GET','POST'])
def tongue_twister():
    try:
        be = bs(requests.get('http://www.tongue-twister.net/in.htm').text, 'html.parser')
        return{
            'result': random.choice([i.text for i in be.findAll('p', class_='TXT')])
        }
    except Exception as e:
        print(e)
        return{
            'result': 'gagal!'
        }

@app.route('/api/calendar', methods=['GET','POST'])
def calendar():
    if request.args.get('image_url'):
        try:
            scraper = cloudscraper.create_scraper()
            img_url = request.args.get('image_url')
            req_img = scraper.get(img_url)
            with open('img/calendar_before.jpg', 'wb') as f:
                f.write(req_img.content)
            post_img = scraper.post('https://photofunia.com/images?server=1', json={'server': '1'}, files={'image': open('img/calendar_before.jpg', 'rb')}).json()
            key = post_img['response']['key']
            width = post_img['response']['image']['highres']['width']
            height = post_img['response']['image']['highres']['height']
            reso = f'{width}.{height}'
            res = scraper.post('https://photofunia.com/categories/all_effects/calendar?server=1', allow_redirects=True, data={'current-category': 'all_effects', 'type': 'Year', 'year': '2021', 'image': key, 'image:crop': '0.0.'+reso})
            be = bs(scraper.get(res.url).content, 'html5lib')
            result = be.find('img', id='result-image')['src']
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': 'gagal, silahkan coba lagi!'
            }
    else:
        return{
            'result': 'masukkan parameter image_url!'
        }

@app.route('/api/burning_fire', methods=['GET','POST'])
def burning_fire():
    if request.args.get('image_url'):
        try:
            scraper = cloudscraper.create_scraper()
            img_url = request.args.get('image_url')
            req_img = scraper.get(img_url)
            with open('img/burning_fire.jpg', 'wb') as f:
                f.write(req_img.content)
            post_img = scraper.post('https://photofunia.com/images?server=1', json={'server': '1'}, files={'image': open('img/burning_fire.jpg', 'rb')}).json()
            key = post_img['response']['key']
            width = post_img['response']['image']['highres']['width']
            height = post_img['response']['image']['highres']['height']
            reso = f'{width}.{height}'
            res = scraper.post('https://photofunia.com/categories/all_effects/burning-fire?server=1', allow_redirects=True, data={'current-category': 'all_effects', 'type': 'Year', 'year': '2021', 'image': key, 'image:crop': '0.0.'+reso})
            be = bs(scraper.get(res.url).content, 'html5lib')
            result = be.find('img', id='result-image')['src']
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': 'gagal!'
            }
    else:
        return{
            'result': 'masukkan parameter image_url!'
        }

@app.route('/api/neon_writing', methods=['GET','POST'])
def neon_writing():
    if request.args.get('text1'):
        text1 = request.args.get('text1')
        if request.args.get('text2'):
            text2 = request.args.get('text2')
            try:
                scraper = cloudscraper.create_scraper()
                res = scraper.post('https://photofunia.com/categories/all_effects/neon-writing?server=1', allow_redirects=True, data={'current-category': 'all_effects', 'text': text1, 'text2': text2}, json={'server': '1'})
                be = bs(scraper.get(res.url).content, 'html5lib')
                print(be)
                result = be.find('img', id='result-image')['src']
                return{
                    'result': result
                }
            except Exception as e:
                print(e)
                return{
                    'result': 'gagal!'
                }
        else:
            return{
                'result': 'masukkan parameter text2!'
            }
    else:
        return{
            'result': 'masukkan parameter text1!'
        }

@app.route('/api/news', methods=['GET','POST'])
def news():
    try:
        return jsonify(requests.get('http://newsapi.org/v2/top-headlines?country=id&apiKey=f87da45269a24b37945ec076bf6fd87c').json())
    except Exception as e:
        print(e)
        return {
            'result': 'gagal!'
        }

@app.route('/api/neon', methods=['GET','POST'])
def neon():
    if request.args.get('text1'):
        if request.args.get('text2'):
            if request.args.get('text3'):
                try:
                    text1 = request.args.get('text1')
                    text2 = request.args.get('text2')
                    text3 = request.args.get('text3')
                    scraper = cloudscraper.create_scraper()
                    url = 'https://textpro.me/80-s-retro-neon-text-effect-online-979.html'
                    gt = scraper.get(url)
                    be = bs(gt.text, 'html.parser')
                    token = be.find('input', attrs={'name': 'token'})['value']
                    build_server = be.find('input', attrs={'name': 'build_server'})['value']
                    build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
                    time.sleep(3)
                    radio = random.choice([i['value'] for i in be.findAll('input', attrs={'name': 'radio0[radio]'})])
                    radio1 = random.choice([i['value'] for i in be.findAll('input', attrs={'name': 'radio1[radio]'})])
                    frs = bs(scraper.post(url, data={'radio0[radio]': radio, 'radio1[radio]': radio1, u'text[]': [u'%s' % text1,u'%s' % text2,u'%s' % text3], 'submit': 'Go', 'token': token, 'build_server': build_server, 'build_server_id': build_server_id }).text, 'html.parser')
                    fv = frs.find('div', id='form_value').text
                    js = json.loads(fv)
                    p = scraper.post('https://textpro.me/effect/create-image', data={'id': '979', 'radio0[radio]': radio, 'radio1[radio]': radio1, u'text[]': [u'%s' % text1,u'%s' % text2,u'%s' % text3], 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
                    result = build_server+p['image']
                    r = scraper.get(result)
                    with open('img/RetroNeon.jpg', 'wb') as f:
                        f.write(r.content)
                    return send_file('img/RetroNeon.jpg')
                except Exception as e:
                    print('Error : %s ' % e)
                    return {
                        'status': False,
                        'error': 'Terjadi kesalahan'
                    }
            else:
                return {
                    'status': False,
                    'msg': 'Masukin param text3!'
                }
        else:
            return {
                'status': False,
                'msg': 'Masukin param text2'
            }
    else:
        return {
            'status': False,
            'msg': 'Masukin param text1'
        }

@app.route('/api/phblogo', methods=['GET','POST'])
def phblogo():
    if request.args.get('text1'):
        if request.args.get('text2'):
            try:
                text1 = request.args.get('text1')
                text2 = request.args.get('text2')
                scraper = cloudscraper.create_scraper()
                url = 'https://textpro.me/pornhub-style-logo-online-generator-free-977.html'
                gt = scraper.get(url)
                be = bs(gt.text, 'html.parser')
                token = be.find('input', attrs={'name': 'token'})['value']
                build_server = be.find('input', attrs={'name': 'build_server'})['value']
                build_server_id = be.find('input', attrs={'name': 'build_server_id'})['value']
                time.sleep(3)
                frs = bs(scraper.post(url, data={u'text[]': [u'%s' % text1,u'%s' % text2], 'submit': 'Go', 'token': token, 'build_server': build_server, 'build_server_id': build_server_id }).text, 'html.parser')
                fv = frs.find('div', id='form_value').text
                js = json.loads(fv)
                p = scraper.post('https://textpro.me/effect/create-image', data={'id': '977', u'text[]': [u'%s' % text1,u'%s' % text2], 'token': js['token'], 'build_server': build_server, 'build_server_id': build_server_id}).json()
                result = build_server+p['image']
                req = scraper.get(result)
                with open('img/pornhub.jpg', 'wb') as f:
                    f.write(req.content)
                crop.crop3('', 'pornhub')
                return send_file('img/pornhub.jpg')
            except Exception as e:
                print('Error : %s ' % e)
                return {
                    'status': False,
                    'result': '[❗] Terjadi kesalahan'
                    }
        else:
            return {
                'status': False,
                'result': 'Masukkan parameter text2!'
            }
    else:
        return {
            'status': False,
            'result': 'Masukkan parameter text1!'
        }

@app.route('/api/lightning', methods=['GET','POST'])
def lightning():
    if request.args.get('image_url'):
        try:
            scraper = cloudscraper.create_scraper()
            img_url = request.args.get('image_url')
            req_img = scraper.get(img_url)
            with open('img/lightning.jpg', 'wb') as f:
                f.write(req_img.content)
            post_img = scraper.post('https://photofunia.com/images?server=1', json={'server': '1'}, files={'image': open('img/burning_fire.jpg', 'rb')}).json()
            key = post_img['response']['key']
            width = post_img['response']['image']['highres']['width']
            height = post_img['response']['image']['highres']['height']
            reso = f'{width}.{height}'
            res = scraper.post('https://photofunia.com/categories/all_effects/lightning?server=1', allow_redirects=True, data={'current-category': 'all_effects', 'type': 'Year', 'year': '2021', 'image': key, 'image:crop': '0.0.'+reso})
            be = bs(scraper.get(res.url).content, 'html5lib')
            result = be.find('img', id='result-image')['src']
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': 'gagal!'
            }
    else:
        return{
            'result': 'masukkan parameter image_url!'
        }
@app.route('/api/lirik', methods=['GET','POST'])
def lirik():
    if request.args.get('q'):
        q = request.args.get('q')
        try:
            req = requests.get('https://scrap.terhambar.com/lirik?word='+q).json()
            return {
                'result': req['result']['lirik']
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter q! '
        }

@app.route('/api/random_pantun', methods=['GET','POST'])
def random_pantun():
    try:
        be = bs(requests.get('https://sharingkali.com/contoh-pantun/').text, 'html.parser')
        randoms = random.choice([i.find('p').text for i in be.findAll('blockquote')])
        return{
            'result': randoms
        }
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan!'
        }

@app.route('/api/tebakgambar', methods=['GET','POST'])
def tebakgambar():
    try:
        tebak = json.loads(open('tebakgambar.json').read())
        result = random.choice(tebak)
        return jsonify(result)
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan!'
        }

@app.route('/api/search_anime', methods=['GET','POST'])
def search_anime():
    if request.args.get('image_url'):
        image = request.args.get('image_url')
        req_img = get(image)
        with open('img/anime_search.jpg', 'wb') as f:
            f.write(req_img.content)
        return jsonify(post('https://api.trace.moe/search', files={'image': open('img/anime_search.jpg', 'rb')}).json())
    else:
        return{
            'result': 'masukkan parameter image_url!'
        }

@app.route('/api/jurnalotaku_search', methods=['GET','POST'])
def jurnal_otaku():
    if request.args.get('q'):
        q = request.args.get('q')
        try:
            be = bs(requests.get('http://jurnalotaku.com/?s='+q).text, 'html.parser')
            result = []
            for i in be.findAll('div', class_='article-inner-wrapper'):
                try:
                    meta = i.find('meta')
                    url = i.find('a')['href']
                    cvr = i.find('div', class_='cover size-a has-depth')
                    img = cvr.find('img')['src']
                    title = cvr.find('img')['alt']
                    category = i.find('a', class_='category box-category main-category').text
                    author = i.find('a', attrs={'rel': 'author'}).text
                    uploaded = i.find('span', class_='datetime').text
                    desc = i.find('div', class_='summary').text
                except Exception:
                    pass
                result.append({
                    'url': url,
                    'img': img,
                    'title': title,
                    'category': category,
                    'author': author,
                    'uploaded': uploaded,
                    'desc': desc.replace('\n', '')
                })
            return {
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter q!'
        }

@app.route('/api/jurnalotaku_lastest', methods=['GET','POST'])
def jurnalotaku_lastest():
    try:
        be = bs(requests.get('http://jurnalotaku.com/').text, 'html.parser')
        result = []
        for i in be.findAll('div', class_='article-wrapper article-tb'):
            try:
                url = i.find('a')['href']
                cvr = i.find('div', class_='cover size-a has-depth')
                img = cvr.find('img')['src']
                title = cvr.find('img')['alt']
                category = i.find('a', class_='category box-category main-category').text
                uploaded = i.find('span', class_='datetime').text
                result.append({
                    'url': url,
                    'img': img,
                    'title': title,
                    'category': category,
                    'uploaded': uploaded
                })
            except Exception:
                pass
        return {
            'result': result
        }
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan!'
        }

@app.route('/api/kurs', methods=['GET','POST'])
def kurs():
    try:
        be = bs(requests.get('http://kurs.dollar.web.id/').text, 'html.parser').find('table')
        res = []
        for i in be.findAll('tr')[1:]:
        	fa = i.findAll('td')
        	kurs = fa[0].text
        	tengah = fa[1].text
        	jual = fa[2].text
        	beli = fa[3].text
        	res.append({
        		'kurs': kurs,
        		'tengah': tengah,
        		'jual': jual,
        		'beli': beli
        	})
        return{
            'result': res
        }
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan!'
        }

@app.route('/api/bioskop', methods=['GET','POST'])
def bioskop():
    if request.args.get('kota'):
        q = request.args.get('kota')
        try:
            be = bs(requests.get('https://jadwalnonton.com/bioskop/di-'+q).text, 'html.parser').find('div', class_='row clearfix thlist')
            result = []
            for i in be.findAll('div', class_='item theater'):
                url = i.find('a')['href']
                bes = bs(requests.get(url).text, 'html.parser')
                title = bes.find('h1').text
                alamat = bes.find('div', class_='mtom10').text.replace('Show map', '').replace('\n', '')
                star = len(bes.findAll('i', class_='icon-star'))
                img = bes.findAll('img')[1]['src']
                result.append({
                    'url': url,
                    'title': title,
                    'alamat': alamat,
                    'bintang': star,
                    'img': img
                })
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter kota!'
        }

@app.route('/api/cuaca', methods=['GET','POST'])
def cuaca():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            print(q)
            r = cloudscraper.create_scraper()
            url = f'https://rest.farzain.com/api/cuaca.php?id={q}&apikey='
            weather = r.get(f'{url}{apiKey}').json()
            print(weather)
            if weather['respon']['deskripsi'] == 'null' or weather['respon']['deskripsi'] == None:
                return {
                    'status': 404,
                    'error': '[❗] Gagal mengambil informasi cuaca, mungkin tempat tidak terdaftar/salah!'
                }
            else:
                return {
                    'status': 200,
                    'result': {
                        'tempat': weather['respon']['tempat'],
                        'cuaca': weather['respon']['cuaca'],
                        'desk': weather['respon']['deskripsi'],
                        'suhu': weather['respon']['suhu'],
                        'kelembapan': weather['respon']['kelembapan'],
                        'udara': weather['respon']['udara'],
                        'angin': weather['respon']['angin']
                    }
                }
        except Exception as e:
            print('Error : %s' % e)
            return {
                'status': False,
                'msg': '[❗] Gagal mengambil informasi cuaca, mungkin tempat tidak terdaftar/salah!'
            }
    else:
        return {
            'status': False,
            'msg': '[!] Masukkan parameter q'
        }

@app.route('/api/hilih', methods=['GET','POST'])
def hilih():
    if request.args.get('text'):
        text = request.args.get('text')
        return{
            'result': re.sub(r'([@#][\w-]+)|[aiueoAIUEO]', 'i', text)
        }
    else:
        return{
            'result': 'masukkan parameter text!'
        }

@app.route('/api/ninja_name', methods=['GET','POST'])
def ninja_name():
    if request.args.get('name'):
        name = request.args.get('name')
        try:
            be = bs(requests.post('http://ninjaname.net/ninja_name.php', data={'real_name': name}).text, 'html.parser').findAll('td', id='brown')[1].text
            return{
                'your_name': name,
                'result': be
            }
        except Exception as e:
            print(e)
            return{
                'result': 'terjadi kesalahan!'
            }
    else:
        return{
            'result': 'masukkan parameter name!'
        }

@app.route('/api/baca-komik', methods=['GET','POST'])
def baca_komik():
    if request.args.get('q'):
        q = request.args.get('q')
        try:
            bes = bs(requests.get('https://bacakomik.co/?s='+q).text, 'html.parser')
            url = random.choice([i.find('a')['href'] for i in bes.findAll('div', class_='animposx')])
            be = bs(requests.get(url).text, 'html.parser')
            title = be.find('h1', class_='entry-title').text
            th = be.find('div', class_='thumb')
            thumb = th.find('img')['data-src']
            spe = be.find('div', class_='spe')
            sn = be.find('div', class_='entry-content entry-content-single')
            sinopsis = sn.find('p').text
            info = [i.text for i in spe.findAll('span')]
            spoiler = [i.find('img')['data-lazy-src'] for i in be.findAll('div', class_='spoiler-img')]
            print(info)
            return {
                'title': title,
                'thumb': thumb,
                'synopsis': sinopsis,
                'spoiler': spoiler,
                'info': info
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return{
            'result': 'masukkan parameter q!'
        }

@app.route('/api/tribun', methods=['GET','POST'])
def tribun():
    try:
        be = bs(get('https://www.tribunnews.com/news').text, 'html.parser').find('div', class_='fl w502')
        result = []
        for i in be.findAll('li', class_='p1520 art-list pos_rel'):
            link = i.find('a')['href']
            title = i.find('a')['title']
            desk = i.find('div', class_='grey2 pt5 f13 ln18 txt-oev-3').text
            di_unggah = i.find('time', class_='foot timeago').text
            img = i.find('img', class_='shou2 bgwhite')['src']
            result.append({
                'url': link,
                'title': title,
                'deskripsi': desk,
                'image': img,
                'di_unggah': di_unggah
            })
        return {
            'result': result
        }
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan!'
        }

@app.route('/api/liputan6', methods=['GET','POST'])
def liputan6():
    try:
        be = bs(get('https://www.liputan6.com/news').text, 'html.parser').find('article', class_='main')
        result = []
        for i in be.findAll('article', class_='articles--iridescent-list--item articles--iridescent-list--text-item'):
            title = i.find('h4', class_='articles--iridescent-list--text-item__title').text
            desk = i.find('div', class_='articles--iridescent-list--text-item__summary articles--iridescent-list--text-item__summary-seo').text
            di_unggah = i.find('time', class_='articles--iridescent-list--text-item__time timeago').text
            pic = i.find('picture', class_='articles--iridescent-list--text-item__figure-image')
            img = pic.find('img')['data-src']
            result.append({
                'title': title,
                'description': desk,
                'uploaded': di_unggah,
                'img': img
            })
        return {
            'result': result
        }
    except Exception as e:
        print(e)
        return{
            'result': 'terjadi kesalahan!'
        }

@app.route('/api/apk-pure', methods=['GET','POST'])
def apk_pure():
    if request.args.get('q'):
        q = request.args.get('q')
        try:
            be = bs(requests.get('https://m.apkpure.com/id/search?q='+q).text, 'html.parser').find('ul', id="search-res")
            result = []
            for i in be.findAll('li'):
                try:
                    url= 'https://m.apkpure.com'+i.find('a')['href']
                    title = i.find('img')['title']
                    img = i.find('img')['data-original']
                    star = i.find('span', class_='star').text
                    score = i.find('span', class_='score')['title']
                    bes = bs(requests.get(url).text, 'html.parser')
                    down = bes.find('div', class_='down')
                    dl = 'https://m.apkpure.com'+down.find('a')['href']
                    version = bes.find('span', attrs={'itemprop': 'version'}).text
                    filesize = bes.find('span', class_='fsize').text
                    result.append({
                        'url': url,
                        'img': img, 
                        'star': star,
                        'score': score,
                        'download_link': dl,
                        'filesize': filesize,
                        'version': version
                    })
                except Exception as e:
                    pass
            return{
                'result': result
            }
        except Exception as e:
            print(e)
            return{
                'result': q+' tidak di temukan!'
            }
    else:
        return jsonify("MASUKKAN PARAMETER q!")

#BELLOW
@app.route('/api', methods=['GET','POST'])
def api():
    return render_template('api_s.html')

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/google', methods=['GET','POST'])
def google():
    return render_template('google.html')

@app.errorhandler(404)
def error(e):
    return render_template('error_req.html'), 404

if __name__ == '__main__':
    try:
        os.environ['deployed']
        print('STATUS : APP DEPLOYED')
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')),debug=False)
    except KeyError:
        print('STATUS : APP NOT DEPLOYED')
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')),debug=True)
