# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyStatsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    省份 = scrapy.Field()
    城市 = scrapy.Field()
    市辖区县 = scrapy.Field()
    城镇 = scrapy.Field()
    城市代码 = scrapy.Field()
    市辖区县代码 = scrapy.Field()
    城镇代码 = scrapy.Field()
    城市2 = scrapy.Field()
    社区 = scrapy.Field()
    社区代码 = scrapy.Field()

