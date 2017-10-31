# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PornItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PornMovieItem(scrapy.Item):
    # 视频源地址
    file_urls = scrapy.Field()
    # 视频标题
    file_name = scrapy.Field()
    files = scrapy.Field()
