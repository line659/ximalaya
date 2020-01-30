# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XimalayaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    audio_id = scrapy.Field()
    audio_src = scrapy.Field()
    audio_title = scrapy.Field()
    audio_files = scrapy.Field()
    audio_detail = scrapy.Field()
    audio_fm_title = scrapy.Field()