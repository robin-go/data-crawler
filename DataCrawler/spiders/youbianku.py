# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from DataCrawler.items import PostcodeItem


class YoubiankuSpider(CrawlSpider):
    name = 'youbianku'
    allowed_domains = ['www.youbianku.com']
    start_urls = ['https://www.youbianku.com/三位索引']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.youbianku.com/\d{3}$'), follow=True),
        Rule(LinkExtractor(allow=r'https://www.youbianku.com/\d{6}$'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = PostcodeItem()

        # 地址
        address_list = response.xpath("//div[@id='mw-content-text']/p[5]/a/text()").extract()

        # 邮编
        code = response.url[-6:]

        if address_list:
            for address in address_list:
                if not address.isdigit():
                    item['address'] = address
                    item['code'] = code
                    yield item
                else:
                    pass
