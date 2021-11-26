from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

client = MongoClient()
db = client['news']
db.news.drop
news = db.news


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.1.932 Yowser/2.5 Safari/537.36'}
url = 'https://lenta.ru'
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
source = 'Лента.ру ' + url
names = dom.xpath("//div[@class='b-yellow-box__wrap']//a[1]/text()")
links = dom.xpath("////div[@class='b-yellow-box__wrap']//a[1]/@href")
for number, link in enumerate(links):
    new_link = url + link
    links[number] = new_link
dates = []
for link in links:
    response = requests.get(link, headers=header)
    dom = html.fromstring(response.text)
    dates.append(dom.xpath("//time[@class='g-date']/text()"))

news_list = []
for i in range(len(names)):
    news_data = {}
    news_data['name'] = names[i]
    news_data['link'] = links[i]
    news_data['date'] = dates[i]
    news_data['source'] = source
    news_list.append(news_data)
    news.insert_one(news_data)


# pprint(news_list)
for new in news.find({}):
    pprint(new)

# pprint(names)
# pprint(links)
# pprint(dates)