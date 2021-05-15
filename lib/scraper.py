from cloudscraper import create_scraper
from bs4 import BeautifulSoup as bs
import time, random, json
r = create_scraper()

class scr:
    def pornhub(self, text, text2):
        '''
        text = white text
        text2 = black text
        '''
        try:
            url = 'https://textpro.me/pornhub-style-logo-online-generator-free-977.html'
            token = bs(r.get(url).text, 'html.parser').find('input', id='token')['value']
            data = {u'text[]': [u'%s' % text,u'%s' % text2], 'submit': 'Go', 'token': token}
            result = 'https://textpro.me'+(bs(r.post(url, data).text, 'html.parser').find('div', class_='thumbnail').img['src'])
            return result
        except Exception as e:
            print(e)
            return {
                'error': 'Emror'
            }
    def wolf(self, text, text2):
        '''
        text = white text
        text2 = black text
        '''
        try:
            url = 'https://textpro.me/create-wolf-logo-galaxy-online-936.html'
            token = bs(r.get(url).text, 'html.parser').find('input', id='token')['value']
            data = {u'text[]': [u'%s' % text,u'%s' % text2], 'submit': 'Go', 'token': token}
            result = 'https://textpro.me'+(bs(r.post(url, data).text, 'html.parser').find('div', class_='thumbnail').img['src'])
            return result
        except Exception as e:
            print(e)
            return {
                'error': 'Emror'
            }

    def glitch(self, text, text2):
        '''
        text = white text
        text2 = black text
        '''
        try:
            url = 'https://photooxy.com/logo-and-text-effects/make-tik-tok-text-effect-375.html'
            #token = bs(r.get(url).text, 'html.parser').find('input', id='token')['value']
            data = {'text_1': text, 'text_2': text2, 'submit': 'Go', 'login': 'OK'}
            result = 'https://photooxy.com'+(bs(r.post(url, data).text, 'html.parser').find('div', class_='thumbnail').img['src'])
            return result
        except Exception as e:
            print(e)
            return {
                'error': 'Emror'
            }

    def retro_neon(self, text, text2, text3):
        '''
        text = white text
        text2 = black text
        '''
        try:
            bg = [
                'e03db829-4f8a-4870-83ff-1d1f0b1bc9f5',
                '21fb6cff-6169-4c44-8b0b-8b3c38b8ddd1',
                '7a16d53f-7115-46d6-a3cc-9dc84bdbae90',
                '8adb4d95-6fe8-4ea9-a877-3ca01aa59e67',
                '7be0c4a2-9070-400d-81c2-6c22cb906bf2',
                '2a108ef8-3bac-4331-bc8e-a0ab12594863'
            ]
            bege = random.choice(bg)
            gaya = [
                'f6e0ed56-7f2b-40c1-8c1e-d6bbbbb27529',
                'cc76567f-396b-44af-8340-6057fd447388',
                '669c3524-593c-47db-bde2-a0a5ace91064',
                '46f21738-3f19-4195-a2fe-05ef22300984'
            ]
            style = random.choice(gaya)
            url = 'https://textpro.me/80-s-retro-neon-text-effect-online-979.html'
            token = bs(r.get(url).text, 'html.parser').find('input', id='token')['value']
            data = {'radio0[radio]': bege, 'radio1[radio]': style, u'text[]': [u'%s' % text,u'%s' % text2,u'%s' % text3], 'submit': 'Go', 'token': token}
            result = 'https://textpro.me'+(bs(r.post(url, data).text, 'html.parser').find('div', class_='thumbnail').img['src'])
            return result
        except Exception as e:
            print(e)
            return {
                'error': 'Emror'
            }

    def black_pink(self, text):
        '''
        text = text
        '''
        try:
            url = 'https://textpro.me/create-blackpink-logo-style-online-1001.html'
            token = bs(r.get(url).text, 'html.parser').find('input', id='token')['value']
            data = {'text[]': text, 'submit': 'Go', 'token': token}
            result = 'https://textpro.me'+(bs(r.post(url, data).text, 'html.parser').find('div', class_='thumbnail').img['src'])
            return result
        except Exception as e:
            print(e)
            return {
                'error': 'Emror'
            }
    def text3d(self, text):
        '''
        text = text
        '''
        try:
            url = 'https://textpro.me/3d-gradient-text-effect-online-free-1002.html'
            token = bs(r.get(url).text, 'html.parser').find('input', id='token')['value']
            data = {'text[]': text, 'submit': 'Go', 'token': token}
            result = 'https://textpro.me'+bs(r.post(url, data).text, 'html.parser').find('div', class_='thumbnail').img['src']
            return result
        except Exception as e:
            print(e)
            return {
                'error': 'Emror'
            }
    def thunder(self, text):
        '''
        text = text
        '''
        try:
            url = 'https://textpro.me/thunder-text-effect-online-881.html'
            token = bs(r.get(url).text, 'html.parser').find('input', id='token')['value']
            data = {'text[]': text, 'submit': 'Go', 'token': token}
            result = 'https://textpro.me'+(bs(r.post(url, data).text, 'html.parser').find('div', class_='thumbnail').img['src'])
            return result
        except Exception as e:
            print(e)
            return {
                'error': 'Emror'
            }
    def neon_light(self, text):
        '''
        text = text
        '''
        try:
            url = 'https://textpro.me/create-a-futuristic-technology-neon-light-text-effect-1006.html'
            token = bs(r.get(url).text, 'html.parser').find('input', id='token')['value']
            data = {'text[]': text, 'submit': 'Go', 'token': token}
            result = (bs(r.post(url, data).text, 'html.parser'))
            return result
        except Exception as e:
            print(e)
            return {
                'error': 'Emror'
            }
            
    def ytdl(self, url):
        link = 'https://y2mate.guru/api/convert'
        data = {'url': url}
        result = r.post(link, data).json()
        return result

    def fbdl(self, url):
        link = 'https://fbdown.net/download.php'
        data = {'URLz': url}
        res = (bs(r.post(link, data).text, 'html5lib').find('div', class_='col-md-4 col-md-offset-2'))
        for a in res.find_all('a', href=True):
            result = a['href']
        return result
    
    def ytmp3(self, url):
        link = 'https://www.clickmp3.com/en'
        data = {'url': url}
        res = (bs(r.post(link, data).text, 'html5lib'))
        print(res)
    
    def tiktok(self, url):
        link = 'https://freedownloadvideo.net/system/action.php'
        token = bs(r.get('https://freedownloadvideo.net/tiktok-video-downloader#url='+url).text, 'html.parser').find('input', attrs={'name':'token'})['value']
        data = {'url':url, 'token': token}
        res = r.post(link, data).json()
        title = res['title']
        thumbnail = res['thumbnail']
        duration = res['duration']
        source = res['source']
        links = res['links']
        video_url = url
        return {
            'title': title,
            'thumbnail': thumbnail,
            'duration': duration,
            'source': source,
            'result': links,
            'video_url': video_url
        }
    def igdl(self, url):
        link = 'https://bigbangram.com/ing-post-api.php'
        data = {'url': url, 'download': 'post'}
        p = r.post(link, data) 
        print(p.content)

    def igstalk(self, username):
        url = 'https://www.instagram.com/'+username+'/?__a=1'
        kukie = bs(r.get('https://pastebin.com/v7JikhK8').text, 'html.parser')
        kuki = kukie.find('textarea', class_='textarea').text
        print(kuki)
        header = {'cookie': kuki}
        p = r.get(url, headers=header).json()
        return p

    def tiktok_wm(self, url):
        j = bs(r.get('https://tiktokdownload.online/id').text, 'html.parser').find('body')
        #js = json.loads(j)
        print(j)
        #token = js['token']
        #be = bs(r.post('https://tiktokdownload.online/results', data={'id': url, 'token': token, '_method': 'POST'}).text, 'html.parser')
        #res = be.find('a', class_='btn btn-primary download_link with_watermark')['href']    
        return res
    
    def tiktok_audio(self, url):
        bes = bs(r.get('https://ssstik.io/id').text, 'html.parser')
        hx = bes.find('form', class_='pure-form pure-g hide-after-request')['data-hx-post']
        link = 'https://ssstik.io'+hx
        tts = bes.find('form', class_='pure-form pure-g hide-after-request')['include-vals']
        be = bs(r.post(link, data={'id': url, 'locale': 'id'}).text, 'html.parser')
        res = be.find('a', class_='pure-button pure-button-primary is-center u-bl dl-button download_link music')['href']
        return 'https://ssstik.io/'+res

    def igs(self, username):
        """
        username = username ig
        """
        link1 = 'https://www.storysaver.net/'
        url = 'https://www.storysaver.net/storyProcesst.php'
        #p = (bs(r.get(link1).text(), 'html5lib').find('input', id='rptid'))
        data = {'text_username': username}
        p = r.post(url, data).text
        print(p)
    
    def pastebin(self, title, text):
        url = 'https://pastebin.com/api/api_post.php'
        data = {'api_dev_key ': 'p6LAc_zuhhZZdQIPXmGQGiC-UeNuYx6x', 'api_paste_code ': text, 'api_paste_private': '0', 'api_paste_name': title, 'api_paste_expire_date': 'N'}
        res = r.post(url, data).content
        print(res)

    def ssweb(self, url):
        """
        url = link web
        """
        link = 'https://www.screenshotmachine.com/capture.php'
        res = r.post(link, data={'url': url, 'device': 'desktop', 'cacheLimit': 0}, headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}).json()
        print('https://www.screenshotmachine.com/'+res['link']+'&attachment')

    def fake_iden(self):
        p = bs(r.post('https://datafakegenerator.com/generador.php', data={'pais': 'United Estates', 'sexo': 'Female', 'de': 18, 'hasta': 60}).text, 'html.parser')
        q = p.findAll('div', class_='6u 12u(mobile)')
        name = q[7].text
        gender = q[9].text
        age = q[11].text
        date = q[13].text
        occupation = q[15].text
        address = q[17].text
        zip_code = q[19].text
        state = q[21].text
        country = q[23].text
        email = q[25].text
        password = q[27].text
        phone = q[29].text
        card = q[31].text
        code = q[33].text
        date_2 = q[35].text
        pin = q[37].text
        height = q[39].text
        weight = q[41].text
        blood = q[43].text
        status = q[45].text
        return {
            'name': name.replace('\n', ''),
            'gender': gender.replace('\n', ''),
            'age': age.replace('\n', ''),
            'birtday': date.replace('\n', ''),
            'occupation': occupation.replace('\n', ''),
            'address': address.replace('\n', ''),
            'zip_code': zip_code.replace('\n', ''),
            'state': state.replace('\n', ''),
            'country': country.replace('\n', ''),
            'email': email.replace('\n', ''),
            'password': password.replace('\n', ''),
            'phone': phone.replace('\n', ''),
            'card': card.replace('\n', ''),
            'code': code.replace('\n', ''),
            'date': date_2.replace('\n', ''),
            'pin_code': pin.replace('\n', ''),
            'weight': weight.replace('\n', ''),
            'height': height.replace('\n', ''),
            'blood_type': blood.replace('\n', ''),
            'status': status.replace('\n', '')
        }

    def wattpad_search(self, q):        
        p = bs(r.get('https://www.wattpad.com/search/'+q).text, 'html.parser')
        res = []
        for i in p.findAll('div', class_='results-story-item'):
            title = i.find('h5', class_='story-title-heading').text
            reads = i.find('small', class_='reads').text
            votes = i.find('small', class_='votes').text
            desc = i.find('p').text
            thumb = i.find('img')['src']
            url = 'https://www.wattpad.com'+i.find('a')['href']
            res.append({
                'title': title,
                'reads': reads,
                'votes': votes,
                'description': desc,
                'url': url,
                'thumb': thumb
            })
        return res