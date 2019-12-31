import scrapy
import requests as re
from bs4 import BeautifulSoup as bs
import json
import unicodedata
import os
import datetime

from airvisual.items import Weather

def clean(text):
    return unicodedata.normalize('NFKD', ' '.join(text.replace('\n', '').split()))

       

class AirvisualSpiderSpider(scrapy.Spider):
    name = 'airvisual_spider'
    allowed_domains = ['airvisual.com']
    
    start_urls = []
    #DOWNLOAD XML FILE 46 MB, TAKING TOO LONG TOME
    '''
    url = 'https://www.airvisual.com/sitemap-places-en-1.xml'
    source = re.get(url)
    soup = bs(source.text, "html.parser")
    aaa=soup.find_all('loc')
    for i in range(len(aaa)):
        if 'indonesia' in str(aaa[i]):
            print(str(i),'',str(len(aaa)))
            start_urls.append(str(aaa[i]).replace('</loc>','').replace('<loc>',''))
    '''
    
    
    
    with open('D:/magang2.csv') as f:
        urls = f.readlines()
    for ur in range(len(urls)):
        urls[ur] = urls[ur].replace('\n','')
    #start_urls=urls[0:100]

    
    
    
    
    
    '''   
    if not os.path.exists('C:\\Dev\\Mgg\\airvisual\\airvisual\\spiders\\'+today):
        os.makedirs('C:\\Dev\\Mgg\\airvisual\\airvisual\\spiders\\'+today)
    '''
    
    
    
    def parse(self,response):
        query = response.url.split('/')[-1]
        yield scrapy.Request(
                url='https://website-api.airvisual.com/v1/search?q=*'+query.replace('-','%20')+'*&units.temperature=celsius&units.distance=kilometer&AQI=US&language=id',
                callback=self.parse_query_search
        )
    
    def parse_query_search(self,response):
        res = json.loads(response.body)
        city_id=res['cities'][0]['id']
        yield scrapy.Request(
                url = 'https://website-api.airvisual.com/v1/cities/'+city_id+'?units.temperature=celsius&units.distance=kilometer&AQI=US&language=id',
                callback=self.parse_data_api
        )
    
    def parse_data_api(self,response):
        data = Weather()
        res = json.loads(response.body)
        data['url'] = response.url
        data['city_id'] = res['id']
        data['city_name'] = res['name']
        data['province'] = res['breadcrumbs'][1]['label']
        data['country'] = res['country']
        data['aqi'] = res['current']['aqi']
        data['aqi_concentration'] = res['current']['concentration']
        data['timezone'] = res['timezone']
        data['city_type'] = res['type']
        data['main_pollutant'] = res['current']['mainPollutant']
        data['condition'] = res['current']['condition']
        data['humidity'] = res['current']['humidity']
        data['pressure'] = res['current']['pressure']
        data['wind_speed'] = res['current']['wind']['speed']
        data['wind_direction'] = res['current']['wind']['direction']
        data['temperature'] = res['current']['temperature']
        data['latitude'] = res['coordinates']['latitude']
        data['longitude'] = res['coordinates']['longitude']
        data['exercise_value'] = res['recommendations']['pollution']['exercice']['value']
        data['exercise_desc'] = res['recommendations']['pollution']['exercice']['text']
        data['windows_value'] = res['recommendations']['pollution']['windows']['value']
        data['windows_desc'] = res['recommendations']['pollution']['windows']['text']

        yield data










