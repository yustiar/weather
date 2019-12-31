import scrapy
import requests as re
from bs4 import BeautifulSoup as bs
import json
import unicodedata
import datetime
import os

from accuweather.items import Weather



def clean(text):
    return unicodedata.normalize('NFKD', ' '.join(text.replace('\n', '').split()))


class AccuweatherSpiderSpider(scrapy.Spider):
    name = 'accuweather_spider'
    allowed_domains = ['accuweather.com']
    start_urls = ['https://www.accuweather.com/en/browse-locations/asi/id']
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    
    '''
    today = datetime.datetime.today().strftime('%d-%m-%Y')
    f = open('C:\\Dev\\Mgg\\accuweather\\batch.bat', 'w')
    f.write('cd C:\\Dev\\Mgg\\accuweather\\accuweather\\spiders'+'\n'
            'scrapy crawl accuweather_spider -t  csv -o  - > "'+'data_'+today+'.csv"'+'\n'
            'xcopy "'+'data_'+today+'.csv"'+' ' +'"C:\\Users\\ASUS\\Desktop\\New folder\\accu_weather" /s/h/e/k/f/c'+'\n'

            )

    f.close()
    '''
    '''
    if not os.path.exists(today):
        os.makedirs(today)
    '''
    
    def parse(self, response):
        json1 = response.xpath('head').get().replace('\t','').replace('\n','')
        json2 = json1.split('var browseLocationsAreas = ')[1]
        json3 = json2.split('var locales =')[0].replace(';','')
        json_obj = json.loads(json3)
        prov = json_obj['locs']
        for pr in prov:
            yield scrapy.Request(
                url='https://www.accuweather.com/en/browse-locations/asi/id/'+pr['id'], 
                headers=self.headers,
                callback=self.parse_area
            )
    def parse_area(self,response):
        json1 = response.xpath('head').get().replace('\t','').replace('\n','')
        json2 = json1.split('var browseLocationsAreas = ')[1]
        json3 = json2.split('var locales =')[0].replace(';','')
        json_obj = json.loads(json3)
        area = json_obj['locs']
        for ar in area:
            yield scrapy.Request(
                    url='https://www.accuweather.com/en/id/'+ar['englishName'].replace(' ','-')+'/'+ar['id']+'/current-weather/'+ar['id'],
                    headers=self.headers,
                    callback=self.parse_data
                )
    def parse_data(self, response):
        data=Weather()
        data['url'] = response.url
        location = clean(response.xpath('//span[@class="recent-location-display-label location-label"]/h1/text()').get())
        data['areaname'] = location.split(', ')[0]
        data['area_id'] = response.url.split('/')[-1]
        data['province'] = location.split(', ')[1]
        
        topleft_container = response.xpath('//div[@class="current-conditions-card content-module"]')
        data['timestamp'] = clean(topleft_container.xpath('//p[@class="module-header sub date"]/text()').get())
        data['condition'] = clean(topleft_container.xpath('//div[@class="phrase"]/text()').get())
        data['temperature'] = clean(topleft_container.xpath('//p[@class="value"]/text()').get())
        
        topright_container = topleft_container.xpath('//div[@class="accordion-item-content accordion-item-content"]//p/text()').getall()
        for topright in topright_container:
            if 'uv index' in topright.lower():
                data['uv_index'] = clean(topright).split(':')[-1].strip()
            elif 'wind:' in topright.lower():
                data['wind'] = clean(topright).split(':')[-1].strip()
            elif 'wind gusts' in topright.lower():
                data['wind_gust'] = clean(topright).split(':')[-1].strip()
            elif 'humidity' in topright.lower():
                data['humidity'] = clean(topright).split(':')[-1].strip()
            elif 'dew point' in topright.lower():
                data['dew_point'] = clean(topright).split(':')[-1].strip()
            elif 'pressure' in topright.lower():
                data['pressure'] = clean(topright).split(':')[-1].strip()
            elif 'cloud cover' in topright.lower():
                data['cloud_cover'] = clean(topright).split(':')[-1].strip()
            elif 'visibility' in topright.lower():
                data['visibility'] = clean(topright).split(':')[-1].strip()
            elif 'ceiling' in topright.lower():
                data['ceiling'] = clean(topright).split(':')[-1].strip()
                
            
        yield data
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        