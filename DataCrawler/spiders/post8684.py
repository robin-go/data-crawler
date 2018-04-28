# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from DataCrawler.items import PostcodeItem


class Post8684Spider(CrawlSpider):
    name = 'post8684'
    allowed_domains = ['post.8684.cn']
    start_urls = ['http://post.8684.cn/']

    rules = (
        Rule(LinkExtractor(allow=r's\d{1,2}\.htm'), follow=True),
        Rule(LinkExtractor(allow=r'c\d{1,3}\.htm'), follow=True),
        Rule(LinkExtractor(allow=r'a\d{1,4}_1\.htm'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        """爬取区县一级的邮编"""

        item = PostcodeItem()

        # 地址
        address = response.xpath("//div[@class='list-con']/a/text()").extract()
        address = ''.join(address)

        # 邮编
        code = response.xpath("//div[@class='list-con']/span[2]/text()").extract_first()

        item['address'] = address
        item['code'] = code

        yield item
