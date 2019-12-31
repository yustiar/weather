import scrapy


class Weather(scrapy.Item):
    url = scrapy.Field()
    areaname = scrapy.Field()
    province = scrapy.Field()
    area_id = scrapy.Field()
    timestamp = scrapy.Field()
    condition = scrapy.Field()
    temperature = scrapy.Field()
    uv_index = scrapy.Field()
    wind = scrapy.Field()
    wind_gust = scrapy.Field()
    humidity = scrapy.Field()
    dew_point = scrapy.Field()
    pressure = scrapy.Field()
    cloud_cover = scrapy.Field()
    visibility = scrapy.Field()
    ceiling = scrapy.Field()







