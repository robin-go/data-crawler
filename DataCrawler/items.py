# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 菜谱
class RecipeItem(scrapy.Item):

    # 菜名
    title = scrapy.Field()
    # 用料
    materials = scrapy.Field()
    # 做法
    steps = scrapy.Field()
    # 评分
    rank = scrapy.Field()
    # url
    url = scrapy.Field()


# 笑话
class JokeItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 内容
    content = scrapy.Field()


# 邮编
class PostcodeItem(scrapy.Item):
    # 地址
    address = scrapy.Field()
    # 邮编
    code = scrapy.Field()
