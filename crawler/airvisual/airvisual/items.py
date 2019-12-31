import scrapy


class Weather(scrapy.Item):
   url = scrapy.Field()
   city_id = scrapy.Field()
   city_name = scrapy.Field()
   province = scrapy.Field()
   country = scrapy.Field()
   aqi = scrapy.Field()
   aqi_concentration = scrapy.Field()
   timezone = scrapy.Field()
   city_type = scrapy.Field()
   main_pollutant = scrapy.Field()
   condition = scrapy.Field()
   humidity = scrapy.Field()
   pressure = scrapy.Field()
   wind_speed = scrapy.Field()
   wind_direction = scrapy.Field()
   temperature = scrapy.Field()
   latitude = scrapy.Field()
   longitude = scrapy.Field()
   exercise_value = scrapy.Field()
   exercise_desc = scrapy.Field()
   windows_value = scrapy.Field()
   windows_desc = scrapy.Field()
   
   
   
   
   