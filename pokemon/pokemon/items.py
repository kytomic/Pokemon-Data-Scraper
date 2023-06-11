# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PokemonItem(scrapy.Item):
    # define the fields for your item here like:

    img_url = scrapy.Field()
    name = scrapy.Field()
    japanese = scrapy.Field()
    types = scrapy.Field()
    species = scrapy.Field()
    ability = scrapy.Field()
    evoform = scrapy.Field()
    evointo = scrapy.Field()
    hp = scrapy.Field()
    attack = scrapy.Field()
    defense = scrapy.Field()
    sp_atk = scrapy.Field()
    sp_def = scrapy.Field()
    speed = scrapy.Field()
    total = scrapy.Field()
    
