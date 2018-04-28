# -*- coding: utf-8 -*-
from w3lib.html import remove_tags
import scrapy
from scrapy.http import Request

from DataCrawler.items import JokeItem

class QiushibaikeSpider(scrapy.Spider):
    name = 'pengfu'
    allowed_domains = ['pengfu.com']
    start_urls = ['https://www.pengfu.com/xiaohua_1.html']

    page = 1
    url0 = 'https://www.pengfu.com/'

    def parse(self, response):

        item = JokeItem()

        joke_selectors = response.xpath("//dl[@class='clearfix dl-con']")
        for joke_selector in joke_selectors:
            # 标题
            title = joke_selector.xpath("./dd/h1/a/text()").extract_first('')
            # 内容
            content = joke_selector.xpath("./dd/div[2]").extract_first('')
            content = remove_tags(content).strip()

            item['title'] = title
            item['content'] = content

            yield item

        if self.page < 50:
            self.page += 1
            next_url = self.url0 + 'xiaohua_' + str(self.page) + '.html'
            yield Request(url=next_url, callback=self.parse)