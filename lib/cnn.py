from bs4 import BeautifulSoup
from requests import get
import json

def query(url):
    datas = get(url)
    soup = BeautifulSoup(datas.text, 'html.parser')
    tag = soup.find_all('article')
    data = []
    for i in tag:
        try:
            title = i.find('h2').text
            link = i.find('a').get('href')
            gambar = i.find('img').get('src')
            tipe = i.find('span', class_="kanal").text
            waktu = i.find('span', class_="date").text
            data.append({
                "judul": title,
                "link": link,
                "poster": gambar,
                "tipe": tipe,
                "waktu": waktu
            })
        except:
            pass

    return data

class Script:

    def index():
        return query('https://www.cnnindonesia.com/')

    def nasional():
        return query('https://www.cnnindonesia.com/nasional')
    def internasional():
        return query('https://www.cnnindonesia.com/internasional')
    def ekonomi():
        return query('https://www.cnnindonesia.com/ekonomi')
    def olahraga():
        return query('https://www.cnnindonesia.com/olahraga')

    def teknologi():
        return query('https://www.cnnindonesia.com/teknologi')

    def hiburan():
        return query('https://www.cnnindonesia.com/hiburan')

    def social():
        return query('https://www.cnnindonesia.com/gaya-hidup')

    def detail(url):
        data = []
        try:
            req = get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            tag = soup.find('div', class_="detail_text")
            gambar = soup.find('div', class_='media_artikel').find('img').get('src')
            judul = soup.find('h1', class_='title').text
            body = tag.text
            data.append({
                "judul": judul,
                "poster": gambar,
                "body": body,
            })
        except:
            data.append({
                "message": "network error",
            })

        return data

    def search(q):
        return query('https://www.cnnindonesia.com/search/?query=' + q)
